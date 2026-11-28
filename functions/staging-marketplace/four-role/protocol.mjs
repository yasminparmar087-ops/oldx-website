import {createC2CloudRunMetadataIdentity} from '../../../scripts/c2-cloud-run-metadata-identity.mjs';
import {createGoogleGatewayPublicKeyResolver} from '../../../scripts/google-gateway-public-keys.mjs';
import {createGatewayAttestationVerifier,GATEWAY_ATTESTATION_HEADER} from '../../../scripts/gateway-attestation.mjs';
import {c2LifecycleBoundary} from '../../../scripts/c2-h2-lifecycle-boundary.mjs';
import {parseBoundedJson} from '../../../scripts/bounded-json.mjs';
import {ROLES,canonical,sha,requireFourRoleAuthority} from './contract.mjs';
export const CONTEXT='x-oldx-h2ah-context',ASSERTION='x-oldx-h2ah-assertion';
const clients=new WeakMap(),verified=new WeakSet();
const deny=()=>{throw Error('H2AH_PRIVATE_RPC_DENIED');};
export async function readBytes(response,limit=32768){
 if(!response.body)return Buffer.alloc(0);const reader=response.body.getReader(),parts=[];let length=0;
 try{for(;;){const {done,value}=await reader.read();if(done)break;length+=value.byteLength;
 if(length>limit)deny();parts.push(value);}}finally{void reader.cancel().catch(()=>{});}
 return Buffer.concat(parts);
}
const contextAudience=c=>'urn:oldx:h2ah:context:'+sha(canonical(c));
export function requireVerifiedFourRoleContext(value){
 if(!verified.has(value))deny();return value;
}
// Separate FULL Google-signed assertion binds every context byte through its
// signed audience. A stripped IAM token/header is NEVER authentication proof.
// IAM/recognized-internal routing remain independently enforced by Cloud Run.
export function createFourRoleProtocol({enabled=false,authority,role,fetchMetadata,
 fetchGoogleKeys,fetchPrivate,now=Date.now}={}){
 if(enabled!==true)return null;
 try{requireFourRoleAuthority(authority);}catch{return null;}
 if(!ROLES[role]||[fetchMetadata,fetchGoogleKeys,fetchPrivate,now].some(x=>typeof x!=='function'))return null;
 const facts=authority.configuration.roles;
 const resolver=createGoogleGatewayPublicKeyResolver({enabled:true,issuer:'https://accounts.google.com',fetchRequest:fetchGoogleKeys,now});
 const verify=async(token,from,audience,iamAudience,signal)=>{
 const verifier=createGatewayAttestationVerifier({enabled:true,identityType:'google-service-account',
 issuer:'https://accounts.google.com',expectedPrincipal:ROLES[from].principal,expectedSubject:ROLES[from].uid,
 attestationAudience:audience,iamAudience,resolvePublicKey:resolver,now});
 if(!verifier)return null;
 return verifier(new Request(iamAudience,{headers:{[GATEWAY_ATTESTATION_HEADER]:token}}),{audience:iamAudience,signal});
 };
 const result=Object.freeze({role,authority,
 async ownRuntimeEvidence({signal}={}){
 requireFourRoleAuthority(authority);
 const audience='urn:oldx:h2ah:boot:'+sha(canonical(facts[role]));
 const identity=createC2CloudRunMetadataIdentity({enabled:true,serviceAccount:ROLES[role].principal,
 expectedSubject:ROLES[role].uid,invokerAudience:facts[role].origin,assertionAudience:audience,fetchMetadata,now});
 const token=await identity.getWebsiteAttestation({audience,signal});
 if(!(await verify(token.token,role,audience,facts[role].origin,signal))?.verified)deny();
 return Object.freeze({principal:ROLES[role].principal,uid:ROLES[role].uid,image:facts[role].image,
 expiresAtMs:Math.min(authority.configuration.expiresAtMs,token.expiresAtMs)});
 },
 async send(to,path,bytes,{operation,reservation,phase='',headers={},signal}={}){
 requireFourRoleAuthority(authority);
 if(!ROLES[to]||!(bytes instanceof Uint8Array)||bytes.byteLength>32768||
 !/^\/(?:internal\/(?:ledger|key-status)|api\/staging\/marketplace\/(?:save|owner|archive|list|detail))$/.test(path)||
 !/^[a-f0-9]{64}$/.test(reservation??'')||typeof operation!=='string'||operation.length>80)deny();
 const snapshot=Buffer.from(bytes),outHeaders=new Headers(headers);
 return c2LifecycleBoundary(async sig=>{
 const at=now(),ctx={v:1,purpose:'oldx.h2ah.stage-request.v1',from:role,to,path,operation,phase,
 policyDigest:authority.configuration.policyDigest,reservation,bodySha256:sha(snapshot),issuedAtMs:at,expiresAtMs:at+15000};
 const audience=contextAudience(ctx),identity=createC2CloudRunMetadataIdentity({enabled:true,
 serviceAccount:ROLES[role].principal,expectedSubject:ROLES[role].uid,
 invokerAudience:facts[to].origin,assertionAudience:audience,fetchMetadata,now});
 const iam=await identity.getInvokerCredential({audience:facts[to].origin,signal:sig});
 const assertion=await identity.getWebsiteAttestation({audience,signal:sig});
 const h=new Headers(outHeaders);h.delete('cookie');h.delete('host');h.set('content-type','application/json');
 h.set('x-serverless-authorization','Bearer '+iam.token);h.set(CONTEXT,Buffer.from(canonical(ctx)).toString('base64url'));
 h.set(ASSERTION,assertion.token);
 const url=facts[to].origin+path;
 const response=await fetchPrivate(url,{method:'POST',body:snapshot,headers:h,redirect:'error',
 credentials:'omit',cache:'no-store',signal:sig});
 if(!(response instanceof Response)||response.redirected||response.url&&response.url!==url)deny();
 const body=await readBytes(response);
 requireFourRoleAuthority(authority);
 // Materialize inside deadline before cancellation; no response stream escapes.
 return new Response(body,{status:response.status,headers:response.headers});
 },{signal,timeoutMs:5000});
 },
 async receive(request,{fromRoles,path}={}){
 requireFourRoleAuthority(authority);
 if(!(request instanceof Request)||request.method!=='POST'||new URL(request.url).origin!==facts[role].origin||
 new URL(request.url).pathname!==path||new URL(request.url).search||request.headers.has('cookie'))deny();
 const iam=request.headers.get('x-serverless-authorization');
 if(typeof iam!=='string'||!/^Bearer [A-Za-z0-9_.-]{1,8192}$/.test(iam))deny(); // Presence only; never proof.
 const encoded=request.headers.get(CONTEXT),assertion=request.headers.get(ASSERTION);
 if(typeof encoded!=='string'||encoded.length>8192||typeof assertion!=='string'||assertion.length>8192)deny();
 const raw=Buffer.from(encoded,'base64url');if(raw.toString('base64url')!==encoded)deny();
 const parsed=parseBoundedJson(raw,{maxBytes:6144});if(!parsed.ok||canonical(parsed.value)!==raw.toString('utf8'))deny();
 const ctx=parsed.value,at=now();
 if(ctx.v!==1||ctx.purpose!=='oldx.h2ah.stage-request.v1'||ctx.to!==role||
 !fromRoles?.includes(ctx.from)||!ROLES[ctx.from]||ctx.path!==path||
 ctx.policyDigest!==authority.configuration.policyDigest||!/^[a-f0-9]{64}$/.test(ctx.reservation??'')||
 !Number.isSafeInteger(ctx.issuedAtMs)||!Number.isSafeInteger(ctx.expiresAtMs)||
 ctx.issuedAtMs>at+1000||at-ctx.issuedAtMs>15000||ctx.expiresAtMs<=at||
 ctx.expiresAtMs-ctx.issuedAtMs>15000||ctx.expiresAtMs<=ctx.issuedAtMs)deny();
 const body=await readBytes(request,32768);
 if(sha(body)!==ctx.bodySha256)deny();
 const proof=await verify(assertion,ctx.from,contextAudience(ctx),facts[role].origin,request.signal);
 if(proof?.verified!==true||!authority.fresh())deny();
 const value=Object.freeze({...ctx,body,principal:ROLES[ctx.from].principal,uid:ROLES[ctx.from].uid});
 verified.add(value);return value;
 }});
 clients.set(result,{policyDigest:authority.configuration.policyDigest,role});return result;
}
export function requireFourRoleProtocol(value,{policyDigest,role}={}){
 const pin=clients.get(value);
 if(!pin||policyDigest!==undefined&&pin.policyDigest!==policyDigest||role!==undefined&&pin.role!==role)deny();return value;
}
