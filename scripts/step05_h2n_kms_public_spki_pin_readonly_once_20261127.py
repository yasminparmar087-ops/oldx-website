#!/usr/bin/env python3
"""OLDX Step05 H2N: source-only, new KMS public-key read under new owner consent.

Only GET exact KMS version metadata and version/publicKey once, fail closed.
SPKI RSA DER decoded and sha256 pinned. No create/sign/IAM/Firebase/Run.
Never repeat after H2N marker, even when 403/timeout/STOP.
"""
from __future__ import annotations
import base64
import hashlib
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

ROOT=Path("/root")
PROJECT="oldx-staging"
OWNER="yasminparmar087@gmail.com"
KEY=("projects/oldx-staging/locations/asia-south1/keyRings/"
     "oldx-c2-h2-signing/cryptoKeys/oldx-c2-attestation-rs256")
VERSION=KEY+"/cryptoKeyVersions/1"
ALGORITHM="RSA_SIGN_PKCS1_2048_SHA256"
SDK=ROOT/"oldx-tools/native-gcloud-594.0.1/google-cloud-sdk"
GCLOUD=SDK/"bin/gcloud"
PY=SDK/"platform/bundledpythonunix/bin/python3"
CONFIG=ROOT/"oldx-tools/oldx-h1b-g2-20261126-cloudsdk-config"
H2M=ROOT/".oldx-step05-h2m-new-ring-key-one-create-once-20261127"
MARKER=ROOT/".oldx-step05-h2n-public-spki-pin-readonly-once-20261127"
VERSION_URL="https://cloudkms.googleapis.com/v1/"+VERSION
PUBLIC_URL=VERSION_URL+"/publicKey"
ALLOWED={VERSION_URL,PUBLIC_URL}

class Stop(Exception): pass
def need(cond,reason):
    if not cond: raise Stop(reason)

def cli(env,args):
    try:
        p=subprocess.run([str(GCLOUD)]+args,env=env,stdin=subprocess.DEVNULL,
                         stdout=subprocess.PIPE,stderr=subprocess.PIPE,
                         timeout=25,check=False)
    except subprocess.TimeoutExpired:
        raise Stop("ISOLATED_GCLOUD_TIMEOUT") from None
    need(p.returncode==0,"ISOLATED_GCLOUD_FAILED")
    return p.stdout.decode("utf-8","replace").strip()

def crc32c(data):
    crc=0xffffffff
    for byte in data:
        crc ^= byte
        for _ in range(8):
            crc=(crc>>1) ^ (0x82f63b78 if crc&1 else 0)
    return (crc^0xffffffff)&0xffffffff

def parse_tlv(buf,offset,tag):
    need(offset+2<=len(buf) and buf[offset]==tag,"DER_TAG_OR_LENGTH_BAD")
    size=buf[offset+1]
    pos=offset+2
    if size&0x80:
        count=size&0x7f
        need(1<=count<=3 and pos+count<=len(buf),"DER_LONG_LENGTH_BAD")
        length=int.from_bytes(buf[pos:pos+count],"big")
        need(length>=128 and buf[pos]!=0,"DER_NONCANONICAL_LENGTH")
        pos+=count
    else:
        length=size
    end=pos+length
    need(end<=len(buf),"DER_TRUNCATED")
    return pos,end,end

def validate_spki(pem):
    need(isinstance(pem,str) and len(pem)<=8192,"PEM_INVALID_SIZE")
    lines=pem.strip().splitlines()
    need(3<=len(lines)<=32 and lines[0]=="-----BEGIN PUBLIC KEY-----"
         and lines[-1]=="-----END PUBLIC KEY-----","PUBLIC_PEM_ARMOR_INVALID")
    b64="".join(lines[1:-1])
    need(bool(re.fullmatch(r"[A-Za-z0-9+/]+={0,2}",b64)),
         "PEM_BASE64_INVALID")
    der=base64.b64decode(b64,validate=True)
    need(base64.b64encode(der).decode("ascii")==b64 and len(der)<=1024,
         "PEM_BASE64_NONCANONICAL_OR_OVERSIZE")
    a,z,next_=parse_tlv(der,0,0x30)
    need(next_==len(der),"SPKI_TRAILING_BYTES")
    b,c,after_alg=parse_tlv(der,a,0x30)
    # AlgorithmIdentifier: rsaEncryption OID + NULL parameters.
    need(der[b:c]==bytes.fromhex("06092a864886f70d0101010500"),
         "NOT_RSA_SPKI_ALGORITHM")
    bit_start,bit_end,after_bit=parse_tlv(der,after_alg,0x03)
    need(after_bit==z and der[bit_start]==0,"SPKI_BIT_STRING_INVALID")
    inner=der[bit_start+1:bit_end]
    x,y,endrsa=parse_tlv(inner,0,0x30)
    need(endrsa==len(inner),"RSA_PUBLIC_TRAILING_BYTES")
    m1,m2,next_mod=parse_tlv(inner,x,0x02)
    e1,e2,end_exp=parse_tlv(inner,next_mod,0x02)
    need(end_exp==y,"RSA_EXPONENT_EXTRA_FIELDS")
    mod=inner[m1:m2]; exp=inner[e1:e2]
    need(len(mod)==257 and mod[0]==0 and mod[1]&0x80,
         "RSA_MODULUS_NOT_2048_BIT")
    need(exp==b"\x01\x00\x01","RSA_EXPONENT_NOT_65537")
    return der

def owner_token():
    need(sys.argv[1:]==["--owner-approved-exact-h2n-two-public-gets-once"],
         "H2N_EXACT_OWNER_CONSENT_FLAG_REQUIRED")
    need(platform.system()=="Linux" and os.geteuid()==0
         and "microsoft" in platform.release().lower(),"ROOT_WSL_REQUIRED")
    need(not MARKER.exists() and not MARKER.is_symlink(),
         "H2N_ONE_SHOT_ALREADY_CONSUMED")
    need(H2M.is_file() and not H2M.is_symlink()
         and H2M.stat().st_uid==0 and H2M.stat().st_size<=4096,
         "H2M_MARKER_UNTRUSTED")
    lines=H2M.read_text(encoding="utf-8").splitlines()
    need("ATTEMPT_CONSUMED=TRUE" in lines
         and "PROJECT="+PROJECT in lines
         and "RESULT=PASS_ONE_NEW_RING_KEY_SOFTWARE_VERSION_VERIFIED" in lines,
         "H2M_SUCCESS_RECEIPT_NOT_FOUND")
    pointers=[x[9:] for x in lines if x.startswith("EVIDENCE=")]
    need(len(pointers)==1,"H2M_EVIDENCE_MISSING")
    evid=Path(pointers[0])
    need(evid.parent==ROOT and bool(re.fullmatch(
         r"oldx-h2m-new-signing-key-\d{8}T\d{6}Z",evid.name))
         and evid.is_dir() and not evid.is_symlink()
         and evid.stat().st_uid==0,"H2M_EVIDENCE_DIR_BAD")
    doc=evid/"sanitized-h2m-one-ring-key.json"
    need(doc.is_file() and not doc.is_symlink() and doc.stat().st_uid==0
         and doc.stat().st_size<=8192,"H2M_EVIDENCE_BAD")
    data=json.loads(doc.read_text(encoding="utf-8"))
    need(data.get("result")=="PASS_ONE_NEW_RING_KEY_SOFTWARE_VERSION_VERIFIED"
         and data.get("project")==PROJECT and data.get("key")==KEY
         and data.get("algorithm")==ALGORITHM
         and data.get("protection")=="SOFTWARE"
         and data.get("version_verified")==VERSION
         and data.get("ring_readback_verified") is True
         and data.get("key_readback_verified") is True,
         "H2M_VERIFIED_VERSION_MISMATCH")
    need(SDK.is_dir() and not SDK.is_symlink() and SDK.stat().st_uid==0,
         "NATIVE_SDK_UNTRUSTED")
    need(GCLOUD.is_file() and not GCLOUD.is_symlink()
         and GCLOUD.stat().st_uid==0 and os.access(GCLOUD,os.X_OK),
         "NATIVE_GCLOUD_UNTRUSTED")
    py=PY.resolve(strict=True)
    need(py.is_relative_to(SDK.resolve(strict=True))
         and py.is_file() and py.stat().st_uid==0 and os.access(py,os.X_OK),
         "NATIVE_PYTHON_UNTRUSTED")
    need(CONFIG.is_dir() and not CONFIG.is_symlink()
         and CONFIG.stat().st_uid==0,"ISOLATED_CONFIG_UNTRUSTED")
    env=dict(os.environ)
    env.update({"HOME":str(ROOT),"PATH":str(SDK/"bin")+":/usr/bin:/bin",
                "CLOUDSDK_CONFIG":str(CONFIG),"CLOUDSDK_PYTHON":str(PY),
                "CLOUDSDK_CORE_DISABLE_USAGE_REPORTING":"1",
                "CLOUDSDK_COMPONENT_MANAGER_DISABLE_UPDATE_CHECK":"1",
                "CLOUDSDK_CORE_CHECK_GCE_METADATA":"false"})
    env.pop("GOOGLE_APPLICATION_CREDENTIALS",None)
    env.pop("CLOUDSDK_AUTH_CREDENTIAL_FILE_OVERRIDE",None)
    need(cli(env,["auth","list","--filter=status:ACTIVE",
                  "--format=value(account)"])==OWNER,"WRONG_OWNER_ACCOUNT")
    need(cli(env,["config","get-value","project"])==PROJECT,
         "WRONG_STAGING_PROJECT")
    token=cli(env,["--quiet","--account="+OWNER,"auth","print-access-token"])
    need(bool(re.fullmatch(r"[A-Za-z0-9._~+-]{40,4096}",token)),
         "OWNER_TOKEN_NOT_AVAILABLE")
    return token

class NoRedirect(request.HTTPRedirectHandler):
    def redirect_request(self,*args,**kwargs): return None

OPENER=request.build_opener(request.ProxyHandler({}),
        request.HTTPSHandler(context=ssl.create_default_context()),
        NoRedirect())

def get(url,token):
    need(url in ALLOWED,"KMS_REQUEST_OUTSIDE_H2N_SCOPE")
    req=request.Request(url,method="GET",headers={
        "Authorization":"Bearer "+token,
        "Accept":"application/json",
        "User-Agent":"OLDX-H2N-public-key-metadata-only/1"})
    try:
        with OPENER.open(req,timeout=35) as response:
            raw=response.read(32769)
            need(response.status==200 and len(raw)<=32768,
                 "KMS_UNEXPECTED_HTTP_OR_RESPONSE_SIZE")
            data=json.loads(raw)
            need(isinstance(data,dict),"KMS_RESPONSE_SCHEMA_BAD")
            return data
    except error.HTTPError as exc:
        code=exc.code
        exc.close()
        raise Stop("KMS_HTTP_"+str(code)) from None
    except (error.URLError,TimeoutError,ssl.SSLError):
        raise Stop("KMS_NETWORK_OR_TIMEOUT") from None

def main():
    os.umask(0o077)
    try: token=owner_token()
    except (Stop,OSError,ValueError,TypeError,UnicodeError) as exc:
        print("OLDX_H2N_RESULT=STOP_BEFORE_REQUEST")
        print("OLDX_H2N_REASON="+(str(exc) if isinstance(exc,Stop)
                                 else type(exc).__name__))
        print("OLDX_H2N_CLOUD_WRITES=NONE")
        return 2
    evidence=ROOT/("oldx-h2n-public-key-pin-"+
                   datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ"))
    try:
        evidence.mkdir(mode=0o700)
        fd=os.open(MARKER,os.O_WRONLY|os.O_CREAT|os.O_EXCL
                   |getattr(os,"O_NOFOLLOW",0),0o600)
        with os.fdopen(fd,"w",encoding="utf-8") as out:
            out.write("ATTEMPT_CONSUMED=TRUE\nEVIDENCE="+str(evidence)+"\n")
    except OSError:
        print("OLDX_H2N_RESULT=STOP_MARKER")
        return 2
    result="STOP_AFTER_MARKER"; reason="UNKNOWN"
    fingerprint="NOT_VERIFIED"; crc_state="NOT_CHECKED"
    try:
        version=get(VERSION_URL,token)
        need(version.get("name")==VERSION and version.get("state")=="ENABLED"
             and version.get("algorithm")==ALGORITHM
             and version.get("protectionLevel")=="SOFTWARE",
             "KMS_VERSION_METADATA_DRIFT")
        public=get(PUBLIC_URL,token)
        # name and protection are documented Beta fields; validate if supplied.
        need(public.get("algorithm")==ALGORITHM and
             public.get("name",VERSION)==VERSION and
             public.get("protectionLevel","SOFTWARE")=="SOFTWARE",
             "KMS_PUBLIC_KEY_METADATA_DRIFT")
        pem=public.get("pem")
        der=validate_spki(pem)
        checksum=public.get("pemCrc32c")
        if checksum is not None:
            need(str(checksum).isdigit() and 0<=int(checksum)<=0xffffffff
                 and crc32c(pem.encode("utf-8"))==int(checksum),
                 "PUBLIC_PEM_CRC32C_MISMATCH")
            crc_state="VERIFIED"
        else:
            crc_state="NOT_PROVIDED_BY_API"
        fingerprint=hashlib.sha256(der).hexdigest()
        (evidence/"public-spki.pem").write_text(pem,encoding="utf-8")
        result="PASS_PUBLIC_SPKI_PIN_VERIFIED_READONLY"
        reason="EXACT_VERSION_RSA2048_AND_SHA256_CONFIRMED"
    except (Stop,OSError,ValueError,TypeError,UnicodeError,
            base64.binascii.Error) as exc:
        reason=str(exc) if isinstance(exc,Stop) else type(exc).__name__
    finally:
        try:
            (evidence/"sanitized-h2n-public-pin.json").write_text(
                json.dumps({"version":VERSION,"algorithm":ALGORITHM,
                    "spki_sha256":fingerprint,"pem_crc32c":crc_state,
                    "result":result,"reason":reason,
                    "resource_writes":False,"signing":False,
                    "h2":"NO_GO","production":"NO_GO"},
                    sort_keys=True,indent=2)+"\n",encoding="utf-8")
            with MARKER.open("a",encoding="utf-8") as out:
                out.write("RESULT="+result+"\nREASON="+reason+"\n")
        except OSError: result="STOP_EVIDENCE_WRITE"
        print("OLDX_H2N_RESULT="+result)
        print("OLDX_H2N_REASON="+reason)
        print("OLDX_H2N_VERSION="+VERSION)
        print("OLDX_H2N_SPKI_SHA256="+fingerprint)
        print("OLDX_H2N_PEM_CRC32C="+crc_state)
        print("OLDX_H2N_CLOUD_WRITES=NONE")
        print("OLDX_H2N_SIGN_IAM_H2_PRODUCTION=NOT_ATTEMPTED")
        print("OLDX_H2N_DO_NOT_REPEAT=TRUE")
    return 0 if result=="PASS_PUBLIC_SPKI_PIN_VERIFIED_READONLY" else 2

if __name__=="__main__": sys.exit(main())
