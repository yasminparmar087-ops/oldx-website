#!/usr/bin/env python3
"""OLDX Step04 C1: one owner-approved NEW private Docker Registry copy.

Usage: --preflight (no writes), then after confirming output --execute (one
single push; persistent consumed journal). Works from the owner's WSL only.
No image builds, Grype scans, IAM/Billing/Cloud Run/Rules/API changes or signing.
Never re-run --execute after a started push or an ambiguous outcome.
"""
import argparse
import json
import os
from pathlib import Path
import re
import subprocess
import sys
import tempfile
import time

ACCOUNT = "yasminparmar087@gmail.com"
PROJECT = "oldx-staging"
LOCATION = "asia-south1"
REPOSITORY = "oldx-staging-images"
PACKAGE = "oldx-npmfree-20261121-a1"
TAG = "c1-20261121-a1"
REGISTRY = "asia-south1-docker.pkg.dev"
SOURCE = "oldx-bellsoft-npmfree:20261120-a1"
SOURCE_ID = "sha256:0844b637cf1bfedef60caa6a54ad515ebf9c0a937453b409101ad0d2ff254f79"
TARGET = f"{REGISTRY}/{PROJECT}/{REPOSITORY}/{PACKAGE}:{TAG}"
ROOT = Path("/mnt/d/OLDX/G2")
JOURNAL = ROOT / "oldx-npmfree-c1-single-push-20261121-a1.json"
WIN_GCLOUD = r"D:\Temp\google-cloud-sdk\bin\gcloud.cmd"
WSL_GCLOUD = Path("/mnt/d/Temp/google-cloud-sdk/bin/gcloud.cmd")
WIN_CMD = Path("/mnt/c/Windows/System32/cmd.exe")
DIGEST = re.compile(r"sha256:[a-f0-9]{64}\Z")
TOKEN = re.compile(r"[A-Za-z0-9_.~+/\-]{30,8192}\Z")
STOP_CODES = {
    "C1_SOURCE_IMAGE_CHANGED",
    "C1_OLD_OR_NEW_PACKAGE_CONFLICT",
    "C1_AUTH_BRIDGE_UNAVAILABLE",
    "C1_SCANNING_NOT_DISABLED",
    "C1_LOCAL_DOCKER_NOT_TRUSTED",
}

class Stop(Exception):
    pass

def require(ok, reason):
    if not ok:
        raise Stop(reason)

def invoke(args, *, input_text=None, timeout=40, quiet=False):
    try:
        p = subprocess.run(args, input=input_text, text=True, stdout=subprocess.PIPE,
                           stderr=subprocess.PIPE, timeout=timeout, check=False)
    except (OSError, subprocess.TimeoutExpired) as exc:
        raise Stop("LOCAL_COMMAND_FAILED_OR_TIMED_OUT") from exc
    # NEVER expose stderr: Docker/Windows may include credential or local paths.
    require(p.returncode == 0, "LOCAL_COMMAND_NONZERO")
    require(len(p.stdout) <= 2_000_000, "LOCAL_COMMAND_OUTPUT_TOO_LARGE")
    return "" if quiet else p.stdout.strip()

def gcloud(*args, allow_not_found=False):
    require(WSL_GCLOUD.is_file() and WIN_CMD.is_file(), "C1_AUTH_BRIDGE_UNAVAILABLE")
    argv = [str(WIN_CMD), "/d", "/c", WIN_GCLOUD, *args]
    try:
        proc = subprocess.run(argv, stdin=subprocess.DEVNULL, capture_output=True,
                              text=True, timeout=60, check=False)
    except (OSError, subprocess.TimeoutExpired) as exc:
        raise Stop("C1_AUTH_BRIDGE_UNAVAILABLE") from exc
    require(len(proc.stdout) < 2_000_000 and len(proc.stderr) < 2_000_000,
            "C1_CLOUD_OUTPUT_TOO_LARGE")
    if proc.returncode:
        if allow_not_found and "NOT_FOUND:" in proc.stderr and "packages.describe" in proc.stderr:
            return None
        raise Stop("C1_GCLOUD_READ_FAILED")
    return proc.stdout.strip()

def review_local(image, context, endpoint, env):
    require(context in {"default", "desktop-linux"} and
            isinstance(endpoint, str) and endpoint.startswith("unix:///") and
            not any(env.get(k) for k in
                    ("DOCKER_HOST", "DOCKER_CONTEXT", "DOCKER_CERT_PATH", "DOCKER_TLS_VERIFY")),
            "C1_LOCAL_DOCKER_NOT_TRUSTED")
    require(isinstance(image, list) and len(image) == 1 and isinstance(image[0], dict),
            "C1_IMAGE_INSPECT_INVALID")
    info = image[0]
    cfg = info.get("Config") or {}
    require(info.get("Id") == SOURCE_ID and SOURCE in (info.get("RepoTags") or []) and
            info.get("Os") == "linux" and info.get("Architecture") == "amd64" and
            isinstance(cfg, dict) and cfg.get("User") == "appuser" and
            cfg.get("Entrypoint") == ["/usr/bin/node"] and
            cfg.get("Cmd") == ["functions/staging-marketplace/product-read-server.mjs"] and
            type(info.get("Size")) is int and 0 < info["Size"] <= 8 * 1024 ** 3,
            "C1_SOURCE_IMAGE_CHANGED")
    return info["Size"]

def validate_repo(config, package_reply, impersonated):
    require(impersonated in {"", "(unset)"}, "C1_IMPERSONATION_NOT_ALLOWED")
    require(isinstance(config, dict) and
            config.get("name") ==
            f"projects/{PROJECT}/locations/{LOCATION}/repositories/{REPOSITORY}" and
            config.get("format") == "DOCKER" and
            config.get("mode") == "STANDARD_REPOSITORY",
            "C1_REPO_CONFIG_CHANGED")
    scanning = config.get("vulnerabilityScanningConfig") or {}
    require(scanning.get("enablementState") == "SCANNING_DISABLED",
            "C1_SCANNING_NOT_DISABLED")
    require(package_reply is None, "C1_OLD_OR_NEW_PACKAGE_CONFLICT")

def probe(*, obtain_token=False):
    require(ROOT.is_dir() and not ROOT.is_symlink() and
            "microsoft" in Path("/proc/version").read_text().lower(),
            "C1_OWNER_WSL_REQUIRED")
    require(not JOURNAL.exists(), "C1_ONE_SHOT_JOURNAL_ALREADY_EXISTS_STOP")
    require(WSL_GCLOUD.is_file() and WIN_CMD.is_file(), "C1_AUTH_BRIDGE_UNAVAILABLE")
    ctx = invoke(["docker", "context", "show"])
    ep = json.loads(invoke(["docker", "context", "inspect",
                             "--format", "{{json .Endpoints.docker.Host}}"]))
    image = json.loads(invoke(["docker", "image", "inspect", SOURCE]))
    bytes_ = review_local(image, ctx, ep, os.environ)
    auth_as = gcloud("config", "get-value", "auth/impersonate_service_account",
                    "--quiet")
    # This query reads the existing repository settings at the moment of push.
    repo = json.loads(gcloud("artifacts", "repositories", "describe", REPOSITORY,
                            "--project=" + PROJECT, "--location=" + LOCATION,
                            "--account=" + ACCOUNT, "--format=json", "--quiet"))
    package = gcloud("artifacts", "packages", "describe", PACKAGE,
                     "--project=" + PROJECT, "--repository=" + REPOSITORY,
                     "--location=" + LOCATION, "--account=" + ACCOUNT,
                     "--format=json", "--quiet", allow_not_found=True)
    validate_repo(repo, package, auth_as)
    access = gcloud("auth", "print-access-token", "--account=" + ACCOUNT, "--quiet")
    # Token always remains in process memory. Never print/store to D: or source.
    require(bool(TOKEN.fullmatch(access)) and "\n" not in access,
            "C1_TOKEN_INVALID_OR_UNAVAILABLE")
    if obtain_token:
        return access, bytes_
    return None, bytes_

def start_journal():
    payload = {"stage": "ONE_PUSH_STARTED_DO_NOT_RETRY", "source_id": SOURCE_ID,
               "target": TARGET, "created_at_unix": int(time.time()),
               "approval": "OWNER_APPROVED_ONE_PRIVATE_COPY_ONLY",
               "signing": "NOT_AUTHORIZED", "cloud_run_deployment": "NOT_AUTHORIZED"}
    try:
        fd = os.open(JOURNAL, os.O_CREAT | os.O_EXCL | os.O_WRONLY, 0o600)
    except FileExistsError as exc:
        raise Stop("C1_ONE_SHOT_JOURNAL_ALREADY_EXISTS_STOP") from exc
    with os.fdopen(fd, "w") as f:
        json.dump(payload, f, sort_keys=True)
        f.flush()
        os.fsync(f.fileno())

def update_journal(stage, digest=None):
    state = json.loads(JOURNAL.read_text())
    state["stage"] = stage
    if digest:
        state["registry_manifest_digest"] = digest
    # Journal data only (no credentials); use replace rather than append.
    next_path = JOURNAL.with_suffix(".tmp")
    with next_path.open("x") as f:
        json.dump(state, f, sort_keys=True)
        f.flush()
        os.fsync(f.fileno())
    next_path.replace(JOURNAL)

def inspect_remote(payload, digest):
    require(isinstance(payload, dict) and payload.get("schemaVersion") == 2,
            "C1_REMOTE_MANIFEST_UNEXPECTED")
    # This C1 is a single linux/amd64 image, NOT a multiarch index copy.
    require("manifests" not in payload and
            (payload.get("config") or {}).get("digest") == SOURCE_ID,
            "C1_REMOTE_CONFIG_DIGEST_MISMATCH")
    layers = payload.get("layers")
    require(isinstance(layers, list) and bool(layers) and
            all(isinstance(x, dict) and isinstance(x.get("digest"), str) and
                DIGEST.fullmatch(x["digest"]) and
                type(x.get("size")) is int and x["size"] > 0 for x in layers),
            "C1_REMOTE_LAYERS_INVALID")
    require(DIGEST.fullmatch(digest) is not None, "C1_REMOTE_DIGEST_INVALID")
    return len(layers)

def perform(token):
    with tempfile.TemporaryDirectory(prefix="oldx-c1-", dir="/tmp") as temp:
        os.chmod(temp, 0o700)
        # Docker credentials written only in a private ephemeral Linux path.
        invoke(["docker", "--config", temp, "login", "-u", "oauth2accesstoken",
                "--password-stdin", REGISTRY], input_text=token + "\n", timeout=50,
               quiet=True)
        # Read-only auth success completed; durable journal before ANY new local
        # tag and before the SINGLE provider-mutating Docker push.
        start_journal()
        print("C1_ONE_COPY_STARTED=YES", flush=True)
        try:
            invoke(["docker", "tag", SOURCE_ID, TARGET], timeout=30, quiet=True)
            push = invoke(["docker", "--config", temp, "push", TARGET],
                          timeout=900)
            m = re.findall(r"digest:\s*(sha256:[a-f0-9]{64})\b", push)
            require(len(m) == 1, "C1_PUSH_RECEIPT_DIGEST_UNAVAILABLE_STOP")
            digest = m[0]
            # A READ-ONLY manifest fetch by exact digest, never by mutable tag.
            raw = invoke(["docker", "--config", temp, "manifest", "inspect",
                          TARGET.split(":")[0] + "@" + digest], timeout=90)
            count = inspect_remote(json.loads(raw), digest)
            update_journal("ONE_PUSH_REMOTE_MANIFEST_VERIFIED", digest)
            print("C1_REGISTRY_SINGLE_PUSH=SUCCESS")
            print("C1_REGISTRY_MANIFEST_DIGEST=" + digest)
            print("C1_REMOTE_LAYER_DESCRIPTOR_COUNT=" + str(count))
            print("C1_REMOTE_CONFIG_ID_MATCH=PASS")
            print("C1_ORIGINAL_BUILD_PROVENANCE=UNVERIFIED")
            print("C1_SIGNED_CUSTODY=NOT_DONE")
            print("CLOUD_RUN_AND_PRODUCTION=NOT_CHANGED")
        except (Stop, OSError, ValueError, TypeError) as exc:
            # Once push might have begun, do NOT auto-retry or delete a remote
            # image. Read-only manual reconciliation is a separate future step.
            print("STOP_C1_OUTCOME_POSSIBLY_REMOTE_CHANGED")
            print("C1_NO_RETRY_AND_NO_DELETE")
            raise Stop("C1_SINGLE_PUSH_OUTCOME_REVIEW_REQUIRED") from exc

def main():
    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--preflight", action="store_true")
    group.add_argument("--execute", action="store_true")
    args = parser.parse_args()
    try:
        token, bytes_ = probe(obtain_token=args.execute)
        if args.preflight:
            print("C1_PREWRITE_LOCAL_AND_WINDOWS_BRIDGE=PASS")
            print("C1_LOCAL_SIZE_BYTES=" + str(bytes_))
            print("C1_NEW_PACKAGE_ABSENT=PASS_AT_INSPECTION")
            print("C1_SCAN_STATE=SCANNING_DISABLED")
            print("C1_REPO_AND_OWNER_ACCOUNT=EXPECTED")
            print("C1_UPLOAD_ACTION=NOT_STARTED")
            print("C1_OWNER_CONSENT=APPROVED_SINGLE_NEW_PRIVATE_COPY")
            print("C1_ORIGINAL_BUILD_PROVENANCE=UNVERIFIED")
            return 0
        perform(token)
        return 0
    except (Stop, OSError, ValueError, TypeError) as exc:
        print("C1_STATUS=STOP")
        print("REASON=" + (str(exc) if isinstance(exc, Stop) else
                           "C1_VALIDATION_OR_IO_ERROR"))
        print("DO_NOT_RETRY_EXECUTE_WITHOUT_READ_ONLY_RECONCILIATION")
        return 2

if __name__ == "__main__":
    sys.exit(main())
