// No ambient IO. A rejecting deadline also bounds providers ignoring AbortSignal.
export async function c2LifecycleBoundary(operation,{signal,timeoutMs=1000}={}) {
  const ctl=new AbortController(),abort=()=>ctl.abort();
  signal?.addEventListener('abort',abort,{once:true});if(signal?.aborted)abort();
  let reject;const stopped=new Promise((_,no)=>{reject=no;});stopped.catch(()=>{});
  ctl.signal.addEventListener('abort',()=>reject(Error('C2_LIFECYCLE_STOP')),{once:true});
  if(ctl.signal.aborted)reject(Error('C2_LIFECYCLE_STOP'));
  const timer=setTimeout(abort,timeoutMs);
  try{return await Promise.race([Promise.resolve().then(()=>{
    if(ctl.signal.aborted)throw Error('C2_LIFECYCLE_STOP');return operation(ctl.signal);
  }),stopped]);}
  finally{clearTimeout(timer);signal?.removeEventListener('abort',abort);abort();}
}
