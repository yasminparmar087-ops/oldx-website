import {createServer} from 'node:http';
import {once} from 'node:events';
import {resolve} from 'node:path';
import {fileURLToPath} from 'node:url';

// H1 ONLY: deliberately no application/provider imports or enable flag.
// A future H2 image must be separately reviewed; PORT never activates Product.
const routes=new Set(['save','owner','archive','list','detail'].map(x=>'/api/staging/marketplace/'+x));
export function createC2OffMediatorServer(){
 const sockets=new Set();
 const server=createServer({maxHeaderSize:8192,requestTimeout:5000,headersTimeout:5000,
  connectionsCheckingInterval:1000},(req,res)=>{
  const path=req.url??'',health=path==='/health';
  let status=404,code='NOT_FOUND';
  const names=req.rawHeaders.filter((_,i)=>i%2===0).map(x=>x.toLowerCase());
  const forbidden=['cookie','authorization','x-serverless-authorization','x-oldx-gateway-attestation',
   'x-oldx-gateway-request-proof','x-oldx-mediated-website-origin','x-oldx-gateway-nonce'];
  if(names.some(x=>forbidden.includes(x))){status=403;code='DENIED';}
  else if(names.length>40||new Set(names).size!==names.length){status=400;code='INVALID_HEADERS';}
  else if(req.headers['content-length']!==undefined&&(!/^\d{1,5}$/.test(req.headers['content-length'])||Number(req.headers['content-length'])>(path.endsWith('/list')||path.endsWith('/detail')?4096:32768))){status=413;code='BODY_TOO_LARGE';}
  else if(health){status=['GET','HEAD'].includes(req.method)?200:405;code=status===200?null:'METHOD_NOT_ALLOWED';}
  else if(routes.has(path)){status=['POST','OPTIONS'].includes(req.method)?503:405;code=status===503?'ENFORCEMENT_UNAVAILABLE':'METHOD_NOT_ALLOWED';}
  const body=JSON.stringify(code===null?{ok:true}:{ok:false,error:{code}});
  res.shouldKeepAlive=false;
  res.writeHead(status,{'content-type':'application/json; charset=utf-8','content-length':Buffer.byteLength(body),
   'cache-control':'private, no-store','x-content-type-options':'nosniff','referrer-policy':'no-referrer',
   'content-security-policy':"default-src 'none'; frame-ancestors 'none'",'connection':'close'});
  res.end(req.method==='HEAD'?undefined:body);
 });
 server.maxRequestsPerSocket=1;
 server.on('connection',socket=>{
  if(sockets.size>=64){socket.destroy();return;}
  sockets.add(socket);socket.once('close',()=>sockets.delete(socket));
  socket.setTimeout(5000,()=>socket.destroy());
 });
 server.on('clientError',(_error,socket)=>socket.destroy());
 return server;
}
export async function listenC2OffMediator(server,{port,host='0.0.0.0'}={}){
 if(!/^[0-9]{1,5}$/.test(String(port))||Number(port)<1||Number(port)>65535||!['0.0.0.0','127.0.0.1'].includes(host))throw Error('C2_BIND_DENIED');
 server.listen(Number(port),host);await once(server,'listening');return server;
}
export async function drainC2OffMediator(server){
 const timer=setTimeout(()=>server.closeAllConnections(),6000);timer.unref();
 try{await new Promise((ok,fail)=>server.close(e=>e?fail(e):ok()));}
 finally{clearTimeout(timer);}
}
async function main(){
 const server=createC2OffMediatorServer();await listenC2OffMediator(server,{port:process.env.PORT??'8080'});
 let stopping=false;
 const stop=async()=>{
  if(stopping)return;stopping=true;
  const timer=setTimeout(()=>process.exit(1),8000);timer.unref();
  try{await drainC2OffMediator(server);}catch{process.exitCode=1;}
  finally{clearTimeout(timer);}
 };
 process.on('SIGTERM',stop);process.on('SIGINT',stop);
}
if(process.argv[1]&&resolve(process.argv[1])===fileURLToPath(import.meta.url))main().catch(()=>{process.exitCode=1;});

