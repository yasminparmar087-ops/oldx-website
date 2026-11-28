import {requireC2H2LifecycleStageLedger} from '../../../scripts/c2-h2-lifecycle-stage-ledger.mjs';
import {requireFourRoleProtocol} from './protocol.mjs';
import {parseBoundedJson} from '../../../scripts/bounded-json.mjs';
const allowed={mediator:['reserve','finish','consumeGuest'],gateway:['claimSign'],reader:['consumeStatusRead']};
export function createBackendLedgerRpc({policy,ledger,protocol,guestAdmission,now=Date.now}={}){
 requireC2H2LifecycleStageLedger(ledger,policy);requireFourRoleProtocol(protocol,{role:'backend'});
 return async request=>{
 try{
 const ctx=await protocol.receive(request,{fromRoles:Object.keys(allowed),path:'/internal/ledger'});
 if(!allowed[ctx.from]?.includes(ctx.operation))throw Error('OPERATION');
 const input=parseBoundedJson(ctx.body,{maxBytes:8192});if(!input.ok)throw Error('BODY');
 if(ctx.operation!=='reserve'&&input.value.reservation!==ctx.reservation)throw Error('RESERVATION');
 const result=ctx.operation==='consumeGuest'?await guestAdmission({operation:input.value.operation},
 {signal:request.signal,deadlineAt:now()+1000}):await ledger[ctx.operation](input.value,{signal:request.signal});
 return Response.json(result,{headers:{'cache-control':'no-store'}});
 }catch{return Response.json({allowed:false},{status:403});}
 };
}
