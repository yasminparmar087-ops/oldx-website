import test from 'node:test';
import assert from 'node:assert/strict';
import {createServer} from 'node:http';
import {once} from 'node:events';
import {createC2WebsiteNodeHandler} from '../../functions/staging-marketplace/c2-website-node-http.mjs';

const website = 'https://mediator-stage.invalid';
const allowed = 'https://oldx-stage.invalid';
const injected = 'https://unapproved.invalid';

test('C2 G1: post-setup mutation cannot broaden the trusted Origin allowlist', async () => {
  const callerControlledConfig = [website, allowed];
  let dispatches = 0;
  const handler = createC2WebsiteNodeHandler({
    enabled: true,
    websiteOrigin: website,
    allowedOrigins: callerControlledConfig,
    mediator: {fetch: request => {
      dispatches++;
      return Response.json({ok: true}, {
        headers: {'access-control-allow-origin': request.headers.get('origin')}
      });
    }}
  });

  // This mutable array is deliberately changed *after* host construction.
  // Trust must be pinned to the original list, not to the caller's object.
  callerControlledConfig.push(injected);
  callerControlledConfig.splice(callerControlledConfig.indexOf(allowed), 1);

  const server = createServer(handler);
  server.listen(0, '127.0.0.1');
  await once(server, 'listening');
  const address = 'http://127.0.0.1:' + server.address().port;
  try {
    const rejected = await fetch(address + '/api/staging/marketplace/list', {
      method: 'POST',
      headers: {'origin': injected, 'content-type': 'application/json'},
      body: '{}'
    });
    assert.equal(rejected.status, 403);
    assert.equal(rejected.headers.get('access-control-allow-origin'), null);
    assert.equal(dispatches, 0);

    const stillApproved = await fetch(address + '/api/staging/marketplace/list', {
      method: 'POST',
      headers: {'origin': allowed, 'content-type': 'application/json'},
      body: '{}'
    });
    assert.equal(stillApproved.status, 200);
    assert.equal(stillApproved.headers.get('access-control-allow-origin'), allowed);
    assert.equal(dispatches, 1);
  } finally {
    server.closeAllConnections();
    await new Promise(resolve => server.close(resolve));
  }
});
