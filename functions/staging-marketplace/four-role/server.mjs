import {createServer} from 'node:http';
import {c2LifecycleBoundary} from '../../../scripts/c2-h2-lifecycle-boundary.mjs';
import {bootstrapFourRole} from './bootstrap.mjs';
import {readBytes} from './protocol.mjs';
export function createFourRoleServer({role,runtime={ready:false}}={}){
 const server=createServer(async(req,res)=>{
 const abort=new AbortController();req.on('aborted',()=>abort.abort());res.on('close',()=>abort.abort());
 try{
 if(req.url==='/healthz'&&req.method==='GET'){
 res.writeHead(200,{'content-type':'application/json','cache-control':'no-store'});
 res.end(JSON.stringify({ok:true,role,state:runtime.ready===true&&runtime.isBound?.()===true?'BOUND':'OFF',productReady:false}));return;
 }
 if(runtime.ready!==true||runtime.isBound&&runtime.isBound()!==true){res.writeHead(503,{'cache-control':'no-store'});res.end();return;}
 if(req.method!=='POST'||!req.url.startsWith('/')||req.url.startsWith('//')||req.url.includes('?')||
 req.url.includes('#')||req.headers.cookie){res.writeHead(403);res.end();return;}
 const result=await c2LifecycleBoundary(async signal=>{
 let size=0;const parts=[];
 for await(const part of req){size+=part.length;if(size>32768)throw Error('SIZE');parts.push(part);}
 const origin=runtime.origin;if(!origin)throw Error('ORIGIN');
 const request=new Request(origin+req.url,{method:'POST',headers:req.headers,body:Buffer.concat(parts),signal});
 const response=await runtime.fetch(request),bytes=await readBytes(response,32768);
 return {status:response.status,headers:Object.fromEntries(response.headers),bytes};
 },{signal:abort.signal,timeoutMs:5000});
 res.writeHead(result.status,{...result.headers,'cache-control':'no-store','x-content-type-options':'nosniff'});res.end(result.bytes);
 }catch{if(!res.headersSent)res.writeHead(503,{'cache-control':'no-store'});res.end();}
 });
 server.requestTimeout=5000;server.headersTimeout=5000;server.keepAliveTimeout=1000;
 server.maxHeadersCount=40;server.maxRequestsPerSocket=1;
 return server;
}
export async function runFourRole(role,{env=process.env}={}){
 const runtime=await bootstrapFourRole(role,{env}),port=env.PORT??'8080';
 if(!/^[0-9]{1,5}$/.test(port)||Number(port)>65535)throw Error('PORT');
 const server=createFourRoleServer({role,runtime});
 await new Promise((resolve,reject)=>{server.once('error',reject);server.listen(Number(port),'0.0.0.0',resolve);});
 if(process.send)process.send({type:'h2ah-listening',role,port:server.address().port,pid:process.pid});
 let stopping=false;
 const stop=()=>{if(stopping)return;stopping=true;
 const timer=setTimeout(()=>{server.closeAllConnections();},4500);timer.unref();
 server.close(async()=>{clearTimeout(timer);await runtime.close?.();});
 };
 process.once('SIGTERM',stop);process.once('SIGINT',stop);
 return server;
}
