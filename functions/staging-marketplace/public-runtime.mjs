import {createStagingMarketplaceGuestRate} from '../../scripts/staging-marketplace-guest-rate.mjs';
import {createMarketplacePublicCursor} from '../../scripts/marketplace-public-cursor.mjs';
import {createStagingMarketplaceBinding} from '../../scripts/staging-marketplace-context.mjs';
import {createStagingMarketplacePublicRepository} from '../../scripts/firebase-marketplace-repository.mjs';
import {createMarketplacePublicHttp} from '../../scripts/marketplace-public-http.mjs';
const failure=status=>({status,headers:{'Cache-Control':'private, no-store'},body:{ok:false,error:{code:status===404?'NOT_FOUND':'ENFORCEMENT_UNAVAILABLE'}}});
// Separate inactive public composition: no SDK/ADC initialization and no command
// or publication enablement. Rate/cursor ports MUST come from a trusted host,
// never request headers, IP claims or browser-provided identities.
export function createStagingMarketplacePublicRuntime({enabled=false,consumeRateLimit,readCursor,issueCursor,Filter,timeoutMs=5000,now=Date.now,...options}={}){
 const off=()=>Object.freeze({handle:async()=>failure(503)});
 if(enabled!==true||![consumeRateLimit,readCursor,issueCursor].every(f=>typeof f==='function'))return off();
 try{
  const binding=createStagingMarketplaceBinding(options);
  const repository=createStagingMarketplacePublicRepository({enabled:true,binding,Filter,readCursor,issueCursor,timeoutMs,now});
  const http=createMarketplacePublicHttp({enabled:true,repository,consumeRateLimit,timeoutMs,now});
  const paths={'/api/staging/marketplace/list':'list','/api/staging/marketplace/detail':'detail'};
  return Object.freeze({handle(path,request,context){
   return typeof path==='string'&&Object.hasOwn(paths,path)?http.handle(paths[path],request,context):Promise.resolve(failure(404));
  }});
 }catch{return off();}
}


// Trusted production-shaped dependencies, still inactive/source-only. No key
// generation, Auth/ADC initialization, cloud call or deployed flag changes.
export function createSecureStagingMarketplacePublicRuntime({enabled=false,guestPolicy,cursorKey,cursorTtlMs=60000,now=Date.now,...options}={}){
 if(enabled!==true)return createStagingMarketplacePublicRuntime();
 try{
  const binding=createStagingMarketplaceBinding(options);
  const quota=createStagingMarketplaceGuestRate({enabled:true,binding,policy:guestPolicy,now});
  const cursor=createMarketplacePublicCursor({key:cursorKey,ttlMs:cursorTtlMs,now});
  return createStagingMarketplacePublicRuntime({...options,enabled:true,now,
   consumeRateLimit:quota,readCursor:cursor.readCursor,issueCursor:cursor.issueCursor});
 }catch{return createStagingMarketplacePublicRuntime();}
}
