// Source-only host adapter for a FUTURE separately approved Cloud Run service.
// Inert by default, no network/environment/credentials at import time.
// This consumes Google metadata-server identity responses only when an explicitly
// enabled trusted host injects its own server-side fetch. Never expose to browser.
const METADATA = 'http://metadata.google.internal/computeMetadata/v1/instance/service-accounts/default/identity';
const principal = value => typeof value === 'string' && /^[a-z][a-z0-9-]{4,28}[a-z0-9]@oldx-staging\.iam\.gserviceaccount\.com$/.test(value);
const cloudRunAudience = value => {
  try {
    const url = new URL(value);
    return url.protocol === 'https:' && /^[-a-z0-9]+\.[-a-z0-9]+\.run\.app$/.test(url.hostname)
      && url.origin === value && url.pathname === '/' && !url.username && !url.password
      && !url.search && !url.hash;
  } catch { return false; }
};
const distinctAudience = value => typeof value === 'string' && value.length >= 10 && value.length <= 512
  && !/[\s\u0000-\u001f\u007f]/.test(value);
const base64url = value => typeof value === 'string' && value.length > 0 && /^[A-Za-z0-9_-]+$/.test(value);
const int = value => Number.isSafeInteger(value) && value > 0;
const deny = () => { throw Error('C2_IDENTITY_UNAVAILABLE'); };
function decodeClaims(token) {
  const bits = token.split('.');
  if (bits.length !== 3 || !bits.every(base64url) || token.length > 8192) return null;
  try {
    const header = JSON.parse(Buffer.from(bits[0], 'base64url').toString('utf8'));
    const claims = JSON.parse(Buffer.from(bits[1], 'base64url').toString('utf8'));
    if (header?.alg !== 'RS256' || typeof claims !== 'object' || claims === null) return null;
    return claims;
  } catch { return null; }
}
async function boundedToken(response, url, wait, signal) {
  if (!(response instanceof Response) || response.status !== 200 || !response.ok || response.redirected
    || response.url && response.url !== url || response.headers.get('Metadata-Flavor') !== 'Google'
    || !response.body) deny();
  const claimedSize = response.headers.get('content-length');
  if (claimedSize !== null && (!/^\d{1,5}$/.test(claimedSize) || Number(claimedSize) > 8192)) deny();
  const reader = response.body.getReader();
  const chunks = []; let total = 0;
  try {
    for (;;) {
      const {done, value} = await wait(()=>reader.read());
      if (done) break;
      total += value.byteLength;
      if (total > 8192) deny();
      chunks.push(value);
    }
  } finally { void reader.cancel().catch(() => {}); }
  const bytes = new Uint8Array(total); let cursor = 0;
  for (const chunk of chunks) { bytes.set(chunk, cursor); cursor += chunk.byteLength; }
  try { return new TextDecoder('utf-8', {fatal:true}).decode(bytes).trim(); }
  catch { deny(); }
}

// The metadata transport is an EXTERNAL trust boundary. A host must inject a
// server-only fetch that talks to the exact Google metadata address. This
// adapter only validates returned shape; cryptographic signature verification
// belongs to Google Cloud Run IAM and the existing backend RS256 verifier.
export function createC2CloudRunMetadataIdentity({enabled=false,serviceAccount,
  invokerAudience,assertionAudience,fetchMetadata,now=Date.now}={}) {
  const ready = enabled === true && principal(serviceAccount) && cloudRunAudience(invokerAudience)
    && distinctAudience(assertionAudience) && assertionAudience !== invokerAudience
    && typeof fetchMetadata === 'function' && typeof now === 'function';
  async function acquire(audience, {signal}={}) {
    if (!ready || signal?.aborted) deny();
    const start = now();
    if (!int(start) || audience !== invokerAudience && audience !== assertionAudience) deny();
    const url = METADATA + '?audience=' + encodeURIComponent(audience) + '&format=full';
    const controller = new AbortController();
    const abort = () => controller.abort();
    signal?.addEventListener('abort', abort, {once:true});
    if (signal?.aborted) abort();
    const stopped = new Promise((_,reject)=>{
      controller.signal.addEventListener('abort',()=>reject(Error('Stopped')),{once:true});
      if(controller.signal.aborted)reject(Error('Stopped'));
    });
    stopped.catch(()=>{});
    const wait = operation => Promise.race([Promise.resolve().then(()=>{
      if(controller.signal.aborted)deny();return operation();
    }),stopped]);
    const timer = setTimeout(abort, 1500);
    try {
      const response = await wait(()=>fetchMetadata(url, {method:'GET',headers:{'Metadata-Flavor':'Google'},
        signal:controller.signal,redirect:'error',cache:'no-store',credentials:'omit'}));
      const token = await boundedToken(response, url, wait, controller.signal);
      const claims = decodeClaims(token);
      const fresh = now();
      const seconds = Math.floor(fresh / 1000);
      if (!claims || !int(fresh) || controller.signal.aborted ||
        !['https://accounts.google.com','accounts.google.com'].includes(claims.iss) ||
        claims.aud !== audience || claims.email !== serviceAccount || claims.email_verified !== true ||
        typeof claims.sub !== 'string' || !/^\d{1,32}$/.test(claims.sub) ||
        !int(claims.iat) || !int(claims.exp) || claims.exp <= claims.iat ||
        claims.exp - claims.iat > 3600 || claims.iat > seconds + 5 ||
        seconds - claims.iat > 60 || claims.exp * 1000 <= fresh + 5000 ||
        claims.exp * 1000 > fresh + 3600000) deny();
      // Google ID token lifetime remains signed/unchanged. The website assertion
      // envelope is a LOCAL short lease matching the independent verifier age.
      const expiresAtMs=audience===assertionAudience?Math.min(claims.exp*1000,claims.iat*1000+60000):claims.exp*1000;
      if(expiresAtMs<=fresh+5000)deny();
      return Object.freeze({token,principal:serviceAccount,audience,expiresAtMs});
    } catch { deny(); }
    finally {clearTimeout(timer); signal?.removeEventListener('abort',abort);}
  }
  return Object.freeze({ready,
    getInvokerCredential: async ({audience,signal}={}) => {
      if (audience !== invokerAudience) deny();
      const item = await acquire(invokerAudience,{signal});
      return Object.freeze({...item,type:'cloud-run-iam-id-token'});
    },
    getWebsiteAttestation: async ({audience,signal}={}) => {
      if (audience !== assertionAudience) deny();
      return acquire(assertionAudience,{signal});
    }
  });
}
