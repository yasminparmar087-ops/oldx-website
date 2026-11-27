// H2U OFF-ONLY Cloud Run entrypoint — DO NOT DEPLOY WITHOUT NEW OWNER APPROVAL.
// Launching the local process requires an explicit PORT; it never enables
// Product publication, KMS signing, Firestore writes or Firebase access.
import {createC2H2GatewayHostSource} from
  '../functions/staging-marketplace/c2-h2-gateway-host-source.mjs';
import {createC2H2UPrivateOffHttpServer,parseC2H2UCloudRunPort} from
  '../functions/staging-marketplace/c2-h2u-private-off-http.mjs';

if(process.env.OLDX_H2U_MODE!==undefined&&
   process.env.OLDX_H2U_MODE!=='OFF'){
  throw Error('H2U_SERVER_MUST_REMAIN_OFF');
}
// Existing H2S Gateway source factory must remain non-ready with no providers.
// It does not create a listener or make a Cloud request on construction.
const h2s=createC2H2GatewayHostSource();
if(h2s.ready!==false)throw Error('H2U_GATEWAY_FACTORY_UNEXPECTEDLY_READY');

const port=parseC2H2UCloudRunPort(process.env.PORT);
const server=createC2H2UPrivateOffHttpServer();
server.on('error',()=>{
  // Never dump environment, credentials or request headers to logs.
  process.stderr.write('H2U_OFF_SERVER_STARTUP_FAILURE\n');
  process.exitCode=1;
});
server.listen(port,'0.0.0.0',()=>{
  process.stdout.write('H2U_OFF_ONLY_LISTENING=TRUE\n');
});
process.on('SIGTERM',()=>{
  server.close(()=>{process.exitCode=0;});
});
