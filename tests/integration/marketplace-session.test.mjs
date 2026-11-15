import test from 'node:test';import assert from 'node:assert/strict';import {createMarketplaceSessionIntegration,providerSessionBinding} from '../../features/marketplace/session-integration.mjs';import {createProviderJourneyIntegration} from '../../features/service-providers/enquiry-integration.mjs';
test('same verified session reaches existing Product/Store/Provider ports; logout cancels private scope',async()=>{const values=[],provider=createProviderJourneyIntegration({enabled:false});const session=createMarketplaceSessionIntegration({enabled:true,bindings:[{setSession:v=>values.push(v)},providerSessionBinding(provider)]});assert.equal(await session.setSession({uid:'owner',sessionId:'opaque'}),true);assert.deepEqual(values[0],{uid:'owner',sessionId:'opaque'});await session.logout();assert.equal(values.at(-1),null);assert.equal(session.snapshot(),null);});
test('unavailable lifecycle enforcement clears every binding and never forwards token/role fields',async()=>{const seen=[];const model=createMarketplaceSessionIntegration({enabled:true,bindings:[{setSession:v=>seen.push(v)},{setSession:v=>{if(v)throw new Error('private failure');}}]});assert.equal(await model.setSession({uid:'owner',sessionId:'opaque',token:'must-not-pass',role:'admin'}),false);assert.deepEqual(seen[0],{uid:'owner',sessionId:'opaque'});assert.equal(seen.at(-1),null);assert.equal(await createMarketplaceSessionIntegration().setSession({uid:'a',sessionId:'b'}),false);});

test('stale asynchronous sign-in cannot reactivate private views after a logout',async()=>{
 let release,started;const gate=new Promise(resolve=>release=resolve),began=new Promise(resolve=>started=resolve);
 const calls=[],scopeChanges=[];const binding={
  setSession:value=>{calls.push(value?.uid??null);if(value?.uid==='first'){started();return gate;}},
  changeScope:()=>scopeChanges.push('cancel'),
 };
 const model=createMarketplaceSessionIntegration({enabled:true,bindings:[binding]});
 const first=model.setSession({uid:'first',sessionId:'a'});
 await began;
 const superseded=model.setSession({uid:'second',sessionId:'b'});
 const logout=model.logout();
 assert.equal(model.snapshot(),null);
 release();
 assert.equal(await first,false);
 assert.equal(await superseded,false);
 assert.equal(await logout,true);
 assert.deepEqual(calls,['first',null]);
 assert.ok(scopeChanges.length>=3);
 assert.equal(model.snapshot(),null);
});

test('newest verified session wins even when the old async port resolves last',async()=>{
 let release,started;
 const gate=new Promise(resolve=>release=resolve),began=new Promise(resolve=>started=resolve);
 const calls=[];
 const model=createMarketplaceSessionIntegration({enabled:true,bindings:[{
  setSession:value=>{calls.push(value?.uid??null);if(value?.uid==='first'){started();return gate;}},
  changeScope(){},
 }]});
 const first=model.setSession({uid:'first',sessionId:'old',token:'never-forward'});
 await began;
 const newer=model.setSession({uid:'second',sessionId:'new',role:'never-forward'});
 assert.equal(model.snapshot(),null);
 release();
 assert.equal(await first,false);
 assert.equal(await newer,true);
 assert.deepEqual(calls,['first','second']);
 assert.deepEqual(model.snapshot(),{uid:'second',sessionId:'new'});
 await model.logout();
 assert.equal(model.snapshot(),null);
 assert.deepEqual(calls,['first','second',null]);
});

test('invalid latest session cancels pending private lifecycle and ignores extra role data',async()=>{
 let release,started;
 const gate=new Promise(resolve=>release=resolve),began=new Promise(resolve=>started=resolve);
 const seen=[];
 const model=createMarketplaceSessionIntegration({enabled:true,bindings:[{
  setSession:value=>{seen.push(value);if(value?.uid==='first'){started();return gate;}},
  changeScope(){},
 }]});
 const first=model.setSession({uid:'first',sessionId:'a',secret:'never-forward'});
 await began;
 const invalid=model.setSession({uid:'malformed/uid',sessionId:'b'});
 release();
 assert.equal(await first,false);
 assert.equal(await invalid,false);
 assert.deepEqual(seen,[{uid:'first',sessionId:'a'},null]);
 assert.equal(model.snapshot(),null);
});
