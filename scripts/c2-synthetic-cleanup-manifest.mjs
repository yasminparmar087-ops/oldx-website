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
 const seen=new Set(),captured=[];
 for(const raw of records){
  const row=copyRecord(raw,['ownerUid','path','runId','updateTime']);
  if(!row||Object.getPrototypeOf(row)!==Object.prototype||Object.keys(row).sort().join(',')!=='ownerUid,path,runId,updateTime'||row.runId!==runId||!ids.has(row.ownerUid)||typeof row.path!=='string'||row.path.length>220||seen.has(row.path)||typeof row.updateTime!=='string'||!/^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(?:\.\d{1,9})?Z$/.test(row.updateTime))return stop('RECORD');
  const parts=row.path.split('/');if(parts.length!==2||!allowed.has(parts[0])||!/^[A-Za-z0-9_-]{1,100}$/.test(parts[1]))return stop('SHARED_OR_FOREIGN_PATH');
  if([c.privateRecords,c.publicViews].includes(parts[0])&&!parts[1].startsWith('product_'))return stop('FOREIGN_PRODUCT_KIND');
  if(parts[0]===c.actors&&parts[1]!==row.ownerUid)return stop('FOREIGN_ACTOR');
  seen.add(row.path);captured.push({...row});
 }
 const out={decision:'DRAFT_ONLY',authorized:false,projectId,databaseId,runId,actors:[...actors],records:captured,
  requires:'fresh exact-path owner/run-marker/updateTime/no-dependency readback + action-specific owner delete consent; Auth creation-time safeguards separately required',
  excluded:'shared generations, rate/nonce rows, infrastructure and provider blobs; no TTL/deletion execution'};
 if(Buffer.byteLength(JSON.stringify(out),'utf8')>32768)return stop('SIZE');
 return out;
}
