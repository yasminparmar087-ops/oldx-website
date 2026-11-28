import {requireFourRoleProtocol} from './protocol.mjs';
import {createOwnMetadataOAuth} from './metadata-oauth.mjs';
import {createStagingMarketplaceMedia} from '../../../scripts/staging-marketplace-media.mjs';
import {c2LifecycleBoundary} from '../../../scripts/c2-h2-lifecycle-boundary.mjs';
import {sha} from './contract.mjs';
export async function loadFirebaseNativeSdk(role){
 const [app,auth]=await Promise.all([import('firebase-admin/app'),import('firebase-admin/auth')]);
 if(role==='mediator')return {...app,...auth};
 const [firestore,storage,google]=await Promise.all([
 import('@google-cloud/firestore'),import('@google-cloud/storage'),import('google-auth-library')]);
 return {...app,...auth,Firestore:firestore.Firestore,FieldValue:firestore.FieldValue,
 Storage:storage.Storage,GoogleAuth:google.GoogleAuth,Compute:google.Compute};
}
// Admin Firestore rejects custom Auth credentials. Use the real native
// Firestore client with an EXPLICIT Compute-only GoogleAuth, not a fake Admin
// wrapper, applicationDefault file search, impersonation or downloaded SA key.
export async function createFirebaseNativeBindings({protocol,fetchMetadata,
 sdkLoader=loadFirebaseNativeSdk,now=Date.now}={}){
 requireFourRoleProtocol(protocol);
 if(!['mediator','backend'].includes(protocol.role))throw Error('FIREBASE_ROLE');
 await protocol.ownRuntimeEvidence();
 const sdk=await sdkLoader(protocol.role),getAccessToken=createOwnMetadataOAuth({protocol,fetchMetadata,now});
 const app=sdk.initializeApp({projectId:'oldx-staging',credential:{getAccessToken}},'oldx-h2ah-'+protocol.role);
 const adminAuth=sdk.getAuth(app);
 if(protocol.role==='mediator')return Object.freeze({adminAuth,close:()=>sdk.deleteApp(app)});
 const auth=new sdk.GoogleAuth({authClient:new sdk.Compute({serviceAccountEmail:'default'})});
 const db=new sdk.Firestore({projectId:'oldx-staging',databaseId:'(default)',auth,
 preferRest:true,maxIdleChannels:0});
 if(db.projectId!=='oldx-staging'||db.databaseId!=='(default)')throw Error('WRONG_NATIVE_DATABASE');
 const storage=new sdk.Storage({projectId:'oldx-staging',authClient:auth,retryOptions:{autoRetry:false,maxRetries:0}});
 const manifest=protocol.authority.configuration.media;
 // Read exactly ONE independently approved, immutable Storage generation.
 // No upload/delete/provider migration; absent provider manifest remains OFF.
 const readApprovedDerivative=async(input,{signal}={})=>{
 if(!manifest||manifest.provider!=='firebase-storage'||input?.derivativeId!==manifest.derivativeId||
 input.version!==manifest.version||!Number.isSafeInteger(input.maxBytes)||input.maxBytes>3145728||
 !/^[a-z0-9][a-z0-9._-]{2,220}$/.test(manifest.bucket??'')||
 !/^[A-Za-z0-9_/-]{1,240}\.(webp|jpg|png)$/.test(manifest.object??'')||
 !/^[1-9][0-9]{0,19}$/.test(manifest.generation??''))return null;
 return c2LifecycleBoundary(async sig=>{
 const file=storage.bucket(manifest.bucket).file(manifest.object,{generation:manifest.generation});
 const stream=file.createReadStream({validation:'crc32c',decompress:false}),parts=[];let length=0;
 const abort=()=>stream.destroy(Error('STOP'));sig.addEventListener('abort',abort,{once:true});
 try{for await(const part of stream){length+=part.length;if(length>input.maxBytes)throw Error('SIZE');parts.push(part);}}
 finally{sig.removeEventListener('abort',abort);stream.destroy();}
 const bytes=Buffer.concat(parts);
 if(sha(bytes)!==manifest.sha256)return null;
 return {derivativeId:input.derivativeId,version:input.version,contentType:manifest.contentType,bytes};
 },{signal,timeoutMs:3000});
 };
 return Object.freeze({adminAuth,adminFirestore:db,FieldValue:sdk.FieldValue,
 createMediaBindings:binding=>createStagingMarketplaceMedia({enabled:true,binding,readApprovedDerivative,now}),
 close:async()=>{await db.terminate();await sdk.deleteApp(app);}});
}
