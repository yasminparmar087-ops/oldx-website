import {createProviderDiscoveryCursorCodec} from './provider-discovery-cursor.mjs';
import {STORE_CATEGORY_IDS} from '../features/stores/store-catalogue.mjs';
const purpose='oldx.marketplace.public.v1';
const exact=(v,keys)=>v&&Object.getPrototypeOf(v)===Object.prototype&&Object.keys(v).sort().join(',')===[...keys].sort().join(',');
const id=v=>typeof v==='string'&&/^[A-Za-z0-9_-]{1,100}$/.test(v);
function validState(s){
 if(!exact(s,['scope','publicationEpoch','after'])||!Number.isSafeInteger(s.publicationEpoch)||s.publicationEpoch<0||!id(s.after)||typeof s.scope!=='string'||s.scope.length>400)return false;
 try{const a=JSON.parse(s.scope);return Array.isArray(a)&&a.length===5&&a[0]==='market-v1'&&['product','store'].includes(a[1])&&Number.isInteger(a[2])&&a[2]>=1&&a[2]<=24&&(a[3]===''||STORE_CATEGORY_IDS.includes(a[3]))&&(a[4]===null||a[1]==='product'&&id(a[4]))&&JSON.stringify(a)===s.scope;}catch{return false;}
}
// Reuse constant-time HMAC verification/TTL codec with an exact purpose and
// public-only canonical state. Repository ALSO checks scope/current generation.
export function createMarketplacePublicCursor({key,now=Date.now,ttlMs=60000}={}){
 const clock=()=>{const n=now();if(!Number.isSafeInteger(n)||n<0)throw Error('Cursor clock unavailable');return n;};
 const codec=createProviderDiscoveryCursorCodec({key,now:clock,ttlMs});
 return Object.freeze({
  issueCursor(state){if(!validState(state))throw Error('Cursor state unavailable');return codec.issueCursor({purpose,...state});},
  readCursor(token,expected){
   try{
    const value=codec.readCursor(token);
    if(!exact(value,['purpose','scope','publicationEpoch','after'])||value.purpose!==purpose)return null;
    const {purpose:ignored,...state}=value;
    if(!validState(state)||expected&&(expected.scope!==state.scope||expected.publicationEpoch!==state.publicationEpoch))return null;
    return state;
   }catch{return null;}
  }
 });
}

