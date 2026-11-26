#!/usr/bin/env python3
"""OLDX Step05 H2P1: one approved creation of exactly 3 NEW runtime service accounts.

SOURCE ONLY UNTIL NEW EXPLICIT OWNER CONSENT FOR THESE EXACT THREE WRITES.
Guarded root WSL owner session; old H2O read-only receipt must show complete
absence of all 3. Before the first write, three exact-name GETs must each 404.
Then one-shot marker is consumed BEFORE any create POST. At most 3 creates
and 3 readbacks. On partial/ambiguous outcome STOP WITHOUT RETRY OR CLEANUP.
NO IAM policy grants, keys, roles, KMS signing, Cloud Run, Firebase or H2 GO.
"""
from __future__ import annotations

import json
import os
import platform
import re
import ssl
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from urllib import request, error

ROOT = Path("/root")
OWNER = "yasminparmar087@gmail.com"
PROJECT = "oldx-staging"
CANDIDATES = (
    ("MEDIATOR", "oldx-c2-web-mediator", "OLDX H2 Website Mediator"),
    ("GATEWAY", "oldx-c2-private-gateway", "OLDX H2 Private Gateway"),
    ("BACKEND", "oldx-c2-product-backend", "OLDX H2 Product Backend"),
)
OLD_DISABLED = "oldx-c2-mediator@oldx-staging.iam.gserviceaccount.com"
SERVICE_ROOT = "https://iam.googleapis.com/v1/projects/oldx-staging/serviceAccounts"
SDK = ROOT / "oldx-tools/native-gcloud-594.0.1/google-cloud-sdk"
GCLOUD = SDK / "bin/gcloud"
PY = SDK / "platform/bundledpythonunix/bin/python3"
CONFIG = ROOT / "oldx-tools/oldx-h1b-g2-20261126-cloudsdk-config"
H2O = ROOT / ".oldx-step05-h2o-signing-identity-and-key-policy-readonly-once-20261127"
MARKER = ROOT / ".oldx-step05-h2p1-three-h2-runtime-service-accounts-owner-once-20261127"

class Stop(Exception):
    pass

def need(ok, reason):
    if not ok:
        raise Stop(reason)

def email_for(account_id):
    need(re.fullmatch(r"[a-z][a-z0-9-]{5,29}", account_id)
         and account_id[-1] != "-", "INVALID_ACCOUNT_ID")
    return account_id + "@" + PROJECT + ".iam.gserviceaccount.com"

def target_url(account_id):
    return SERVICE_ROOT + "/" + email_for(account_id)

CREATE_URL = SERVICE_ROOT
GET_URLS = frozenset(target_url(a) for _, a, _ in CANDIDATES)
ALLOWED = frozenset([("POST", CREATE_URL)] + [("GET", u) for u in GET_URLS])

def cli(env, args):
    try:
        p = subprocess.run([str(GCLOUD)] + args,
            env=env, stdin=subprocess.DEVNULL,
            stdout=subprocess.PIPE, stderr=subprocess.PIPE,
            check=False, timeout=25)
    except subprocess.TimeoutExpired:
        raise Stop("OWNER_CLOUDSDK_TIMEOUT") from None
    need(p.returncode == 0, "OWNER_CLOUDSDK_FAILED")
    return p.stdout.decode("utf-8","replace").strip()

def verified_prior_receipt():
    need(H2O.is_file() and not H2O.is_symlink()
         and H2O.stat().st_uid == 0 and H2O.stat().st_size <= 4096,
         "H2O_MARKER_NOT_TRUSTED")
    marker = H2O.read_text(encoding="utf-8").splitlines()
    need("ATTEMPT_CONSUMED=TRUE" in marker and
         "RESULT=READ_ONLY_EXACT_SIGNER_IDENTITY_AND_KEY_POLICY_WITH_LIMITS"
         in marker, "H2O_SUCCESS_NOT_PRESENT")
    ptr = [v[9:] for v in marker if v.startswith("EVIDENCE=")]
    need(len(ptr) == 1, "H2O_EVIDENCE_UNKNOWN")
    evid = Path(ptr[0])
    need(evid.parent == ROOT and bool(re.fullmatch(
        r"oldx-h2o-signer-iam-metadata-\d{8}T\d{6}Z", evid.name))
        and evid.is_dir() and not evid.is_symlink()
        and evid.stat().st_uid == 0, "H2O_EVIDENCE_DIR_UNTRUSTED")
    doc = evid / "sanitized-h2o-iam-metadata.json"
    need(doc.is_file() and not doc.is_symlink() and doc.stat().st_uid == 0
         and doc.stat().st_size <= 16384, "H2O_EVIDENCE_FILE_UNTRUSTED")
    data = json.loads(doc.read_text(encoding="utf-8"))
    candidates = data.get("summary", {}).get("identity", {}).get("candidates", {})
    policy = data.get("summary", {}).get("key_policy", {})
    need(data.get("project") == PROJECT and
         data.get("key") ==
         "projects/oldx-staging/locations/asia-south1/keyRings/"
         "oldx-c2-h2-signing/cryptoKeys/oldx-c2-attestation-rs256" and
         data.get("result") ==
         "READ_ONLY_EXACT_SIGNER_IDENTITY_AND_KEY_POLICY_WITH_LIMITS" and
         data.get("cloud_writes") is False and
         data.get("summary", {}).get("identity", {}).get("scope") ==
         "COMPLETE_VISIBLE_PAGE" and
         all(candidates.get(k, {}).get("state") ==
             "NOT_IN_COMPLETE_PROJECT_LIST"
             for k in ("mediator", "gateway", "backend")) and
         policy.get("scope") == "EXACT_CRYPTOKEY_DIRECT_POLICY_ONLY" and
         policy.get("direct_gateway_signer_present") is False and
         policy.get("safe_to_grant") is False,
         "H2O_RESULT_OR_TRUST_BOUNDARY_MISMATCH")

def owner_token():
    need(sys.argv[1:] == ["--owner-explicitly-approved-only-three-new-h2-runtime-sa-creates"],
         "EXACT_THREE_SA_CREATE_APPROVAL_FLAG_REQUIRED")
    need(platform.system() == "Linux" and os.geteuid() == 0
         and "microsoft" in platform.release().lower(),
         "ROOT_WSL_REQUIRED")
    need(not MARKER.exists() and not MARKER.is_symlink(),
         "H2P1_ALREADY_CONSUMED")
    need(len({email_for(a) for _,a,_ in CANDIDATES}) == 3
         and all(email_for(a) != OLD_DISABLED for _,a,_ in CANDIDATES),
         "SCOPE_OR_TRIAL_IDENTITY_DRIFT")
    verified_prior_receipt()
    need(SDK.is_dir() and not SDK.is_symlink()
         and SDK.stat().st_uid == 0, "NATIVE_SDK_UNTRUSTED")
    need(GCLOUD.is_file() and not GCLOUD.is_symlink()
         and GCLOUD.stat().st_uid == 0 and os.access(GCLOUD, os.X_OK),
         "NATIVE_GCLOUD_UNTRUSTED")
    py = PY.resolve(strict=True)
    need(py.is_relative_to(SDK.resolve(strict=True))
         and py.is_file() and py.stat().st_uid == 0
         and os.access(py, os.X_OK), "NATIVE_PYTHON_UNTRUSTED")
    need(CONFIG.is_dir() and not CONFIG.is_symlink()
         and CONFIG.stat().st_uid == 0, "ISOLATED_CONFIG_UNTRUSTED")
    env = dict(os.environ)
    env.update({"HOME":str(ROOT),
        "PATH":str(SDK/"bin")+":/usr/bin:/bin",
        "CLOUDSDK_CONFIG":str(CONFIG),
        "CLOUDSDK_PYTHON":str(PY),
        "CLOUDSDK_CORE_DISABLE_USAGE_REPORTING":"1",
        "CLOUDSDK_COMPONENT_MANAGER_DISABLE_UPDATE_CHECK":"1",
        "CLOUDSDK_CORE_CHECK_GCE_METADATA":"false"})
    env.pop("GOOGLE_APPLICATION_CREDENTIALS",None)
    env.pop("CLOUDSDK_AUTH_CREDENTIAL_FILE_OVERRIDE",None)
    need(cli(env, ["auth","list","--filter=status:ACTIVE",
                   "--format=value(account)"])==OWNER,
         "WRONG_OWNER_ACCOUNT")
    need(cli(env, ["config","get-value","project"])==PROJECT,
         "WRONG_STAGING_PROJECT")
    tok = cli(env, ["--quiet","--account="+OWNER,
                   "auth","print-access-token"])
    need(bool(re.fullmatch(r"[A-Za-z0-9._~+-]{40,4096}", tok)),
         "OWNER_ACCESS_TOKEN_UNAVAILABLE")
    return tok

class NoRedirect(request.HTTPRedirectHandler):
    def redirect_request(self,*args,**kwargs):
        return None

OPENER = request.build_opener(request.ProxyHandler({}),
    request.HTTPSHandler(context=ssl.create_default_context()),
    NoRedirect())

def rest(method, url, token, body=None):
    need((method,url) in ALLOWED, "REQUEST_OUTSIDE_EXACT_SA_ALLOWLIST")
    need((method == "POST") == (body is not None),
         "UNEXPECTED_HTTP_BODY")
    if method == "POST":
        need(url == CREATE_URL and isinstance(body,dict) and
             set(body)=={"accountId","serviceAccount"} and
             body["accountId"] in [v for _,v,_ in CANDIDATES] and
             isinstance(body["serviceAccount"],dict) and
             set(body["serviceAccount"])=={"displayName"} and
             body["serviceAccount"]["displayName"] ==
             next(label for _,v,label in CANDIDATES
                  if v==body["accountId"]),
             "POST_BODY_SCOPE_DRIFT")
    req = request.Request(url,method=method, headers={
        "Authorization":"Bearer "+token,
        "Accept":"application/json",
        "User-Agent":"OLDX-H2P1-three-sa-only/1",
        **({"Content-Type":"application/json"} if body is not None else {})},
        data=json.dumps(body,separators=(",",":")).encode("utf-8")
        if body is not None else None)
    try:
        with OPENER.open(req,timeout=35) as response:
            raw = response.read(32769)
            need(response.status==200 and len(raw)<=32768,
                 "UNEXPECTED_GOOGLE_IAM_RESPONSE")
            payload=json.loads(raw)
            need(isinstance(payload,dict), "INVALID_IAM_RESPONSE")
            return 200, payload
    except error.HTTPError as exc:
        code=exc.code
        exc.close()
        return code, {}
    except (error.URLError,ssl.SSLError,TimeoutError):
        raise Stop("GOOGLE_IAM_NETWORK_OR_TIMEOUT") from None

def identity(obj,account_id):
    email=email_for(account_id)
    need(isinstance(obj,dict)
         and obj.get("email")==email
         and isinstance(obj.get("uniqueId"),str)
         and bool(re.fullmatch(r"\d{10,32}",obj["uniqueId"]))
         and obj.get("disabled",False) is False,
         "SA_EMAIL_UID_OR_DISABLED_MISMATCH")
    name=obj.get("name")
    need(isinstance(name,str) and name.startswith(
         "projects/"+PROJECT+"/serviceAccounts/")
         and name.rsplit("/",1)[-1] in (email,obj["uniqueId"]),
         "SA_CANONICAL_NAME_MISMATCH")
    if "projectId" in obj:
        need(obj["projectId"]==PROJECT,"SA_PROJECT_ID_MISMATCH")
    return obj["uniqueId"]

def append(line):
    with MARKER.open("a",encoding="utf-8") as out:
        out.write(line+"\n")

def main():
    os.umask(0o077)
    try:
        token=owner_token()
        # Fresh exact-name absent checks; ANY 403/timeout is STOP, not absence.
        for kind,account,_ in CANDIDATES:
            code,_=rest("GET",target_url(account),token)
            need(code==404,kind+"_TARGET_NOT_FRESH_404_HTTP_"+str(code))
    except (Stop,OSError,ValueError,TypeError,UnicodeError) as exc:
        print("OLDX_H2P1_RESULT=STOP_BEFORE_WRITE")
        print("OLDX_H2P1_REASON="+(str(exc) if isinstance(exc,Stop)
                                  else type(exc).__name__))
        print("OLDX_H2P1_CLOUD_WRITES=NONE")
        return 2
    evidence=ROOT/("oldx-h2p1-three-runtime-sas-"+
                    datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ"))
    try:
        evidence.mkdir(mode=0o700)
        fd=os.open(MARKER,os.O_CREAT|os.O_EXCL|os.O_WRONLY|
                   getattr(os,"O_NOFOLLOW",0),0o600)
        with os.fdopen(fd,"w",encoding="utf-8") as out:
            out.write("ATTEMPT_CONSUMED=TRUE\nPROJECT="+PROJECT+
                      "\nEVIDENCE="+str(evidence)+"\n")
    except OSError:
        print("OLDX_H2P1_RESULT=STOP_MARKER")
        print("OLDX_H2P1_CLOUD_WRITES=NONE")
        return 2
    result="STOP_AFTER_MARKER"; reason="UNKNOWN"
    created=[]
    attempted=[]
    try:
        for kind,account,label in CANDIDATES:
            append("CREATE_"+kind+"_ABOUT_TO_BE_SENT=TRUE")
            attempted.append(kind)
            code, data=rest("POST",CREATE_URL,token,{
                "accountId":account,
                "serviceAccount":{"displayName":label}})
            need(code==200,
                 kind+"_CREATE_HTTP_"+str(code))
            uid=identity(data,account)
            code,fresh=rest("GET",target_url(account),token)
            need(code==200,kind+"_READBACK_HTTP_"+str(code))
            need(identity(fresh,account)==uid,kind+"_UID_READBACK_DRIFT")
            created.append({"kind":kind,"email":email_for(account),"uid":uid,
                            "state":"ENABLED_NO_ROLES_ASSIGNED_BY_THIS_SCRIPT"})
            append("VERIFIED_"+kind+"_UID="+uid)
        need(len(created)==3 and len({i["uid"] for i in created})==3,
             "NON_DISTINCT_CREATED_UID")
        result="PASS_THREE_NEW_H2_RUNTIME_SERVICE_ACCOUNTS_CREATED_VERIFIED"
        reason="EXACT_CREATE_AND_READBACK_UIDS_CONFIRMED"
    except (Stop,OSError,ValueError,TypeError,UnicodeError) as exc:
        reason=str(exc) if isinstance(exc,Stop) else type(exc).__name__
        # No retries, no automatic cleanup after ANY attempted POST.
    finally:
        try:
            (evidence/"sanitized-h2p1-created-sas.json").write_text(
                json.dumps({"project":PROJECT,"attempted":attempted,
                    "verified_created":created,
                    "result":result,"reason":reason,
                    "kms_iam_grants":False,"service_account_keys":False,
                    "cloud_run":False,"h2":"NO_GO","production":"NO_GO"},
                    sort_keys=True,indent=2)+"\n",encoding="utf-8")
            append("RESULT="+result)
            append("REASON="+reason)
        except OSError:
            result="STOP_EVIDENCE_WRITE"
        print("OLDX_H2P1_RESULT="+result)
        print("OLDX_H2P1_REASON="+reason)
        print("OLDX_H2P1_PROJECT="+PROJECT)
        for kind,account,_ in CANDIDATES:
            v=next((x for x in created if x["kind"]==kind),None)
            print("OLDX_H2P1_"+kind+"_STATE="+
                  ("VERIFIED_NEW_ENABLED" if v else
                   ("ATTEMPTED_UNVERIFIED" if kind in attempted
                    else "NOT_ATTEMPTED")))
            if v: print("OLDX_H2P1_"+kind+"_UID="+v["uid"])
        print("OLDX_H2P1_CREATE_ATTEMPT_COUNT="+str(len(attempted)))
        print("OLDX_H2P1_VERIFIED_NEW_ACCOUNT_COUNT="+str(len(created)))
        print("OLDX_H2P1_IAM_GRANTS_KEYS_KMS_SIGN_RUN=NONE")
        print("OLDX_H2P1_H2_PRODUCTION=NO_GO")
        print("OLDX_H2P1_DO_NOT_REPEAT=TRUE")
    return 0 if result=="PASS_THREE_NEW_H2_RUNTIME_SERVICE_ACCOUNTS_CREATED_VERIFIED" else 2

if __name__=="__main__":
    sys.exit(main())
