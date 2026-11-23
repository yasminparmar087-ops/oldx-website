// Inactive injected HTTPS transport. No global fetch, SDK, cookies, stored tokens,
// retries, Cloud Run IAM token minting or automatic route installation.
const commands=new Set(['save','owner','archive']),reads=new Set(['list','detail']);
const failure=()=>({status:503,body:{ok:false,error:{code:'ENFORCEMENT_UNAVAILABLE'}}});
export function createMarketplaceHttpTransport({enabled=false,origin,fetchRequest}={}){
 let base;
 try{const u=new URL(origin);if(u.protocol==='https:'&&!u.username&&!u.password&&u.pathname==='/'&&!u.search&&!u.hash)base=u.origin;}catch{}
 async function send(operation,body,{credential,signal}={},privateRequest=false){
  if(enabled!==true||!base||typeof fetchRequest!=='function'||!(privateRequest?commands:reads).has(operation))return failure();
  if(signal?.aborted)throw Error('CANCELLED');
  if(privateRequest&&(typeof credential!=='string'||credential.length>8192||!/^[-\w]+\.[-\w]+\.[-\w]+$/.test(credential)))return {status:401,body:{ok:false,error:{code:'AUTH_REQUIRED'}}};
  const payload=JSON.stringify(body);
  if(new TextEncoder().encode(payload).byteLength>(privateRequest?32768:4096))return {status:413,body:{ok:false,error:{code:'INVALID_REQUEST'}}};
  // A thrown/lost response propagates to the existing authenticated client,
  // which preserves the mutation requestId and reports OUTCOME_UNKNOWN.
  const answer=await fetchRequest(base+'/api/staging/marketplace/'+operation,{
   method:'POST',headers:{'content-type':'application/json',...(privateRequest?{authorization:'Bearer '+credential}:{})},
   body:payload,signal,credentials:'omit',cache:'no-store',redirect:'error',referrerPolicy:'no-referrer'
  });
  if(!(answer instanceof Response)||answer.redirected||!/^application\/json(?:;\s*charset=utf-8)?$/i.test(answer.headers.get('content-type')??''))throw Error('INVALID_RESPONSE');
  const reader=answer.body?.getReader();if(!reader)throw Error('INVALID_RESPONSE');
  const chunks=[];let size=0;
  try{while(true){const {done,value}=await reader.read();if(done)break;size+=value.byteLength;if(size>65536)throw Error('INVALID_RESPONSE');chunks.push(value);if(signal?.aborted)throw Error('CANCELLED');}}
  finally{await reader.cancel().catch(()=>{});}
  const bytes=new Uint8Array(size);let offset=0;for(const part of chunks){bytes.set(part,offset);offset+=part.byteLength;}
  if(signal?.aborted)throw Error('CANCELLED');
  return {status:answer.status,body:JSON.parse(new TextDecoder('utf-8',{fatal:true}).decode(bytes))};
 }
 return Object.freeze({sendCommand:(op,body,ctx)=>send(op,body,ctx,true),sendRead:(op,body,ctx)=>send(op,body,ctx)});
}

