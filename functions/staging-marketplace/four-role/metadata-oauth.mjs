import {c2LifecycleBoundary} from '../../../scripts/c2-h2-lifecycle-boundary.mjs';
import {readBytes,requireFourRoleProtocol} from './protocol.mjs';
import {ROLES} from './contract.mjs';
const base='http://metadata.google.internal/computeMetadata/v1/instance/service-accounts/default/';
export function createOwnMetadataOAuth({protocol,fetchMetadata,now=Date.now}={}){
 requireFourRoleProtocol(protocol);
 return async({signal}={})=>c2LifecycleBoundary(async sig=>{
 const proof=await protocol.ownRuntimeEvidence({signal:sig});
 const read=async(path,max)=>{
 const url=base+path,response=await fetchMetadata(url,{method:'GET',headers:{'Metadata-Flavor':'Google'},
 redirect:'error',credentials:'omit',cache:'no-store',signal:sig});
 if(!(response instanceof Response)||response.status!==200||response.redirected||
 response.url&&response.url!==url||response.headers.get('Metadata-Flavor')!=='Google')throw Error('OWN_METADATA_UNAVAILABLE');
 return(new TextDecoder('utf-8',{fatal:true})).decode(await readBytes(response,max));
 };
 if((await read('email',320)).trim()!==ROLES[protocol.role].principal)throw Error('WRONG_ATTACHED_SA');
 const item=JSON.parse(await read('token',8192)),at=now();
 if(item.token_type!=='Bearer'||typeof item.access_token!=='string'||
 !/^[A-Za-z0-9._~+-]{40,4096}$/.test(item.access_token)||
 !Number.isSafeInteger(item.expires_in)||item.expires_in<10||item.expires_in>3600||
 proof.expiresAtMs<=at+1500)throw Error('OWN_METADATA_UNAVAILABLE');
 return Object.freeze({access_token:item.access_token,expires_in:Math.floor(
 (Math.min(at+item.expires_in*1000,proof.expiresAtMs)-at)/1000)});
 },{signal,timeoutMs:1500});
}
