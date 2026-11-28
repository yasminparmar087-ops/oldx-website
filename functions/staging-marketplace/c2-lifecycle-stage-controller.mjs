import {requireC2H2LifecycleStageLedger} from '../../scripts/c2-h2-lifecycle-stage-ledger.mjs';
import {createHash} from 'node:crypto';
import {requireC2H2MultiSignLifecyclePolicy} from '../../scripts/c2-h2-lifecycle-signing-status-contract.mjs';
import {c2LifecycleBoundary} from '../../scripts/c2-h2-lifecycle-boundary.mjs';
import {createStagingMarketplaceEnforcement} from '../../scripts/provider-enforcement-adapters.mjs';
const digest=x=>createHash('sha256').update(x).digest('hex');
const failure=(status=503,code='LIFECYCLE_BLOCKED')=>Response.json({ok:false,error:{code}},{status});
const pathFor=['save','save','list','detail','save','save'];
// SERVER-HELD orchestration, not a browser bearer-grant endpoint. The ledger
// reserves before dispatch, and the signing host must atomically claim that
// reservation against canonical proof body/auth/path before each signature.
// Actual HTTP/IAM hops stay in existing mediator/Gateway/backend factories.
export function createC2LifecycleStageController({enabled=false,policy,ledger,
  adminAuth,websiteOrigin,getCurrentSession,dispatch,now=Date.now}={}) {
  const off=Object.freeze({ready:false,execute:async()=>failure()});
  if(enabled!==true)return off;
  let p,auth;
  try {
    p=requireC2H2MultiSignLifecyclePolicy(policy);requireC2H2LifecycleStageLedger(ledger,p);
    const u=new URL(websiteOrigin);if(u.origin!==websiteOrigin||u.protocol!=='https:')return off;
    if(ledger?.ready!==true||![ledger.reserve,ledger.finish,getCurrentSession,dispatch,now].every(x=>typeof x==='function'))return off;
    auth=createStagingMarketplaceEnforcement({enabled:true,adminAuth,now});
  }catch{return off;}
  const fresh=signal=>{const t=now();if(signal.aborted||!Number.isSafeInteger(t)||t<p.startsAtMs||t>=p.expiresAtMs)throw Error('STOP');};
  return Object.freeze({ready:true,async execute({phase,sessionToken,sessionId,request,signal}={}) {
    const index=p.phases.findIndex(x=>x.phase===phase),stage=p.phases[index];
    if(!stage||!(request instanceof Request)||typeof sessionToken!=='string'||
       typeof sessionId!=='string'||sessionId.length<1||sessionId.length>100)return failure(403,'DENIED');
    let reservation=null;
    try{return await c2LifecycleBoundary(async sig=>{
      fresh(sig);
      const current=()=>getCurrentSession();
      const matches=()=>{const s=current();return s?.uid===stage.actor&&s.sessionId===sessionId;};
      if(!matches())return failure(403,'DENIED');
      const claims=await auth.verifyFirebaseToken(sessionToken,{checkRevoked:true,signal:sig});
      if(claims?.uid!==stage.actor||!matches())return failure(403,'DENIED');
      const url=new URL(request.url),op=pathFor[index],guest=index===2||index===3;
      if(url.origin!==websiteOrigin||url.pathname!=='/api/staging/marketplace/'+op||
         url.search||url.hash||request.method!=='POST'||request.headers.get('origin')!==websiteOrigin||
         request.headers.has('cookie')||[...request.headers.keys()].some(k=>k.startsWith('x-oldx-')||k==='x-serverless-authorization')||
         request.headers.get('content-type')!=='application/json'||
         request.headers.get('authorization')!==(guest?null:'Bearer '+sessionToken))return failure(403,'DENIED');
      const chunks=[];let bytes=0;const reader=request.clone().body?.getReader();
      if(!reader)return failure(400,'INVALID_REQUEST');
      try{for(;;){const {done,value}=await reader.read();if(done)break;bytes+=value.byteLength;
        if(bytes>(guest?4096:32768))throw Error('SIZE');chunks.push(value);}}
      finally{void reader.cancel().catch(()=>{});}
      fresh(sig);const body=Buffer.concat(chunks),data=JSON.parse(body.toString('utf8'));
      // Repository remains the authority for ownership/moderation/revision.
      // This additionally pins the six orchestration stages and single Product.
      const product='c2_'+p.runId+'_product';
      if(data.kind!=='product'||op!=='list'&&data.id!==(index===0?null:product)||
         op==='save'&&data.publication!==['draft','publish',null,null,'draft','withdraw'][index])
        return failure(403,'DENIED');
      if(!matches())return failure(403,'DENIED');
      const reserved=await ledger.reserve({phase,actor:claims.uid,nonceSha256:stage.nonceSha256,
        requestSha256:digest(body),sessionSha256:digest(JSON.stringify([claims.uid,sessionId,sessionToken])),
        authSha256:digest(request.headers.get('authorization')??'')},{signal:sig});
      fresh(sig);if(reserved?.allowed!==true)return failure(409,'STAGE_CONSUMED');
      reservation=reserved.reservation;
      if(!matches())throw Error('SESSION_CHANGED');
      // Reservation is server context, NEVER an HTTP authorization/header.
      const response=await dispatch(new Request(request.url,{method:'POST',headers:request.headers,
        body,signal:sig}),{phase,reservation,signal:sig});
      fresh(sig);if(!(response instanceof Response)||!matches())throw Error('OUTCOME_UNKNOWN');
      // Consume the bounded response inside the deadline. Returning a live
      // fetch body would let deadline cleanup abort it after a confirmed write.
      const parts=[];let size=0;const output=response.body?.getReader();
      if(output)try{for(;;){const {done,value}=await output.read();if(done)break;
        size+=value.byteLength;if(size>32768)throw Error('RESPONSE_SIZE');parts.push(value);}}
      finally{void output.cancel().catch(()=>{});}
      fresh(sig);const retained=Buffer.concat(parts);
      // No effect is retried. Non-200 or lost response quarantines the lifecycle.
      const done=await ledger.finish({reservation,outcome:response.status===200?'CONFIRMED':'UNKNOWN',
        responseSha256:digest(Buffer.concat([Buffer.from(String(response.status)),retained]))},{signal:sig});
      if(done?.allowed!==true)throw Error('OUTCOME_UNKNOWN');
      return new Response(retained,{status:response.status,headers:response.headers});
    },{signal:signal??request.signal,timeoutMs:5000});}
    catch{return reservation?failure(202,'OUTCOME_UNKNOWN'):failure();}
    // A lost/expired finish leaves PENDING permanently; no automatic retry.
  }});
}
