import {copyRecord} from './isolated-firestore-context.mjs';
import {STAGING_MARKETPLACE_COLLECTIONS as c,STAGING_MEDIA_COLLECTIONS as m} from './staging-marketplace-context.mjs';
const allowed=new Set([c.actors,c.privateRecords,c.publicViews,c.receipts,c.audits,m.assets,m.associations,m.reviews,m.publications,m.permissions,m.receipts,m.audits]);
// Pure DRAFT validator, NOT a delete tool or proof that captured metadata is true.
// Shared generations/rate/nonce collections are deliberately excluded: current
// numeric nonce expiry alone cannot safely prove per-run ownership or enable TTL.
export function prepareC2SyntheticCleanupManifest({enabled=false,projectId,databaseId,runId,actors,records}={}){
 const stop=reason=>({decision:'STOP',reason,authorized:false});
 if(enabled!==true)return stop('DISABLED');
 if(projectId!=='oldx-staging'||databaseId!=='(default)'||typeof runId!=='string'||!/^[A-Za-z0-9_-]{1,30}$/.test(runId)||!Array.isArray(actors)||actors.length<1||actors.length>2||!Array.isArray(records)||records.length>128)return stop('SCOPE');
 const ids=new Set(actors);if(ids.size!==actors.length||actors.some(uid=>!['synthetic-c2-'+runId+'-seller','synthetic-c2-'+runId+'-buyer'].includes(uid)))return stop('ACTORS');
 const seen=new Set(),captured=[],products=new Set(),photos=new Set();
 for(const raw of records){
  const row=copyRecord(raw,['ownerUid','path','runId','updateTime']);
  if(!row||Object.getPrototypeOf(row)!==Object.prototype||Object.keys(row).sort().join(',')!=='ownerUid,path,runId,updateTime'||row.runId!==runId||!ids.has(row.ownerUid)||typeof row.path!=='string'||row.path.length>220||seen.has(row.path)||typeof row.updateTime!=='string'||!/^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(?:\.\d{1,9})?Z$/.test(row.updateTime))return stop('RECORD');
  const parts=row.path.split('/');if(parts.length!==2||!allowed.has(parts[0])||!/^[A-Za-z0-9_-]{1,100}$/.test(parts[1]))return stop('SHARED_OR_FOREIGN_PATH');
  if([c.privateRecords,c.publicViews].includes(parts[0])&&!parts[1].startsWith('product_'))return stop('FOREIGN_PRODUCT_KIND');
  if(parts[0]===c.actors&&parts[1]!==row.ownerUid)return stop('FOREIGN_ACTOR');
  if([c.privateRecords,c.publicViews].includes(parts[0]))products.add(parts[1]);
  if(parts[0]===m.assets)photos.add(parts[1]);
  if(products.size>1||photos.size>1)return stop('SYNTHETIC_OBJECT_CAP');
  seen.add(row.path);captured.push({...row});
 }
 const out={decision:'DRAFT_ONLY',authorized:false,projectId,databaseId,runId,actors:[...actors],records:captured,
  requires:'fresh exact-path owner/run-marker/updateTime/no-dependency readback + action-specific owner delete consent; Auth creation-time safeguards separately required',
  excluded:'shared generations, rate/nonce rows, infrastructure and provider blobs; no TTL/deletion execution'};
 if(Buffer.byteLength(JSON.stringify(out),'utf8')>32768)return stop('SIZE');
 return out;
}



// PURE evidence reconciliation, never a delete provider or ownership proof.
// Trusted future host must capture real native-schema linkage/version evidence.
export function reconcileC2SyntheticCleanup({enabled=false,manifest,readbacks=[],results=[]}={}){
 const stop=reason=>({decision:'STOP',authorized:false,reason});
 const m=copyRecord(manifest,['decision','authorized','projectId','databaseId','runId','actors','records','requires','excluded']);
 if(enabled!==true||m?.decision!=='DRAFT_ONLY'||m.authorized!==false)return stop('DISABLED_OR_MANIFEST');
 const draft=prepareC2SyntheticCleanupManifest({enabled:true,projectId:m.projectId,databaseId:m.databaseId,runId:m.runId,actors:m.actors,records:m.records});
 if(draft.decision!=='DRAFT_ONLY'||!Array.isArray(readbacks)||!Array.isArray(results)||readbacks.length!==draft.records.length||results.length>draft.records.length)return stop('SCOPE');
 const rows=new Map(),outcomes=new Map();
 for(const raw of readbacks){
  const r=copyRecord(raw,['path','ownerUid','runId','updateTime','exists','dependencies']);
  if(!r||typeof r.path!=='string'||rows.has(r.path)||typeof r.exists!=='boolean'||!Array.isArray(r.dependencies)||r.dependencies.length>32||r.dependencies.length!==0)return stop('DEPENDENCY_OR_READBACK');
  rows.set(r.path,r);
 }
 for(const raw of results){
  const r=copyRecord(raw,['path','updateTime','status']);
  if(!r||outcomes.has(r.path)||!['DELETED_CONFIRMED','FAILED','UNKNOWN'].includes(r.status))return stop('OUTCOME');
  outcomes.set(r.path,r);
 }
 const paths=new Set(draft.records.map(r=>r.path));if([...rows.keys(),...outcomes.keys()].some(p=>!paths.has(p)))return stop('FOREIGN_PATH');
 const completed=[],pending=[],uncertain=[];
 for(const row of draft.records){
  const r=rows.get(row.path),outcome=outcomes.get(row.path);
  if(!r||r.ownerUid!==row.ownerUid||r.runId!==row.runId||r.updateTime!==row.updateTime||outcome&&outcome.updateTime!==row.updateTime)return stop('OWNER_OR_VERSION');
  if(outcome?.status==='DELETED_CONFIRMED'){
   if(r.exists!==false)return stop('DELETE_NOT_CONFIRMED');completed.push(row.path);
  }else if(outcome){uncertain.push(row.path);}
  else{if(!r.exists)return stop('UNEXPLAINED_ABSENCE');pending.push(row.path);}
 }
 // Unknown/failed deletion never licenses retry. All output remains a draft.
 return {decision:uncertain.length?'PARTIAL_STOP':pending.length?'DRAFT_READY':'DRAFT_COMPLETE',authorized:false,
  completed,pending,uncertain,requires:'independent real-schema ownership/dependency/version verification and separate delete authority; no automatic retry'};
}
