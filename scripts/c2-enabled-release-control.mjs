import {createHash} from 'node:crypto';
import {copyRecord} from './isolated-firestore-context.mjs';
const controls=new WeakSet();
const operations=new Set(['save','owner','archive','list','detail']);
const hex=v=>typeof v==='string'&&/^[a-f0-9]{64}$/.test(v)&&v!=='0'.repeat(64);
const integer=v=>Number.isSafeInteger(v)&&v>=0;
const principal=v=>typeof v==='string'&&/^[a-z][a-z0-9-]{4,28}[a-z0-9]@oldx-staging\.iam\.gserviceaccount\.com$/.test(v);
const image=v=>typeof v==='string'&&/^asia-south1-docker\.pkg\.dev\/oldx-staging\/oldx-staging-images\/[a-z0-9][a-z0-9_-]{0,80}@sha256:[a-f0-9]{64}$/.test(v)&&
 !['576a1faa599459ed9b1cdeccc01a3adc2076dffff617bec42f38df7d3a75663e','612f3c02806a93d991127f87e34391646edf9bad251bb22b8aace90a434bc30a'].some(x=>v.endsWith(x));
const failure=(code='ENFORCEMENT_UNAVAILABLE',status=503)=>Response.json({ok:false,error:{code}},{status,headers:{'cache-control':'private, no-store'}});
// Trusted SERVER configuration only, not browser input or authentication proof.
// verifyApproval must independently verify H2 authority for this exact digest.
// consumeRunBudget MUST be durable/atomic across hosts; local fixtures do NOT qualify.
export function createC2EnabledReleaseControl({enabled=false,contract,verifyApproval,consumeRunBudget,now=Date.now}={}){
 let snapshot,digest,ready=false;
 try{
  const c=copyRecord(contract,['v','purpose','runId','projectId','databaseId','startsAtMs','expiresAtMs','principals','images','evidence','limits','actors','managedPhotoId']);
  const p=copyRecord(c?.principals,['mediator','gateway','backend']);
  const i=copyRecord(c?.images,['mediator','gateway','backend']);
  const e=copyRecord(c?.evidence,['identity','iam','media','cleanup','security','rollback']);
  const actors=copyRecord(c?.actors,['seller','buyer']);
  const l=copyRecord(c?.limits,['maxRequests','maxActors','maxProducts','maxPhotos']);
  ready=enabled===true&&c?.v===1&&c.purpose==='oldx.c2.enabled-product.synthetic.v1'&&c.projectId==='oldx-staging'&&c.databaseId==='(default)'&&
   typeof c.runId==='string'&&/^[A-Za-z0-9_-]{1,30}$/.test(c.runId)&&integer(c.startsAtMs)&&integer(c.expiresAtMs)&&c.expiresAtMs>c.startsAtMs&&c.expiresAtMs-c.startsAtMs<=1200000&&
   !!p&&Object.values(p).every(principal)&&new Set(Object.values(p)).size===3&&!!i&&Object.values(i).every(image)&&
   !!actors&&actors.seller==='synthetic-c2-'+c.runId+'-seller'&&actors.buyer==='synthetic-c2-'+c.runId+'-buyer'&&typeof c.managedPhotoId==='string'&&/^[A-Za-z0-9_-]{20,80}$/.test(c.managedPhotoId)&&!!e&&Object.values(e).every(hex)&&!!l&&Number.isSafeInteger(l.maxRequests)&&l.maxRequests>0&&l.maxRequests<=20&&l.maxActors===2&&l.maxProducts===1&&l.maxPhotos===1&&
   [verifyApproval,consumeRunBudget,now].every(x=>typeof x==='function');
  if(ready){
   snapshot=Object.freeze({...c,principals:Object.freeze({...p}),images:Object.freeze({...i}),evidence:Object.freeze({...e}),actors:Object.freeze({...actors}),limits:Object.freeze({...l})});
   digest=createHash('sha256').update(JSON.stringify(snapshot)).digest('hex');
  }
 }catch{ready=false;}
 const fresh=()=>{const t=now();return integer(t)&&t>=snapshot?.startsAtMs&&t<snapshot?.expiresAtMs;};
 const control=Object.freeze({ready,contractDigest:ready?digest:null,
  runtimePrincipal:ready?snapshot.principals.backend:null,
  runtimeImage:ready?snapshot.images.backend:null,
  productId:ready?'c2_'+snapshot.runId+'_product':null,
  isActorAllowed:uid=>ready&&Object.values(snapshot.actors).includes(uid),
  wrap(backend){
   return Object.freeze({async fetch(request){
    if(!ready||!fresh()||!(request instanceof Request)||typeof backend?.fetch!=='function')return failure();
    const u=new URL(request.url),op=u.pathname.split('/').at(-1);
    if(request.method!=='POST'||u.search||u.hash||u.pathname!=='/api/staging/marketplace/'+op||!operations.has(op))return failure('INVALID_REQUEST',400);
    const ctl=new AbortController(),abort=()=>ctl.abort();
    request.signal.addEventListener('abort',abort,{once:true});if(request.signal.aborted)abort();
    const stopped=new Promise((_,reject)=>{ctl.signal.addEventListener('abort',()=>reject(Error('Stopped')),{once:true});if(ctl.signal.aborted)reject(Error('Stopped'));});stopped.catch(()=>{});
    const wait=fn=>Promise.race([Promise.resolve().then(()=>{if(ctl.signal.aborted||!fresh())throw Error('Stopped');return fn();}),stopped]);
    const timer=setTimeout(abort,Math.max(1,Math.min(5000,snapshot.expiresAtMs-now())));
    let dispatched=false;
    try{
     const reader=request.clone().body?.getReader();if(!reader)return failure('INVALID_REQUEST',400);
     const chunks=[];let size=0;
     try{for(;;){const {done,value}=await wait(()=>reader.read());if(done)break;size+=value.byteLength;
      if(size>(['list','detail'].includes(op)?4096:32768))return failure('INVALID_REQUEST',413);chunks.push(value);
     }}finally{void reader.cancel().catch(()=>{});}
     const bytes=Buffer.concat(chunks,size),body=JSON.parse(new TextDecoder('utf-8',{fatal:true}).decode(bytes));
     if(body?.kind!=='product')return failure('INVALID_REQUEST',400);
     if(body.id!==undefined&&body.id!==null&&body.id!=='c2_'+snapshot.runId+'_product')return failure('DENIED',403);
     if(op==='save'&&(!Array.isArray(body.profile?.photos)||body.profile.photos.length>1||
      body.profile.photos.some(photo=>photo?.kind!=='managed'||photo.imageId!==snapshot.managedPhotoId)))return failure('PHOTOS_REQUIRED',403);

     const approval=copyRecord(await wait(()=>verifyApproval(structuredClone(snapshot),{contractDigest:digest,signal:ctl.signal})),['authorized','contractDigest','expiresAtMs']);
     if(!approval||approval.authorized!==true||approval.contractDigest!==digest||approval.expiresAtMs!==snapshot.expiresAtMs||!fresh())return failure();
     const budget=copyRecord(await wait(()=>consumeRunBudget({runId:snapshot.runId,operation:op,projectId:snapshot.projectId,databaseId:snapshot.databaseId,
      limits:{...snapshot.limits},expiresAtMs:snapshot.expiresAtMs},{signal:ctl.signal})),['allowed']);
     if(budget?.allowed!==true)return failure('RATE_LIMITED',429);
     const response=await wait(()=>{dispatched=true;return backend.fetch(new Request(request,{signal:ctl.signal}));});
     if(!fresh())throw Error('Expired');
     return response instanceof Response?response:failure();
    }catch{
     return dispatched&&['save','archive'].includes(op)?Response.json({ok:false,error:{code:'OUTCOME_UNKNOWN'},retrySameRequest:true},{status:202,headers:{'cache-control':'private, no-store'}}):failure();
    }finally{clearTimeout(timer);request.signal.removeEventListener('abort',abort);}
   }});
  }});
 controls.add(control);return control;
}
export function requireC2EnabledReleaseControl(control){
 if(!controls.has(control)||control.ready!==true)throw Error('C2_RELEASE_UNAVAILABLE');
 return control;
}
