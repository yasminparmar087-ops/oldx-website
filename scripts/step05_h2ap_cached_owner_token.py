#!/usr/bin/env python3
"""H2AP child: cached Owner token to anonymous IPC only; no refresh or persistence."""
from __future__ import annotations
import datetime,json,logging,os,re,sqlite3,stat,sys
from pathlib import Path
SDK=Path("/root/oldx-tools/native-gcloud-594.0.1/google-cloud-sdk")
CONFIG=Path("/root/oldx-tools/oldx-h1b-g2-20261126-cloudsdk-config")
OWNER="yasminparmar087@gmail.com"
class Stop(Exception):pass
def validate_cached(credential,now):
    from google.oauth2.credentials import Credentials
    if not isinstance(credential,Credentials):raise Stop("OWNER_USER_CREDENTIAL_REQUIRED")
    token=credential.token;expiry=credential.expiry
    if not isinstance(token,str) or not re.fullmatch(r"[A-Za-z0-9._~+-]{40,4096}",token):raise Stop("CACHED_TOKEN_MISSING")
    if not isinstance(expiry,datetime.datetime):raise Stop("CACHED_EXPIRY_MISSING")
    if expiry.tzinfo is None:expiry=expiry.replace(tzinfo=datetime.timezone.utc)
    remaining=(expiry-now).total_seconds()
    if not 180<=remaining<=3700:raise Stop("CACHED_TOKEN_EXPIRED_OR_INSUFFICIENT_NO_REFRESH")
    return {"token":token,"expiresAt":int(expiry.timestamp())}
def sandbox(config):
    # SDK may normally open SQLite writable or cache refreshed tokens.
    # Force its TWO existing stores read-only/immutable, and deny all network/writes.
    connect=sqlite3.connect;allowed={config/"credentials.db",config/"access_tokens.db"}
    def readonly(database,*args,**kwargs):
        p=Path(database)
        if p not in allowed or not p.is_file() or p.is_symlink() or p.stat().st_uid!=0:
            raise Stop("SDK_CACHE_FILE_SCOPE")
        kwargs["uri"]=True
        return connect(p.as_uri()+"?mode=ro&immutable=1",*args,**kwargs)
    sqlite3.connect=readonly
    def audit(event,args):
        if event=="open":
            mode=args[1] or "";flags=args[2]
            if any(c in str(mode) for c in "wax+") or isinstance(flags,int) and flags&(os.O_WRONLY|os.O_RDWR|os.O_CREAT|os.O_TRUNC|os.O_APPEND):
                raise Stop("SDK_WRITE_FORBIDDEN")
        if event.startswith(("socket.","subprocess.","os.exec","os.spawn")) or event in (
            "os.system","os.mkdir","os.remove","os.rmdir","os.rename","os.chmod","os.chown","os.link","os.symlink","os.truncate"):
            raise Stop("SDK_NETWORK_OR_MUTATION_FORBIDDEN")
        if event=="sqlite3.connect":
            value=str(args[0])
            if not any(value==p.as_uri()+"?mode=ro&immutable=1" for p in allowed):
                raise Stop("SDK_SQLITE_NOT_READONLY")
    sys.addaudithook(audit)
def main():
    if sys.argv[1:]!=["--h2ap-cached-owner-token-to-pipe-only"] or os.geteuid()!=0:return 2
    if not stat.S_ISFIFO(os.fstat(1).st_mode) or not os.readlink("/proc/self/fd/1").startswith("pipe:["):return 2
    logging.disable(logging.CRITICAL);sys.dont_write_bytecode=True
    sys.path[:0]=[str(SDK/"lib"),str(SDK/"lib/third_party")]
    sandbox(CONFIG)
    # Explicit account, no impersonation, no ADC, no credential refresh or API fallback.
    from googlecloudsdk.core.credentials import store
    credential=store.Load(account=OWNER,prevent_refresh=True,allow_account_impersonation=False)
    packet=validate_cached(credential,datetime.datetime.now(datetime.timezone.utc))
    os.write(1,json.dumps(packet,separators=(",",":")).encode())
    packet=None;credential=None
    return 0
if __name__=="__main__":
    try:sys.exit(main())
    except Exception as error:
        code=str(error) if isinstance(error,Stop) else type(error).__name__.upper()
        if not re.fullmatch(r"[A-Z0-9_]{1,100}",code):code="SDK_LOAD_UNKNOWN"
        os.write(2,("H2AP_TOKEN_STOP="+code).encode())
        sys.exit(2) # Fixed code only, never SDK exception/credential contents.
