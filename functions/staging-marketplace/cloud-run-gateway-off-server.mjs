import {createServer} from 'node:http';
import {once} from 'node:events';
import {resolve} from 'node:path';
import {fileURLToPath} from 'node:url';

// Isolated Step05 C1A OFF-only Cloud Run entrypoint. No application imports,
// ADC/Firestore/KMS/network clients, IAM token mint, credential reads or routes.
// The existing private Product service and original traffic remain untouched.
const headers=Object.freeze({
 'content-type':'application/json; charset=utf-8',
 'cache-control':'private, no-store',
 'x-content-type-options':'nosniff',
 'referrer-policy':'no-referrer'
});
const result=(res,status,code,head=false)=>{
 if(res.headersSent||res.destroyed)return;
 const payload=JSON.stringify(code===null?{ok:true}:{ok:false,error:{code}});
 res.shouldKeepAlive=false;
 res.writeHead(status,{...headers,'content-length':Buffer.byteLength(payload),'connection':'close'});
 res.end(head?undefined:payload);
};

export function createStep05OffGatewayServer(){
 return createServer({maxHeaderSize:8192,requestTimeout:5000,headersTimeout:5000,
  connectionsCheckingInterval:1000},(req,res)=>{
  const path=req.url??'';
  if(path==='/healthz'||path==='/health'){
   if(req.method!=='GET'&&req.method!=='HEAD')return result(res,405,'METHOD_NOT_ALLOWED');
   return result(res,200,null,req.method==='HEAD');
  }
  if(path==='/api'||path.startsWith('/api/')||path.startsWith('/api?'))
   return result(res,503,'ENFORCEMENT_UNAVAILABLE');
  return result(res,404,'NOT_FOUND');
 });
}

export async function listenStep05OffGateway(server,{port=process.env.PORT??'8080',host='0.0.0.0'}={}){
 if(!/^[0-9]{1,5}$/.test(String(port))||Number(port)<1||Number(port)>65535||
  !['0.0.0.0','127.0.0.1'].includes(host))throw Error('Invalid Gateway bind');
 server.listen(Number(port),host);
 await once(server,'listening');
 return server;
}
export async function drainStep05OffGateway(server){
 const timer=setTimeout(()=>server.closeAllConnections(),7000);timer.unref();
 try{await new Promise((ok,fail)=>server.close(error=>error?fail(error):ok()));}
 finally{clearTimeout(timer);}
}
async function main(){
 const server=createStep05OffGatewayServer();
 await listenStep05OffGateway(server);
 let stopping=false;
 const stop=async()=>{
  if(stopping)return;
  stopping=true;
  const deadline=setTimeout(()=>process.exit(1),9000);deadline.unref();
  try{await drainStep05OffGateway(server);}catch{process.exitCode=1;}
  finally{clearTimeout(deadline);}
 };
 process.on('SIGTERM',stop);process.on('SIGINT',stop);
}
if(process.argv[1]&&resolve(process.argv[1])===fileURLToPath(import.meta.url)){
 main().catch(()=>{process.exitCode=1;});
}
