#!/usr/bin/env python3
"""OLDX Step05 H1B G2B: ONE retained H1A image Docker push + remote immutable digest validation.

Authorised scope: native Owner WSL / existing isolated G2 credentials / oldx-staging Mumbai
existing Artifact Registry only. No rebuild, no scan, no Cloud Run, IAM, Firebase or cleanup.
One-shot consumed before first Docker tag/push. A failure must NOT trigger a retry.
"""
from __future__ import annotations
import base64
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import platform
import re
import secrets
import ssl
import stat
import subprocess
import sys
from urllib import request, error

OWNER = "yasminparmar087@gmail.com"
PROJECT = "oldx-staging"
REGION = "asia-south1"
REGISTRY = "asia-south1-docker.pkg.dev"
REPOSITORY = "oldx-staging-images"
NAME = "oldx-c2-mediator-off"
IMAGE = f"{REGISTRY}/{PROJECT}/{REPOSITORY}/{NAME}"
ORIGINAL = "oldx-h1a-c2-mediator-off:local-20261124t195244z"
FROZEN_LOCAL_ID = "sha256:576a1faa599459ed9b1cdeccc01a3adc2076dffff617bec42f38df7d3a75663e"
FROZEN_CHILD = "sha256:2e555bd98424d29b32a7bb3409a45e2c257569ff632085e4ff0e3a9ab4413b5f"
FROZEN_CONFIG = "sha256:c71c7268e08f9ed91a92fd4e82e499a7331c3a071985cebcede7d76efbdf5b71"

ROOT = Path("/root")
BASE = ROOT / "oldx-tools"
SDK = BASE / "native-gcloud-594.0.1/google-cloud-sdk"
CLI = SDK / "bin/gcloud"
PYTHON = SDK / "platform/bundledpythonunix/bin/python3"
G2_CONFIG = BASE / "oldx-h1b-g2-20261126-cloudsdk-config"
DOCKER_CONFIG = BASE / "oldx-h1b-g2-20261126-docker-config"
G2_RECOVERY = ROOT / ".oldx-h1b-g2a-terminal-stdin-recovery-once-20261126"
G2_OLD = ROOT / ".oldx-h1b-g2-wsl-owner-login-once-20261126"
MARKER = ROOT / ".oldx-h1b-g2b-retained-single-push-once-20261126"

MEDIA = ", ".join((
    "application/vnd.oci.image.index.v1+json",
    "application/vnd.docker.distribution.manifest.list.v2+json",
    "application/vnd.oci.image.manifest.v1+json",
    "application/vnd.docker.distribution.manifest.v2+json",
))
MANIFEST_TYPES = {
    "application/vnd.oci.image.manifest.v1+json",
    "application/vnd.docker.distribution.manifest.v2+json",
}
INDEX_TYPES = {
    "application/vnd.oci.image.index.v1+json",
    "application/vnd.docker.distribution.manifest.list.v2+json",
}
class Stop(Exception):
    pass

def must(condition, reason):
    if not condition:
        raise Stop(reason)

def run(cmd, env, timeout=30):
    try:
        return subprocess.run(cmd, stdin=subprocess.DEVNULL, stdout=subprocess.PIPE,
            stderr=subprocess.PIPE, env=env, timeout=timeout, check=False)
    except subprocess.TimeoutExpired as exc:
        raise Stop("COMMAND_TIMEOUT_" + Path(cmd[0]).name) from exc

class NoRedirect(request.HTTPRedirectHandler):
    def redirect_request(self, *args, **kwargs):
        return None

OPENER = request.build_opener(request.ProxyHandler({}),
    request.HTTPSHandler(context=ssl.create_default_context()), NoRedirect())

def http(method, url, token, accept, limit=2097152):
    must(url.startswith("https://"), "NON_HTTPS_URL")
    # A basic credential bearing a short-lived OAuth token is used only for this exact registry host.
    from urllib.parse import urlsplit
    host = urlsplit(url).hostname
    must(host in {REGISTRY, "artifactregistry.googleapis.com"}, "UNEXPECTED_HTTP_HOST")
    if host == REGISTRY:
        basic = base64.b64encode(("oauth2accesstoken:" + token).encode("utf-8")).decode("ascii")
        auth = "Basic " + basic
    else:
        auth = "Bearer " + token
    req = request.Request(url, method=method, headers={
        "Authorization": auth, "Accept": accept,
        "User-Agent": "OLDX-H1B-G2B-reuse-single-push/1"})
    try:
        with OPENER.open(req, timeout=35) as resp:
            must(resp.status == 200, "UNEXPECTED_HTTP_SUCCESS_STATUS")
            payload = b"" if method == "HEAD" else resp.read(limit + 1)
            must(len(payload) <= limit, "HTTP_PAYLOAD_TOO_LARGE")
            return 200, payload, resp.headers
    except error.HTTPError as exc:
        status = exc.code
        exc.close()
        return status, b"", {}

def safe_json(raw):
    try:
        obj = json.loads(raw)
    except (ValueError, UnicodeError):
        raise Stop("REMOTE_INVALID_JSON") from None
    must(isinstance(obj, dict), "REMOTE_SCHEMA_INVALID")
    return obj

def manifest(url, token):
    status, raw, headers = http("GET", url, token, MEDIA)
    must(status == 200, "REMOTE_MANIFEST_HTTP_" + str(status))
    must(len(raw) > 0, "REMOTE_MANIFEST_EMPTY")
    digest = "sha256:" + hashlib.sha256(raw).hexdigest()
    header_digest = headers.get("Docker-Content-Digest", "")
    must(not header_digest or header_digest == digest, "REMOTE_MANIFEST_HEADER_DIGEST_MISMATCH")
    obj = safe_json(raw)
    return digest, obj

def verified_remote(token, tag):
    tag_url = f"https://{REGISTRY}/v2/{PROJECT}/{REPOSITORY}/{NAME}/manifests/{tag}"
    remote_digest, obj = manifest(tag_url, token)
    kind = obj.get("mediaType", "")
    if kind in INDEX_TYPES:
        entries = obj.get("manifests")
        must(isinstance(entries, list), "REMOTE_INDEX_MANIFESTS_BAD")
        matches = [e for e in entries if isinstance(e, dict) and
            isinstance(e.get("platform"), dict) and
            e["platform"].get("os") == "linux" and
            e["platform"].get("architecture") == "amd64"]
        must(len(matches) == 1, "REMOTE_AMD64_MANIFEST_NOT_UNIQUE")
        child = matches[0].get("digest")
        must(isinstance(child, str) and re.fullmatch(r"sha256:[a-f0-9]{64}", child),
            "REMOTE_CHILD_DIGEST_INVALID")
        child_url = f"https://{REGISTRY}/v2/{PROJECT}/{REPOSITORY}/{NAME}/manifests/{child}"
        read_digest, child_obj = manifest(child_url, token)
        must(read_digest == child, "REMOTE_CHILD_DIGEST_WRONG")
    elif kind in MANIFEST_TYPES:
        child = remote_digest
        child_obj = obj
    else:
        raise Stop("REMOTE_MANIFEST_MEDIA_TYPE_UNSUPPORTED")
    config = child_obj.get("config")
    must(isinstance(config, dict), "REMOTE_CONFIG_MISSING")
    config_digest = config.get("digest")
    must(config_digest == FROZEN_CONFIG, "REMOTE_FROZEN_CONFIG_MISMATCH")
    must(child == FROZEN_CHILD, "REMOTE_CHILD_DIFFERS_FROZEN_SOURCE")
    return {"remote_tag": tag, "remote_index_or_manifest": remote_digest,
            "remote_amd64_child": child, "remote_config": config_digest,
            "status": "MATCHES_FROZEN_AMD64_CHILD_AND_CONFIG"}

def preflight():
    must(sys.argv[1:] == ["--h1b-g2b-retained-image-push-once"], "EXACT_FLAG_REQUIRED")
    must(platform.system() == "Linux" and
        "microsoft" in platform.release().lower() and os.geteuid() == 0,
        "OWNER_ROOT_WSL_REQUIRED")
    must(not MARKER.exists() and not MARKER.is_symlink(), "ONESHOT_ALREADY_CONSUMED")
    must(CLI.is_file() and os.access(CLI, os.X_OK) and not CLI.is_symlink(),
        "NATIVE_GCLOUD_MISSING")
    sdk = SDK.resolve(strict=True)
    must(sdk == SDK and SDK.stat().st_uid == 0, "SDK_IDENTITY_MISMATCH")
    py = PYTHON.resolve(strict=True)
    must(py.is_relative_to(sdk) and py.stat().st_uid == 0 and
        py.is_file() and os.access(py, os.X_OK), "PYTHON_OUTSIDE_FROZEN_SDK")
    must(G2_CONFIG.is_dir() and not G2_CONFIG.is_symlink() and
        G2_CONFIG.stat().st_uid == 0 and
        DOCKER_CONFIG.is_dir() and not DOCKER_CONFIG.is_symlink() and
        DOCKER_CONFIG.stat().st_uid == 0, "ISOLATED_G2_CONFIGS_MISSING")
    must(G2_OLD.is_file() and not G2_OLD.is_symlink() and
        "ATTEMPT_CONSUMED=TRUE" in G2_OLD.read_text().splitlines(),
        "OLD_G2A_MARKER_NOT_CONSUMED")
    must(G2_RECOVERY.is_file() and not G2_RECOVERY.is_symlink() and
        "RESULT=LOGIN_AND_ISOLATED_DOCKER_HELPER_READY" in
        G2_RECOVERY.read_text().splitlines(), "G2_RECOVERY_NOT_VERIFIED")
    cfg_path = DOCKER_CONFIG / "config.json"
    must(cfg_path.is_file() and not cfg_path.is_symlink() and
        cfg_path.stat().st_uid == 0, "DOCKER_HELPER_CONFIG_MISSING")
    cfg = safe_json(cfg_path.read_bytes())
    must(cfg == {"credHelpers": {REGISTRY: "gcloud"}}, "DOCKER_HELPER_NOT_EXACTLY_SINGLE_HOST")
    env = dict(os.environ)
    env.update({
        "HOME": str(ROOT),
        "PATH": f"{SDK}/bin:/usr/bin:/bin",
        "CLOUDSDK_CONFIG": str(G2_CONFIG),
        "DOCKER_CONFIG": str(DOCKER_CONFIG),
        "CLOUDSDK_PYTHON": str(PYTHON),
        "CLOUDSDK_CORE_DISABLE_USAGE_REPORTING": "1",
        "CLOUDSDK_COMPONENT_MANAGER_DISABLE_UPDATE_CHECK": "1",
        "CLOUDSDK_CORE_CHECK_GCE_METADATA": "false",
    })
    for key in ("GOOGLE_APPLICATION_CREDENTIALS", "CLOUDSDK_AUTH_CREDENTIAL_FILE_OVERRIDE"):
        env.pop(key, None)
    owner = run([str(CLI), "auth", "list", "--filter=status:ACTIVE",
                 "--format=value(account)"], env)
    must(owner.returncode == 0 and owner.stdout.decode().strip() == OWNER,
         "OWNER_ACCOUNT_NOT_VERIFIED")
    project = run([str(CLI), "config", "get-value", "project"], env)
    must(project.returncode == 0 and project.stdout.decode().strip() == PROJECT,
         "PROJECT_NOT_VERIFIED")
    docker = run(["docker", "image", "inspect", "--format={{.Id}}", ORIGINAL], env)
    must(docker.returncode == 0 and docker.stdout.decode().strip() == FROZEN_LOCAL_ID,
         "RETAINED_LOCAL_IMAGE_MISMATCH")
    arch = run(["docker", "image", "inspect", "--format={{.Os}}/{{.Architecture}}",
                ORIGINAL], env)
    must(arch.returncode == 0 and arch.stdout.decode().strip() == "linux/amd64",
         "LOCAL_IMAGE_ARCH_NOT_LINUX_AMD64")
    cred = run([str(CLI), "--quiet", "--account=" + OWNER, "auth",
                "print-access-token"], env)
    token = cred.stdout.decode("ascii", errors="ignore").strip()
    must(cred.returncode == 0 and re.fullmatch(r"[A-Za-z0-9._~+-]{40,4096}", token),
         "ISOLATED_OWNER_ACCESS_TOKEN_UNAVAILABLE")
    repo_url = (f"https://artifactregistry.googleapis.com/v1/projects/{PROJECT}"
                f"/locations/{REGION}/repositories/{REPOSITORY}")
    status, data, _ = http("GET", repo_url, token, "application/json")
    must(status == 200, "EXISTING_REPOSITORY_HTTP_" + str(status))
    repository = safe_json(data)
    must(repository.get("format") == "DOCKER" and
         repository.get("name") ==
         f"projects/{PROJECT}/locations/{REGION}/repositories/{REPOSITORY}",
         "EXISTING_REPOSITORY_IDENTITY_MISMATCH")
    return env, token

def main():
    os.umask(0o077)
    try:
        env, token = preflight()
        tag = ("h1b-g2b-20261126-" + secrets.token_hex(10))
        remote = IMAGE + ":" + tag
        status, _, _ = http(
            "HEAD", f"https://{REGISTRY}/v2/{PROJECT}/{REPOSITORY}/{NAME}/manifests/{tag}",
            token, MEDIA)
        must(status == 404, "TAG_COLLISION_OR_REGISTRY_HTTP_" + str(status))
        existing_local = run(["docker", "image", "inspect", "--format={{.Id}}",
                              remote], env)
        must(existing_local.returncode != 0, "REMOTE_TAG_ALREADY_PRESENT_LOCALLY")
    except (Stop, OSError, ValueError, subprocess.SubprocessError) as exc:
        print("H1B_G2B_RESULT=STOP_PREFLIGHT")
        print("H1B_G2B_REASON=" + (str(exc) if isinstance(exc, Stop) else
                                  type(exc).__name__))
        print("H1B_G2B_REGISTRY_PUSH=NOT_ATTEMPTED")
        return 2
    evidence = ROOT / ("oldx-h1b-g2b-evidence-" +
        datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ"))
    try:
        evidence.mkdir(mode=0o700)
        with MARKER.open("x") as fd:
            fd.write("ATTEMPT_CONSUMED=TRUE\nEVIDENCE=" + str(evidence) +
                     "\nTAG=" + tag + "\n")
        os.chmod(MARKER, 0o600)
    except (OSError, FileExistsError):
        print("H1B_G2B_RESULT=STOP_MARKER_OR_EVIDENCE_CREATE")
        return 2
    outcome = "STOP_AFTER_MARKER"
    reason = "UNKNOWN"
    digest = None
    push_attempt = False
    try:
        tagged = run(["docker", "tag", ORIGINAL, remote], env, timeout=30)
        must(tagged.returncode == 0, "LOCAL_DOCKER_TAG_FAILED")
        # Recheck the exact new tag, after local retag and immediately before upload.
        status, _, _ = http(
            "HEAD", f"https://{REGISTRY}/v2/{PROJECT}/{REPOSITORY}/{NAME}/manifests/{tag}",
            token, MEDIA)
        must(status == 404, "REMOTE_TAG_NOT_EMPTY_BEFORE_PUSH_" + str(status))
        print("H1B_G2B_STAGE=ONE_AUTHORIZED_PUSH_ATTEMPT", flush=True)
        push_attempt = True
        with (evidence / "docker-push.stdout").open("wb") as out, \
             (evidence / "docker-push.stderr").open("wb") as err:
            try:
                result = subprocess.run(["docker", "push", remote],
                     env=env, stdin=subprocess.DEVNULL, stdout=out,
                     stderr=err, timeout=900, check=False)
                push_ok = result.returncode == 0
            except subprocess.TimeoutExpired:
                raise Stop("DOCKER_PUSH_TIMEOUT_NO_RETRY") from None
        must(push_ok, "DOCKER_PUSH_NONZERO_NO_RETRY")
        digest = verified_remote(token, tag)
        with (evidence / "sanitized-result.json").open("x") as fd:
            json.dump(digest, fd, indent=2, sort_keys=True)
            fd.write("\n")
        outcome = "PASS_REMOTE_FROZEN_DIGEST_VERIFIED"
        reason = "ONE_PUSH_VERIFIED"
        print("H1B_G2B_REMOTE_DIGEST=" + digest["remote_index_or_manifest"])
        print("H1B_G2B_REMOTE_AMD64_CHILD=" + digest["remote_amd64_child"])
        print("H1B_G2B_REMOTE_CONFIG=" + digest["remote_config"])
    except (Stop, OSError, ValueError, subprocess.SubprocessError) as exc:
        reason = str(exc) if isinstance(exc, Stop) else type(exc).__name__
    finally:
        with MARKER.open("a") as fd:
            fd.write("RESULT=" + outcome + "\nREASON=" + reason + "\n")
        print("H1B_G2B_TAG=" + tag)
        print("H1B_G2B_PUSH_ATTEMPTED=" + str(push_attempt).upper())
        print("H1B_G2B_RESULT=" + outcome)
        print("H1B_G2B_REASON=" + reason)
        print("H1B_G2B_CLOUD_RUN_OR_IAM_WRITES=NONE")
        print("H1B_G2B_DO_NOT_REPEAT=TRUE")
    return 0 if outcome == "PASS_REMOTE_FROZEN_DIGEST_VERIFIED" else 2

if __name__ == "__main__":
    sys.exit(main())
