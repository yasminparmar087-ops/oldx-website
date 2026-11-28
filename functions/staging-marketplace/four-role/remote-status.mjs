import {H2S_VERSION,H2S_VERSION_URL,H2S_PUBLIC_URL,H2S_ALGORITHM,H2S_SPKI_SHA256,
 c2H2VersionMetadataMatches,c2H2PublicKeyMatches} from '../../../scripts/c2-h2-independent-kms-version-status.mjs';
import {requireFourRoleProtocol} from './protocol.mjs';
export function createRemoteReaderStatus({protocol,getStageContext}={}){
 requireFourRoleProtocol(protocol);
 return async({name,signal}={})=>{
 if(name!==H2S_VERSION)throw Error('H2AH_WRONG_KEY');
 const ctx=getStageContext(),usage=protocol.role==='gateway'?'sign':protocol.role==='backend'?'verify':null;
 if(!usage||!ctx?.reservation)throw Error('H2AH_NO_STAGE');
 const read=async(kind,url)=>{
 const response=await protocol.send('reader','/internal/key-status',Buffer.from(JSON.stringify({name,url})),
 {operation:usage+'-'+kind,reservation:ctx.reservation,phase:ctx.phase,signal});
 if(response.status!==200)throw Error('H2AH_READER_UNAVAILABLE');return response.json();
 };
 const version=await read('version',H2S_VERSION_URL);
 if(!c2H2VersionMetadataMatches(version))throw Error('H2AH_KEY_STATUS_UNVERIFIED');
 const pub=await read('public',H2S_PUBLIC_URL);
 if(!c2H2PublicKeyMatches(pub))throw Error('H2AH_PIN_UNVERIFIED');
 return Object.freeze({name,state:'ENABLED',algorithm:H2S_ALGORITHM,publicKeySha256:H2S_SPKI_SHA256});
 };
}
