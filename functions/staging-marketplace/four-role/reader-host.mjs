import {createPublicKey} from 'node:crypto';
import {c2Crc32c} from '../../../scripts/c2-kms-request-signing.mjs';
import {createC2H2AGReaderSourcePorts,C2_H2AG_READER_EMAIL,C2_H2AG_READER_UID} from '../../../scripts/c2-h2ag-reader-metadata-source.mjs';
import {H2S_VERSION,H2S_VERSION_URL,H2S_PUBLIC_URL} from '../../../scripts/c2-h2-independent-kms-version-status.mjs';
import {requireC2H2LifecycleStageLedger} from '../../../scripts/c2-h2-lifecycle-stage-ledger.mjs';
import {requireFourRoleAuthority} from './contract.mjs';
import {requireFourRoleProtocol} from './protocol.mjs';
import {parseBoundedJson} from '../../../scripts/bounded-json.mjs';
export function createFourRoleReaderHost({enabled=false,authority,policy,ledger,protocol,fetchMetadata,fetchKms,now=Date.now}={}){
 const off=Object.freeze({ready:false,fetch:async()=>new Response(null,{status:503})});
 if(enabled!==true)return off;
 try{requireFourRoleAuthority(authority);requireC2H2LifecycleStageLedger(ledger,policy);
 requireFourRoleProtocol(protocol,{policyDigest:ledger.policyDigest,role:'reader'});}catch{return off;}
 if(typeof fetchMetadata!=='function'||typeof fetchKms!=='function')return off;
 return Object.freeze({ready:true,async fetch(request){
 try{
 const ctx=await protocol.receive(request,{fromRoles:['gateway','backend'],path:'/internal/key-status'});
 const operation=ctx.operation,usage=ctx.from==='gateway'?'sign':'verify';
 if(![usage+'-version',usage+'-public'].includes(operation))throw Error('ROLE_OPERATION');
 const parsed=parseBoundedJson(ctx.body,{maxBytes:1024}),input=parsed.value;
 const url=operation.endsWith('-version')?H2S_VERSION_URL:H2S_PUBLIC_URL;
 if(!parsed.ok||input.name!==H2S_VERSION||input.url!==url)throw Error('KEY');
 const ports=createC2H2AGReaderSourcePorts({enabled:true,now,fetchReader:fetchKms,
 metadataOptions:{readerEmail:C2_H2AG_READER_EMAIL,readerUid:C2_H2AG_READER_UID,
 readerImage:authority.configuration.roles.reader.image,fetchMetadata,
 // Source of this callback is branded signed authority + fresh cryptographically
 // verified OWN metadata ID JWT, never an arbitrary authorized:true value.
 verifyRuntimeBinding:async(_input,opts)=>protocol.ownRuntimeEvidence(opts)},
 verifyReaderAuthority:async(_input,opts)=>{
 const own=await protocol.ownRuntimeEvidence(opts);
 return {authorized:true,principal:own.principal,uid:own.uid,keyVersion:H2S_VERSION,expiresAtMs:own.expiresAtMs};
 },
 consumeDurableReadBudget:(_input,opts)=>ledger.consumeStatusRead({reservation:ctx.reservation,operation},opts)});
 if(!ports.ready)throw Error('PORTS');
 const value=await(operation.endsWith('-version')?ports.readExactVersion:ports.readExactPublicKey)(
 {name:H2S_VERSION,url,signal:request.signal});
 if(!value||value.name!==undefined&&value.name!==H2S_VERSION||
 value.algorithm!=='RSA_SIGN_PKCS1_2048_SHA256'||
 value.protectionLevel!==undefined&&value.protectionLevel!=='SOFTWARE')throw Error('KMS_RESPONSE');
 if(operation.endsWith('-version')){
 if(value.name!==H2S_VERSION||typeof value.state!=='string'||
 !['ENABLED','DISABLED','DESTROYED','DESTROY_SCHEDULED','PENDING_GENERATION','PENDING_IMPORT','IMPORT_FAILED'].includes(value.state))
 throw Error('KMS_RESPONSE');
 }else{
 if(typeof value.pem!=='string'||value.pem.length>8192||
 !value.pem.startsWith('-----BEGIN PUBLIC KEY-----\n')||!value.pem.trimEnd().endsWith('-----END PUBLIC KEY-----')||
 c2Crc32c(Buffer.from(value.pem))!==value.pemCrc32c)throw Error('KMS_RESPONSE');
 const key=createPublicKey(value.pem);if(key.type!=='public'||key.asymmetricKeyType!=='rsa'||
 key.asymmetricKeyDetails?.modulusLength!==2048||key.asymmetricKeyDetails?.publicExponent!==65537n)throw Error('KMS_RESPONSE');
 }
 // Public metadata only. Never include OAuth/access token, private keys, raw
 // provider headers, credentials or opaque KMS response extras.
 const keys=operation.endsWith('-version')?['name','state','algorithm','protectionLevel']:
 ['name','pem','pemCrc32c','algorithm','protectionLevel'];
 const result=Object.fromEntries(keys.filter(k=>Object.hasOwn(value,k)).map(k=>[k,value[k]]));
 return Response.json(result,{headers:{'cache-control':'no-store'}});
 }catch{return Response.json({ok:false,error:{code:'READER_DENIED'}},{status:503});}
 }});
}
