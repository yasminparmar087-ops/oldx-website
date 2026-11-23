import test from 'node:test';
import assert from 'node:assert/strict';
import {createMarketplacePublicCursor} from '../../scripts/marketplace-public-cursor.mjs';
import {createProviderDiscoveryCursorCodec} from '../../scripts/provider-discovery-cursor.mjs';
import {createIsolatedMarketplaceRepository,MARKETPLACE_TEST_SCHEMA as c} from '../../scripts/firebase-marketplace-repository.mjs';
import {fakeFirestoreSdk} from './fake-firestore-sdk.mjs';
const key=new Uint8Array(32).fill(23),scope=JSON.stringify(['market-v1','product',1,'cars',null]);
const state={scope,publicationEpoch:2,after:'a'};
test('bounded signed public state validates purpose/scope/generation and copies injected key',()=>{
 let time=100000;const mutable=new Uint8Array(key),codec=createMarketplacePublicCursor({key:mutable,now:()=>time,ttlMs:1000});
 mutable.fill(0);const token=codec.issueCursor(state);
 assert.ok(token.length<=1024);assert.deepEqual(codec.readCursor(token,{scope,publicationEpoch:2}),state);
 assert.equal(createMarketplacePublicCursor({key,now:()=>time,ttlMs:1000}).readCursor(token)?.after,'a');
 for(const expected of [{scope:JSON.stringify(['market-v1','product',2,'cars',null]),publicationEpoch:2},{scope,publicationEpoch:3}])assert.equal(codec.readCursor(token,expected),null);
 time=101000;assert.equal(codec.readCursor(token),null);time=99999;assert.equal(codec.readCursor(token),null);
});
test('tampering, wrong key/purpose, malformed tokens and sensitive/invalid payloads are rejected',()=>{
 const codec=createMarketplacePublicCursor({key,now:()=>100000});
 const token=codec.issueCursor(state);
 for(const v of [token+'x',token.slice(0,-5)+'abcde','x'.repeat(1025),'a.b','',null])assert.equal(codec.readCursor(v),null);
 assert.equal(createMarketplacePublicCursor({key:new Uint8Array(32).fill(99),now:()=>100000}).readCursor(token),null);
 const foreign=createProviderDiscoveryCursorCodec({key,now:()=>100000}).issueCursor({purpose:'other',...state});assert.equal(codec.readCursor(foreign),null);
 for(const bad of [{...state,ownerUid:'private'},{...state,publicationEpoch:-1},{...state,after:'../secret'},{...state,scope:'["market-v1","product",25,"cars",null]'},{...state,scope:'["market-v1","store",1,"cars","private"]'}])assert.throws(()=>codec.issueCursor(bad));
 assert.throws(()=>createMarketplacePublicCursor({key:new Uint8Array(8)}));
 assert.throws(()=>createMarketplacePublicCursor({key,now:()=>NaN}).issueCursor(state));
});
test('actual repository pagination rejects stale publication generation and cross-scope replay',async()=>{
 const f=fakeFirestoreSdk(),codec=createMarketplacePublicCursor({key,now:()=>100000});
 f.seed(c.actors,'seller',{uid:'seller',canWrite:true,suspended:false});f.seed(c.generations,'current',{value:2});
 for(const id of ['a','b']){
  const row={id,kind:'product',revision:1,title:'ગુજરાતી हिन्दी',description:'Synthetic',category:'cars',locationLabel:'Sample',basePrice:1,isSold:false,storeId:null};
  f.seed(c.publicViews,'product_'+id,row);f.seed(c.privateRecords,'product_'+id,{id,kind:'product',ownerUid:'seller',published:true,publicationRevision:1,publicProfile:row});
 }
 const repo=createIsolatedMarketplaceRepository({enabled:true,firestore:f.db,sdk:f.sdk,schema:c,...codec});
 const input={kind:'product',limit:1,category:'cars',storeId:null,cursor:null};
 const first=await repo.list(input);assert.equal(first.ok,true);assert.ok(first.nextCursor);
 assert.equal((await repo.list({...input,cursor:first.nextCursor})).items[0].id,'b');
 assert.equal((await repo.list({...input,category:'',cursor:first.nextCursor})).code,'CURSOR_INVALID');
 f.seed(c.generations,'current',{value:3});assert.equal((await repo.list({...input,cursor:first.nextCursor})).code,'CURSOR_INVALID');
});

