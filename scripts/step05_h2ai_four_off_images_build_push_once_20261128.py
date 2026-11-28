#!/usr/bin/env python3
"""BAJUTO Step05 H2AI — ONE Owner-approved LOCAL build+private registry push per role.

APPROVED: 4 immutable-source, default-OFF linux/amd64 images, each <=1
docker buildx build --push. Not approved: Cloud Run, Firestore, IAM, KMS, VPC,
Firebase, key/secret, real User data, old image overwrite, automatic retries.
This operates only in Owner's WSL root with pinned native gcloud.
Never rerun when local one-shot marker is present, including after partial
errors or unknown outcomes.
"""
from __future__ import annotations

import hashlib
import json
import os
import platform
import re
import secrets
import shutil
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path("/root")
PROJECT = "oldx-staging"
OWNER = "yasminparmar087@gmail.com"
REGION = "asia-south1"
REGISTRY = "asia-south1-docker.pkg.dev"
REPOSITORY = "oldx-staging-images"
REPO_URL = "https://github.com/yasminparmar087-ops/oldx-website.git"
BRANCH = "security-hardening-review"
APPROVED_SOURCE = "5d5a621d7a9d9015b5068077b914fef3d6fb9925"
ROLES = {
    "mediator": "oldx-c2-mediator-h2ah",
    "gateway": "oldx-c2-gateway-h2ah",
    "backend": "oldx-c2-backend-h2ah",
    "reader": "oldx-c2-kms-reader",
}
IMAGES = {role: f"{REGISTRY}/{PROJECT}/{REPOSITORY}/{name}"
          for role, name in ROLES.items()}
IMMUTABLE_BASE = "49559f4ee6632a11a13a7e198183efee1226de7a8f437df83c180b01bd8253ec"
IMMUTABLE_BUILDER = "dc26ae92c9fb15cf6b1d63e20e00be48fb23fceb061c54"
OLD_OFF = {"4b1bd8a5cba33e96969f8f92ebd73b73f281b6ca5279fd2b14d3be8e9a5391f2",
           "576a1faa599459ed9b1cdeccc01a3adc2076dffff617bec42f38df7d3a75663e",
           "612f3c02806a93d991127f87e34391646edf9bad251bb22b8aace90a434bc30a"}
SDK = ROOT / "oldx-tools/native-gcloud-594.0.1/google-cloud-sdk"
GCLOUD = SDK / "bin/gcloud"
PY = SDK / "platform/bundledpythonunix/bin/python3"
CONFIG = ROOT / "oldx-tools/oldx-h1b-g2-20261126-cloudsdk-config"
MARK = ROOT / ".oldx-step05-h2ai-four-off-build-push-once-20261128"
FLAG = "--h2ai-owner-approved-four-local-amd64-off-builds-private-push-once"
HEX64 = re.compile(r"sha256:[a-f0-9]{64}\Z")
TOKEN = re.compile(r"[A-Za-z0-9._~+\-]{40,4096}\Z")

class Stop(Exception):
    pass

def need(condition, message):
    if not condition:
        raise Stop(message)

def command(argv, *, cwd=None, env=None, timeout=45, input_bytes=None,
            capture=True, log=None):
    # All argv are constants or rigorously checked local path/image values.
    try:
        if log is not None:
            with open(log, "ab") as out:
                out.write(("\n$ EXECUTING_APPROVED_PHASE: " + str(argv[:3]) + "\n").encode())
                result = subprocess.run(argv, cwd=cwd, env=env, stdin=subprocess.DEVNULL,
                    stdout=out, stderr=subprocess.STDOUT, timeout=timeout, check=False)
        else:
            result = subprocess.run(argv, cwd=cwd, env=env,
                input=input_bytes, stdout=subprocess.PIPE,
                stderr=subprocess.PIPE, timeout=timeout, check=False)
    except subprocess.TimeoutExpired:
        raise Stop("SUBPROCESS_TIMEOUT_UNKNOWN_NO_AUTOMATIC_RETRY") from None
    except OSError:
        raise Stop("SUBPROCESS_UNAVAILABLE_NO_RETRY") from None
    if result.returncode != 0:
        raise Stop("APPROVED_COMMAND_FAILED_NO_RETRY")
    if log is not None:
        return ""
    if len(result.stdout) > 1048576:
        raise Stop("COMMAND_STDOUT_TOO_LARGE")
    return result.stdout.decode("utf-8", "strict").strip()

def isolated_owner_env():
    need(platform.system()=="Linux" and os.geteuid()==0
         and "microsoft" in platform.release().lower(), "ROOT_WSL_REQUIRED")
    need(sys.argv[1:]==[FLAG], "EXACT_FOUR_IMAGES_OWNER_APPROVAL_FLAG_REQUIRED")
    need(not MARK.exists() and not MARK.is_symlink(), "H2AI_MARKER_ALREADY_CONSUMED_DO_NOT_REPEAT")
    need(SDK.is_dir() and not SDK.is_symlink() and SDK.stat().st_uid==0,
         "NATIVE_GCLOUD_SDK_UNTRUSTED")
    need(GCLOUD.is_file() and GCLOUD.stat().st_uid==0
         and os.access(GCLOUD,os.X_OK), "NATIVE_GCLOUD_UNTRUSTED")
    python = PY.resolve(strict=True)
    need(python.is_relative_to(SDK.resolve(strict=True))
         and python.is_file() and os.access(python,os.X_OK),
         "NATIVE_GCLOUD_PYTHON_UNTRUSTED")
    need(CONFIG.is_dir() and not CONFIG.is_symlink()
         and CONFIG.stat().st_uid==0, "NATIVE_OWNER_CONFIG_UNTRUSTED")
    env=dict(os.environ)
    env.update({"HOME":str(ROOT),"CLOUDSDK_CONFIG":str(CONFIG),
                "CLOUDSDK_PYTHON":str(PY),
                "CLOUDSDK_CORE_DISABLE_USAGE_REPORTING":"1",
                "CLOUDSDK_COMPONENT_MANAGER_DISABLE_UPDATE_CHECK":"1",
                "CLOUDSDK_CORE_CHECK_GCE_METADATA":"false",
                "GIT_TERMINAL_PROMPT":"0","GCM_INTERACTIVE":"never"})
    env.pop("GOOGLE_APPLICATION_CREDENTIALS",None)
    env.pop("CLOUDSDK_AUTH_CREDENTIAL_FILE_OVERRIDE",None)
    def cloud(args,timeout=35):
        return command([str(GCLOUD),"--quiet",*args],env=env,timeout=timeout)
    need(cloud(["auth","list","--filter=status:ACTIVE",
                "--format=value(account)"])==OWNER,"WRONG_ACTIVE_OWNER")
    need(cloud(["config","get-value","project"])==PROJECT,"WRONG_PROJECT")
    # A single read-only API call validates that the expected repository exists.
    info=json.loads(cloud(["--project="+PROJECT,"artifacts","repositories",
       "describe",REPOSITORY,"--location="+REGION,"--format=json"]))
    need(info.get("name")==f"projects/{PROJECT}/locations/{REGION}/repositories/{REPOSITORY}"
         and info.get("format")=="DOCKER","WRONG_PRIVATE_ARTIFACT_REPOSITORY")
    return env,cloud

def preflight_docker(env):
    need(shutil.which("docker") is not None,"DOCKER_UNAVAILABLE_WSL")
    need(shutil.which("node") is not None,"NODE_UNAVAILABLE_WSL")
    need(shutil.which("git") is not None,"GIT_UNAVAILABLE_WSL")
    v=command(["node","--version"],env=env)
    need(re.fullmatch(r"v([0-9]+)\.[0-9]+\.[0-9]+",v)!=None
         and int(v.split(".")[0][1:])>=24,"NODE24_OR_NEWER_REQUIRED")
    command(["docker","buildx","version"],env=env)
    os_type=command(["docker","info","--format","{{.OSType}}"],env=env,timeout=35)
    need(os_type=="linux","LINUX_DOCKER_ENGINE_REQUIRED")
    free=shutil.disk_usage(ROOT).free
    need(free>=6*1024**3,"LESS_THAN_6_GIB_ROOT_FREE_STOP")
    return v

def prepare_source(evidence,env):
    checkout=evidence/"source"
    # Never operate in or reset Owner's local dirty checkout.
    command(["git","-c","credential.helper=","clone","--quiet","--depth","25",
             "--single-branch","--branch",BRANCH,REPO_URL,str(checkout)],
            env=env,timeout=180)
    revision=command(["git","rev-parse","HEAD"],cwd=checkout,env=env)
    need(re.fullmatch(r"[a-f0-9]{40}",revision)!=None,
         "SOURCE_REVISION_INVALID")
    command(["git","cat-file","-e",APPROVED_SOURCE+"^{commit}"],cwd=checkout,env=env)
    command(["git","merge-base","--is-ancestor",APPROVED_SOURCE,revision],
            cwd=checkout,env=env)
    dirty=command(["git","status","--porcelain"],cwd=checkout,env=env)
    need(dirty=="","SOURCE_CHECKOUT_NOT_CLEAN")
    # Only documentation, AGENTS, tests and THIS new runner may differ from
    # the approved source: imported source closure / locks must not drift.
    changed=command(["git","diff","--name-only",APPROVED_SOURCE,revision,
                     "--","features","functions","deployment/four-role","scripts"],
                     cwd=checkout,env=env)
    changed_paths=[s for s in changed.splitlines() if s]
    need(all(s=="scripts/step05_h2ai_four_off_images_build_push_once_20261128.py"
             for s in changed_paths),"APPROVED_SOURCE_OR_LOCKS_DRIFT_STOP")
    bundles={}
    for role in ROLES:
        context=evidence/("context-"+role)
        stdout=command(["node","scripts/step05-h2ah-source-package.mjs",
                        "--prepare-source-only",role,str(context)],
                        cwd=checkout,env=env,timeout=60)
        obj=json.loads(stdout)
        need(obj.get("role")==role and obj.get("sourceRevision")==revision
             and obj.get("context")==str(context) and
             re.fullmatch(r"[a-f0-9]{64}",obj.get("provenanceSha256",""))!=None,
             "SOURCE_CLOSURE_PROVENANCE_DRIFT")
        df=context/"deployment/four-role"/("Dockerfile."+role)
        source=df.read_text(encoding="utf-8")
        need("FROM --platform=linux/amd64 gcr.io/distroless/nodejs24-debian13:nonroot@sha256:"+IMMUTABLE_BASE in source,
             "RUNTIME_BASE_PIN_CHANGED")
        if role in ("mediator","backend"):
            need("FROM --platform=linux/amd64 node:24-bookworm-slim@sha256:"+IMMUTABLE_BUILDER in source,
                 "DEPENDENCY_BUILDER_PIN_CHANGED")
        need(source.count("\nFROM ")<=1, "UNEXPECTED_ADDITIONAL_DOCKER_BASE")
        need("USER root" not in source and "--chown=65532:65532" in source,
             "NONROOT_DOCKER_BOUNDARY_CHANGED")
        need((context/"deployment/four-role"/("Dockerfile."+role+".dockerignore")).is_file(),
             "DOCKERIGNORE_MISSING")
        bundles[role]={"context":str(context),"provenanceSha256":obj["provenanceSha256"],
                       "closureFileCount":obj.get("files")}
    return revision,bundles

def mark(text):
    with MARK.open("a",encoding="utf-8") as f:
        f.write(text+"\n")

def describe_pushed_image(ref,env):
    raw=command(["docker","buildx","imagetools","inspect","--raw",ref],
                env=env,timeout=100)
    item=json.loads(raw)
    manifests=item.get("manifests")
    if isinstance(manifests,list):
        real=[m for m in manifests if isinstance(m,dict)
              and m.get("platform",{}).get("os")=="linux"
              and m.get("platform",{}).get("architecture")=="amd64"]
        need(len(real)==1 and HEX64.fullmatch(real[0].get("digest","")) is not None,
             "CHILD_AMD64_DIGEST_MISSING_OR_MULTIPLE_STOP")
        child=real[0]["digest"]
    else:
        need(item.get("mediaType") in
             ("application/vnd.oci.image.manifest.v1+json",
              "application/vnd.docker.distribution.manifest.v2+json"),
             "REGISTRY_IMAGE_MANIFEST_UNKNOWN")
        child="USE_ROOT_MANIFEST_DIGEST"
    return child,hashlib.sha256(raw.encode()).hexdigest()

def main():
    os.umask(0o077)
    try:
        env,cloud=isolated_owner_env()
        node_version=preflight_docker(env)
        print("H2AI_PREFLIGHT=OWNER_PROJECT_REPOSITORY_NODE_DOCKER_DISK_PASS",flush=True)
    except (Stop,OSError,ValueError,TypeError,KeyError,UnicodeError) as e:
        print("H2AI_RESULT=STOP_BEFORE_ANY_CLOUD_REGISTRY_WRITE")
        print("H2AI_REASON="+(str(e) if isinstance(e,Stop) else type(e).__name__))
        print("H2AI_RETRY=NO_REGISTRY_WRITE_STARTED_CHECK_EXACT_ERROR_FIRST")
        return 2
    evidence=ROOT/("oldx-h2ai-four-builds-"+datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
                   +"-"+secrets.token_hex(3))
    try:
        evidence.mkdir(mode=0o700)
        revision,bundles=prepare_source(evidence,env)
        tag="h2ai-"+revision[:12]+"-"+secrets.token_hex(6)
        need(re.fullmatch(r"h2ai-[a-f0-9]{12}-[a-f0-9]{12}",tag)!=None,"TAG_INVALID")
        docker_config=evidence/"private-docker-config"
        docker_config.mkdir(mode=0o700)
        local_env=dict(env)
        local_env.update({"DOCKER_CONFIG":str(docker_config),
                          "DOCKER_DEFAULT_PLATFORM":"linux/amd64",
                          "DOCKER_BUILDKIT":"1"})
        access_token=cloud(["--account="+OWNER,"--project="+PROJECT,
                            "auth","print-access-token"])
        need(TOKEN.fullmatch(access_token)!=None, "OWNER_OAUTH_TOKEN_INVALID")
        # This stores ONLY a short-lived token in an exclusive PRIVATE temp
        # Docker config. Do not use gcloud auth configure-docker globally.
        command(["docker","login","-u","oauth2accesstoken",
                 "--password-stdin","https://"+REGISTRY],env=local_env,
                input_bytes=(access_token+"\n").encode(),timeout=40)
        access_token=None
        print("H2AI_SOURCE_BUNDLES=FOUR_READY_EXACT_APPROVED_SOURCE",flush=True)
    except (Stop,OSError,ValueError,TypeError,KeyError,UnicodeError) as e:
        print("H2AI_RESULT=STOP_BEFORE_ANY_BUILD_OR_PUSH")
        print("H2AI_REASON="+(str(e) if isinstance(e,Stop) else type(e).__name__))
        print("H2AI_NO_REGISTRY_BUILD_OR_PUSH=TRUE")
        return 2

    receipts={"sourceApproved":APPROVED_SOURCE,"sourceRevision":revision,
              "node":node_version,"tag":tag,"project":PROJECT,
              "roles":{},"outcome":"UNKNOWN_OR_PARTIAL"}
    try:
        fd=os.open(str(MARK),os.O_CREAT|os.O_EXCL|os.O_WRONLY|
                   getattr(os,"O_NOFOLLOW",0),0o600)
        with os.fdopen(fd,"w",encoding="utf-8") as f:
            f.write("ATTEMPT_CONSUMED=TRUE\nPROJECT="+PROJECT+"\n")
            f.write("APPROVED_SOURCE="+APPROVED_SOURCE+"\nREVISION="+revision+"\n")
            f.write("EVIDENCE="+str(evidence)+"\nTAG="+tag+"\n")
        print("H2AI_MARKER=CONSUMED_NO_REPEAT",flush=True)
        for role in ROLES:
            ref=IMAGES[role]+":"+tag
            # A fresh unpredictable tag in a separately named target.
            # A failure/unknown after invocation consumes this role's attempt.
            mark("ROLE="+role+" ONE_BUILD_AND_PUSH_ABOUT_TO_START=TRUE")
            receipts["roles"][role]={"ref":ref,
                   "sourceProvenanceSha256":bundles[role]["provenanceSha256"],
                   "buildPushAttempted":True}
            print("H2AI_BUILD_PUSH_START="+role,flush=True)
            log=evidence/("private-build-"+role+".log")
            metadata=evidence/("private-build-"+role+"-metadata.json")
            command(["docker","buildx","build","--platform","linux/amd64",
                     "--progress","plain","--provenance=true","--sbom=true",
                     "--push","--metadata-file",str(metadata),
                     "--file","deployment/four-role/Dockerfile."+role,
                     "--tag",ref,bundles[role]["context"]],
                    env=local_env,timeout=3600,log=log)
            meta=json.loads(metadata.read_text(encoding="utf-8"))
            index=meta.get("containerimage.digest","")
            need(HEX64.fullmatch(index)!=None,"REGISTRY_INDEX_DIGEST_NOT_RECORDED")
            child,manifest_sha256=describe_pushed_image(ref,local_env)
            if child=="USE_ROOT_MANIFEST_DIGEST":
                child=index
            need(HEX64.fullmatch(child)!=None and child[7:] not in
                 OLD_OFF|{IMMUTABLE_BASE,IMMUTABLE_BUILDER},
                 "IMAGE_CHILD_DIGEST_OLD_OR_MISSING")
            receipts["roles"][role].update({
                "registryIndexDigest":index,"linuxAmd64ChildDigest":child,
                "rawManifestSha256":manifest_sha256,"readbackVerified":True,
                "buildLogSha256":hashlib.sha256(log.read_bytes()).hexdigest()})
            mark("ROLE="+role+" REGISTRY_INDEX="+index+" AMD64_CHILD="+child)
            print("H2AI_IMAGE_PUSH_AND_AMD64_DIGEST_VERIFIED="+role+" "+child,
                  flush=True)
        need(len(receipts["roles"])==4
             and all(v.get("readbackVerified") for v in receipts["roles"].values())
             and len({v["linuxAmd64ChildDigest"] for v in receipts["roles"].values()})==4,
             "FOUR_DISTINCT_IMAGES_NOT_VERIFIED")
        receipts["outcome"]="PASS_FOUR_NEW_PRIVATE_OFF_IMAGES"
        result="PASS_FOUR_NEW_PRIVATE_OFF_IMAGES"
    except (Stop,OSError,ValueError,TypeError,UnicodeError,KeyError) as e:
        result="STOP_AFTER_MARKER_POSSIBLE_PARTIAL_REGISTRY_WRITES"
        receipts["outcome"]=result
        receipts["reason"]=str(e) if isinstance(e,Stop) else type(e).__name__
    finally:
        # Evidence is private ROOT-owned; do not log bearer tokens.
        try:
            (evidence/"sanitized-h2ai-summary.json").write_text(
                json.dumps(receipts,sort_keys=True,indent=2)+"\n",encoding="utf-8")
            mark("RESULT="+result)
            shutil.rmtree(docker_config,ignore_errors=True)
        except OSError:
            result="STOP_EVIDENCE_WRITE"
        print("H2AI_RESULT="+result)
        print("H2AI_SOURCE_REVISION="+revision)
        print("H2AI_PRIVATE_EVIDENCE="+str(evidence))
        print("H2AI_DOCKER_CONFIG=TEMPORARY_NOT_GLOBAL")
        print("H2AI_CLOUD_RUN_IAM_KMS_FIRESTORE_DEPLOYMENT=NONE")
        print("H2AI_H2_PRODUCTION=NO_GO")
        print("H2AI_DO_NOT_REPEAT=TRUE")
        print("H2AI_REASON="+receipts.get("reason","NONE"))
    return 0 if result=="PASS_FOUR_NEW_PRIVATE_OFF_IMAGES" else 2

if __name__=="__main__":
    sys.exit(main())
