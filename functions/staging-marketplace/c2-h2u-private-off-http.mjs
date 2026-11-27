import {createServer} from 'node:http';

// H2U: OFF-ONLY source for a FUTURE IAM-private Cloud Run Gateway.
// No deployment, secret, IAM principal, KMS call, Firestore transaction,
// listener, or enabled Product route is created by importing this module.
// The Cloud Run FRONTEND must enforce Invoker auth; /healthz returning 200
// here does NOT mean this process authenticated the caller.
const OPERATIONS=new Set(['save','owner','archive','list','detail']);
const MEDIA_TYPE='application/json; charset=utf-8';
const HEADERS=Object.freeze({
  'content-type':MEDIA_TYPE,
  'cache-control':'private, no-store',
  'x-content-type-options':'nosniff',
  'content-security-policy':"default-src 'none'",
  'connection':'close',
});
const reply=(res,status,body)=>{
  res.writeHead(status,HEADERS);
  res.end(JSON.stringify(body)+'\n');
};

export function parseC2H2UCloudRunPort(value){
  if(typeof value!=='string'||!/^[1-9][0-9]{0,4}$/.test(value)||
     Number(value)>65535)throw Error('H2U_INVALID_CLOUD_RUN_PORT');
  return Number(value);
}

export function createC2H2UPrivateOffRequestHandler(){
  // No option accepts "enabled": this version can NEVER dispatch to a real
  // H2S signer or call an injected backend/metadata/Firestore provider.
  return Object.freeze((req,res)=>{
    const method=req?.method;
    const target=req?.url;
    if(typeof method!=='string'||typeof target!=='string'||
       target.length>2048){
      reply(res,400,{ok:false,error:{code:'INVALID_REQUEST'}});
      return;
    }
    if(method==='GET'&&target==='/healthz'){
      reply(res,200,{ok:true,service:'oldx-c2-private-gateway',mode:'OFF'});
      return;
    }
    const match=/^\/api\/staging\/marketplace\/([a-z]+)$/.exec(target);
    if(match&&OPERATIONS.has(match[1])){
      reply(res,503,{ok:false,error:{code:'H2_GATEWAY_DISABLED'}});
      return;
    }
    reply(res,404,{ok:false,error:{code:'NOT_FOUND'}});
  });
}

export function createC2H2UPrivateOffHttpServer(){
  const server=createServer({maxHeaderSize:8192,requireHostHeader:true},
    createC2H2UPrivateOffRequestHandler());
  server.headersTimeout=5000;
  server.requestTimeout=10000;
  server.keepAliveTimeout=1000;
  server.maxRequestsPerSocket=16;
  return server; // caller MUST call .listen() explicitly; no side effects.
}
