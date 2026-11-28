import {H2S_VERSION} from '../../../scripts/c2-h2-independent-kms-version-status.mjs';
import {createOwnMetadataOAuth} from './metadata-oauth.mjs';
import {readBytes,requireFourRoleProtocol} from './protocol.mjs';
import {parseBoundedJson} from '../../../scripts/bounded-json.mjs';
// New multi-sign scope ONLY, after branded durable claim in existing signer.
// Does not invoke/recreate historical one-sign credential/transport factories.
export function createLifecycleKmsTransport({protocol,fetchMetadata,fetchKms,now=Date.now}={}){
 requireFourRoleProtocol(protocol,{role:'gateway'});
 const get=createOwnMetadataOAuth({protocol,fetchMetadata,now});
 return async(input,{signal,retry}={})=>{
 if(input?.name!==H2S_VERSION||retry!==false||typeof fetchKms!=='function')throw Error('KMS_SCOPE');
 const credential=await get({signal}),url='https://cloudkms.googleapis.com/v1/'+H2S_VERSION+':asymmetricSign';
 const response=await fetchKms(url,{method:'POST',headers:{Authorization:'Bearer '+credential.access_token,
 'content-type':'application/json'},body:JSON.stringify({digest:input.digest,digestCrc32c:input.digestCrc32c}),
 redirect:'error',credentials:'omit',cache:'no-store',signal});
 if(!(response instanceof Response)||response.status!==200||response.redirected||response.url&&response.url!==url)
 throw Error('KMS_OUTCOME_UNKNOWN');
 const data=parseBoundedJson(await readBytes(response,4096),{maxBytes:4096});
 if(!data.ok)throw Error('KMS_OUTCOME_UNKNOWN');
 return data.value; // Existing signer independently validates CRC + actual RSA.
 };
}
