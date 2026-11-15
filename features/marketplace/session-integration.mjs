// Shared existing-UI Auth lifecycle fanout. No Firebase listener, token storage,
// role resolution, endpoint or automatic activation. Hosts supply verified scope.
// Serialize all fanout work so a slow old sign-in cannot finish after logout and
// resurrect a private Product/Store/Provider view.
export function createMarketplaceSessionIntegration({enabled=false,bindings=[]}={}){
 let epoch=0,current=null,tail=Promise.resolve();
 const invalidate=()=>{epoch++;current=null;for(const binding of bindings){
  try{binding.changeScope?.();}catch{/* Continue invalidating other scopes. */}
 }return epoch;};
 const fanout=async value=>{
  const tasks=bindings.map(binding=>{
   try{
    if(typeof binding.setSession!=='function')throw new Error('Missing lifecycle port');
    return Promise.resolve(binding.setSession(value&&{...value}));
   }catch{return Promise.reject(new Error('Lifecycle unavailable'));}
  });
  const settled=await Promise.allSettled(tasks);
  return settled.every(item=>item.status==='fulfilled');
 };
 const enqueue=task=>{const result=tail.then(task,task);tail=result.then(()=>{},()=>{});return result;};
 const clear=()=>{
  const version=invalidate();
  return enqueue(async()=>{const ok=await fanout(null);return version===epoch&&ok;});
 };
 return Object.freeze({
  async setSession(value){
   if(!enabled)return false;
   if(!value||typeof value.uid!=='string'||!/^[A-Za-z0-9_-]{1,100}$/.test(value.uid)||
      typeof value.sessionId!=='string'||!/^[A-Za-z0-9_-]{1,100}$/.test(value.sessionId)){
    await clear();return false;
   }
   const version=invalidate(),scope={uid:value.uid,sessionId:value.sessionId};
   return enqueue(async()=>{
    // An obsolete queued login is skipped, not sent to private bindings.
    if(version!==epoch)return false;
    const ok=await fanout(scope);
    if(version!==epoch)return false;
    if(!ok){await fanout(null);return false;}
    current={...scope};
    return true;
   });
  },
  logout:clear,
  changeScope(){for(const binding of bindings){try{binding.changeScope?.();}catch{}}},
  snapshot:()=>current&&{...current},
 });
}

// Existing Provider UI requires its initial revision/generation scope. Zero is a
// bootstrap starting point, not a grant or fabricated persisted revision.
export function providerSessionBinding(journey){return Object.freeze({setSession:value=>journey.setSession(value?{...value,revision:0,generation:0}:null),changeScope:()=>journey.changeScope()});}
