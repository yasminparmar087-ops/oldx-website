import {readFile} from 'node:fs/promises';
import {createFourRoleAuthority,requireFourRoleAuthority,ROLES,sha} from './contract.mjs';
import {createFourRoleRuntime} from './bindings.mjs';
import {H2S_VERSION_URL,H2S_PUBLIC_URL} from '../../../scripts/c2-h2-independent-kms-version-status.mjs';
const off=()=>({ready:false,fetch:async()=>new Response(null,{status:503}),close:async()=>{}});
const fixed='/run/oldx/';
export async function bootstrapFourRole(role,{env=process.env,read=readFile,transport=globalThis.fetch}={}){
 if(env.OLDX_H2AH_ENABLED!=='true')return off();
 try{
 if(!ROLES[role]||['GOOGLE_APPLICATION_CREDENTIALS','CLOUDSDK_AUTH_CREDENTIAL_FILE_OVERRIDE',
 'FIRESTORE_EMULATOR_HOST','FIREBASE_AUTH_EMULATOR_HOST','STORAGE_EMULATOR_HOST',
 'HTTP_PROXY','HTTPS_PROXY','ALL_PROXY'].some(k=>env[k])||
 env.GCE_METADATA_HOST&&env.GCE_METADATA_HOST!=='metadata.google.internal'||
 env.GCE_METADATA_ROOT||env.GCE_METADATA_IP)throw Error('UNTRUSTED_ENV');
 const [raw,pin,provenanceRaw]=await Promise.all([
 read(fixed+'config/runtime.json','utf8'),read(fixed+'trust/controller-spki.sha256','utf8'),
 read(new URL('../../../deployment/four-role/source-provenance.json',import.meta.url),'utf8')]);
 if(raw.length>131072||pin.length>80||provenanceRaw.length>65536)throw Error('SIZE');
 const config=JSON.parse(raw),provenance=JSON.parse(provenanceRaw);
 const authority=createFourRoleAuthority({enabled:true,configuration:config.configuration,envelope:config.envelope,
 controllerPublicKeyPem:config.controllerPublicKeyPem,controllerSpkiSha256:pin.trim()});
 if(!authority||provenance.sourceRevision!==authority.configuration.sourceRevision||
 provenance.role!==role||env.K_REVISION!==authority.configuration.roles[role].revision)throw Error('PROVENANCE');
 const files=provenance.files;
 if(!files||Object.keys(files).length<10||!files['functions/staging-marketplace/four-role/'+role+'.mjs'])
 throw Error('SOURCE_MANIFEST');
 for(const [path,digest]of Object.entries(files)){
 if(!/^(?:(?:functions|features|scripts)\/[A-Za-z0-9_./-]+\.mjs|package(?:-lock)?\.json)$/.test(path)||
 path.includes('..')||!/^[a-f0-9]{64}$/.test(digest)||
 sha(await read(new URL('../../../'+path,import.meta.url)))!==digest)throw Error('SOURCE_HASH');
 }
 const facts=authority.configuration.roles;
 const metadataBase='http://metadata.google.internal/computeMetadata/v1/instance/service-accounts/default/';
 const fetchMetadata=(url,init)=>{
 const u=new URL(url);
 if(!url.startsWith(metadataBase)||!['email','token','identity'].includes(u.pathname.split('/').at(-1))||
 init?.method!=='GET')throw Error('METADATA_SCOPE');
 return transport(url,{...init,redirect:'error',credentials:'omit'});
 };
 const fetchGoogleKeys=(url,init)=>{
 if(url!=='https://www.googleapis.com/oauth2/v3/certs'||init?.method!=='GET')throw Error('JWKS_SCOPE');
 return transport(url,{...init,redirect:'error',credentials:'omit'});
 };
 const fetchPrivate=(url,init)=>{
 requireFourRoleAuthority(authority);
 if(!Object.values(facts).some(r=>r.origin===new URL(url).origin)||init?.method!=='POST')throw Error('PRIVATE_SCOPE');
 return transport(url,{...init,redirect:'error',credentials:'omit'});
 };
 const fetchKms=(url,init)=>{
 requireFourRoleAuthority(authority);
 const allowed=role==='reader'&&init?.method==='GET'&&[H2S_VERSION_URL,H2S_PUBLIC_URL].includes(url)||
 role==='gateway'&&init?.method==='POST'&&url===H2S_VERSION_URL+':asymmetricSign';
 if(!allowed)throw Error('KMS_ROLE_SCOPE');return transport(url,{...init,redirect:'error',credentials:'omit'});
 };
 const cursorKey=role==='backend'?new Uint8Array(await read(fixed+'cursor/cursor-key')):undefined;
 return await createFourRoleRuntime({enabled:true,role,authority,configuration:config,
 fetchMetadata,fetchGoogleKeys,fetchPrivate,fetchKms,cursorKey});
 }catch{return off();} // No secret/error/body/config logging; absent real proof stays OFF.
}
