// SOURCE ONLY: no listener is opened and no provider, token or SDK is created.
// A future separately approved staging host must inject a trusted mediator.
const operations = new Set(['save', 'owner', 'archive', 'list', 'detail']);
const forbidden = new Set([
  'cookie', 'x-serverless-authorization', 'x-oldx-gateway-attestation',
  'x-oldx-gateway-request-proof', 'x-oldx-mediated-website-origin',
  'x-oldx-gateway-nonce'
]);
const sensitive = new Set(['origin', 'authorization', 'content-type', 'content-length',
  'transfer-encoding', 'content-encoding']);
const origin = value => {
  try {
    const url = new URL(value);
    return typeof value === 'string' && url.protocol === 'https:' && url.origin === value &&
      url.pathname === '/' && !url.username && !url.password && !url.search && !url.hash;
  } catch { return false; }
};
const failure = (status, code) => ({status, body: JSON.stringify({ok:false,error:{code}})});
const jsonHeaders = {'content-type':'application/json; charset=utf-8',
  'cache-control':'private, no-store', 'x-content-type-options':'nosniff'};

// Node HTTP adapter for the existing C2 website mediator factory. Its own
// upstream identity, trust, quota, and private Gateway checks stay mandatory.
// Never construct origin from Host, Forwarded or X-Forwarded-* headers.
export function createC2WebsiteNodeHandler({enabled=false,websiteOrigin,allowedOrigins,
  mediator,timeoutMs=5000}={}) {
  const ready = enabled === true && origin(websiteOrigin) &&
    Array.isArray(allowedOrigins) && allowedOrigins.length > 0 && allowedOrigins.length <= 8 &&
    allowedOrigins.every(origin) && allowedOrigins.includes(websiteOrigin) &&
    typeof mediator?.fetch === 'function' && Number.isInteger(timeoutMs) &&
    timeoutMs >= 1 && timeoutMs <= 5000;
  return async (req,res) => {
    const send = (status,body,extra={}) => {
      if (res.destroyed || res.headersSent) return;
      res.shouldKeepAlive = false;
      res.writeHead(status,{...jsonHeaders,...extra,'connection':'close'});
      res.end(body);
    };
    if (!ready) return send(...Object.values(failure(503,'ENFORCEMENT_UNAVAILABLE')));
    const path=req.url??'', prefix='/api/staging/marketplace/';
    if (!path.startsWith(prefix) || !operations.has(path.slice(prefix.length)))
      return send(...Object.values(failure(404,'NOT_FOUND')));
    if (req.method !== 'POST' && req.method !== 'OPTIONS')
      return send(...Object.values(failure(405,'METHOD_NOT_ALLOWED')));
    if (req.rawHeaders.length>80) return send(...Object.values(failure(400,'INVALID_HEADERS')));
    const seen=new Set();
    for (let i=0;i<req.rawHeaders.length;i+=2) {
      const key=req.rawHeaders[i].toLowerCase();
      if(forbidden.has(key)) return send(...Object.values(failure(403,'DENIED')));
      if(sensitive.has(key) && seen.has(key)) return send(...Object.values(failure(400,'DUPLICATE_HEADER')));
      seen.add(key);
    }
    const caller=req.headers.origin;
    if (typeof caller !== 'string' || !allowedOrigins.includes(caller))
      return send(...Object.values(failure(403,'DENIED')));
    if(req.method==='OPTIONS' && req.headers['content-length'] !== undefined && req.headers['content-length'] !== '0')
      return send(...Object.values(failure(400,'INVALID_PREFLIGHT')));
    const publicRead=path.endsWith('/list') || path.endsWith('/detail');
    const limit=publicRead?4096:32768;
    const length=req.headers['content-length'];
    if (length!==undefined && (!/^\d{1,5}$/.test(length) || Number(length)>limit))
      return send(...Object.values(failure(413,'BODY_TOO_LARGE')));
    if (req.method==='POST' && (!/^application\/json(?:;\s*charset=utf-8)?$/i.test(req.headers['content-type']??'') ||
      req.headers['content-encoding'] && req.headers['content-encoding'] !== 'identity'))
      return send(...Object.values(failure(415,'UNSUPPORTED_MEDIA_TYPE')));
    const controller=new AbortController();
    const abort=()=>controller.abort();
    const stopped=new Promise((_,reject)=>{controller.signal.addEventListener('abort',()=>reject(Error('ABORTED')),{once:true});});
    stopped.catch(()=>{});
    const bounded=operation=>Promise.race([Promise.resolve().then(()=>{if(controller.signal.aborted)throw Error('ABORTED');return operation();}),stopped]);
    res.once('close',abort);
    const timer=setTimeout(abort,timeoutMs);
    try {
      const chunks=[];let size=0;
      const input=req[Symbol.asyncIterator]();
      for (;;) {
        const {done,value:chunk}=await bounded(()=>input.next());if(done)break;
        if(controller.signal.aborted) throw Error('ABORTED');
        size+=chunk.length;
        if(size>limit) return send(...Object.values(failure(413,'BODY_TOO_LARGE')));
        chunks.push(chunk);
      }
      const headers=new Headers();
      for(const key of ['origin','authorization','content-type','content-encoding',
        'access-control-request-method','access-control-request-headers']) {
        const v=req.headers[key];if(typeof v==='string') headers.set(key,v);
      }
      const request=new Request(websiteOrigin+path,{method:req.method,headers,
        ...(req.method==='POST'?{body:Buffer.concat(chunks,size)}:{}),signal:controller.signal});
      const result=await bounded(()=>mediator.fetch(request));
      if (!(result instanceof Response) || result.redirected || result.status<200 ||
        result.status>599 || result.status===204 && result.body) throw Error('BAD_RESPONSE');
      const out=[];let count=0;
      if(result.body){const output=result.body[Symbol.asyncIterator]();for(;;){
        const {done,value:chunk}=await bounded(()=>output.next());if(done)break;
        if(controller.signal.aborted) throw Error('ABORTED');
        count+=chunk.length;
        if(count>65536) throw Error('OVERSIZE_RESPONSE');
        out.push(chunk);
      }}
      const extra={};
      const corsOrigin=result.headers.get('access-control-allow-origin');
      if (corsOrigin===caller && allowedOrigins.includes(corsOrigin)) {
        extra['access-control-allow-origin']=corsOrigin;
        for(const key of ['access-control-allow-methods','access-control-allow-headers','vary']) {
          const value=result.headers.get(key);if(value && value.length<=200) extra[key]=value;
        }
      }
      send(result.status,Buffer.concat(out,count),extra);
    } catch {
      send(...Object.values(failure(503,'ENFORCEMENT_UNAVAILABLE')));
    } finally {clearTimeout(timer);res.off('close',abort);}
  };
}
