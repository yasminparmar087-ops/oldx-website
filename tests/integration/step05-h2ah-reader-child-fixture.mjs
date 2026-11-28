import {c2Crc32c} from '../../scripts/c2-kms-request-signing.mjs';
// LOCAL TEST DOUBLE ONLY. No real Google/Firebase/KMS transport or credentials.
import {createPrivateKey,sign} from 'node:crypto';
import {createFourRoleAuthority,ROLES} from '../../functions/staging-marketplace/four-role/contract.mjs';
import {createFourRoleProtocol} from '../../functions/staging-marketplace/four-role/protocol.mjs';
import {createC2H2MultiSignLifecyclePolicy} from '../../scripts/c2-h2-lifecycle-signing-status-contract.mjs';
import {createC2H2RemoteLifecycleStageLedger} from '../../scripts/c2-h2-lifecycle-stage-ledger.mjs';
import {createFourRoleReaderHost} from '../../functions/staging-marketplace/four-role/reader-host.mjs';
import {createFourRoleServer} from '../../functions/staging-marketplace/four-role/server.mjs';
let server,calls=0,mode='normal';
process.on('message',async message=>{
 if(message.type==='counts'){process.send({type:'counts',calls,pid:process.pid});return;}
 if(message.type==='mode'){mode=message.mode;process.send({type:'mode'});return;}
 if(message.type==='stop'){server?.closeAllConnections();server?.close(()=>process.disconnect());return;}
 if(message.type!=='start')return;
 try{
 const c=message.configuration,now=()=>c.clock,key=createPrivateKey(c.googlePrivateKeyPem);
 const authority=createFourRoleAuthority({...c.authority,enabled:true,now});
 const policy=createC2H2MultiSignLifecyclePolicy({enabled:true,proposal:c.proposal,mode:'bounded-per-request-multisign-v1',maxSignAttempts:6});
 const jwt=aud=>{const enc=x=>Buffer.from(JSON.stringify(x)).toString('base64url');
 const data=enc({alg:'RS256',kid:'four-role-google'})+'.'+enc({iss:'https://accounts.google.com',aud,
 sub:c.readerUid??ROLES.reader.uid,email:ROLES.reader.principal,email_verified:true,iat:c.clock/1000,exp:c.clock/1000+3600});
 return data+'.'+sign('RSA-SHA256',Buffer.from(data),key).toString('base64url');};
 const fetchMetadata=async url=>{
 if(mode==='missing-token'&&url.endsWith('/token'))return new Response('{}',{headers:{'Metadata-Flavor':'Google'}});
 const body=url.endsWith('/email')?ROLES.reader.principal:url.endsWith('/token')?
 JSON.stringify({access_token:'local-test-reader-'+'a'.repeat(80),token_type:'Bearer',expires_in:300}):
 jwt(new URL(url).searchParams.get('audience'));
 return new Response(body,{headers:{'Metadata-Flavor':'Google'}});
 };
 const protocol=createFourRoleProtocol({enabled:true,authority,role:'reader',now,fetchMetadata,
 fetchGoogleKeys:async()=>Response.json({keys:[c.googleJwk]},{headers:{'cache-control':'max-age=300'}}),
 fetchPrivate:async(url,init)=>{
 const response=await fetch(c.backendAddress+new URL(url).pathname,init);
 return new Response(await response.arrayBuffer(),{status:response.status,headers:response.headers});
 }});
 const ledger=createC2H2RemoteLifecycleStageLedger({enabled:true,policy,protocol});
 const reader=createFourRoleReaderHost({enabled:true,authority,policy,ledger,protocol,fetchMetadata,now,
 fetchKms:async url=>{
 calls++;if(mode==='ambiguous')throw Error('SIMULATED_NETWORK_OUTCOME_UNKNOWN');
 if(mode==='malformed')return Response.json({name:'wrong-key',state:'ENABLED'});
 const data=url.endsWith('/publicKey')?mode==='private-pem'?{...c.publicValue,pem:c.googlePrivateKeyPem,
 pemCrc32c:c2Crc32c(Buffer.from(c.googlePrivateKeyPem))}:c.publicValue:c.versionValue;
 return Response.json({...data,access_token:'MUST_NEVER_LEAK',privateKey:'MUST_NEVER_LEAK'});
 }});
 server=createFourRoleServer({role:'reader',runtime:{...reader,origin:authority.configuration.roles.reader.origin}});
 server.listen(0,'127.0.0.1');await new Promise(r=>server.once('listening',r));
 process.send({type:'ready',port:server.address().port,pid:process.pid});
 }catch{process.send({type:'failed'});}
});
