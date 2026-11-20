#!/usr/bin/env python3
"""C0 read-only metadata preflight for EXISTING OLDX npm-free local image.

Runs only local Docker metadata inspect commands. NO Docker build, run, save,
push, tag, login, Grype, Firebase, Cloud APIs, Billing, mutation, or network.
Output size is local uncompressed estimate, NOT Registry bytes or a cost cap.
The previous completed one-shot source/runtime/scan/integrity checks are consumed.
"""
import json
import os
from pathlib import Path
import re
import subprocess
import sys

IMAGE = "oldx-bellsoft-npmfree:20261120-a1"
IMAGE_ID = "sha256:0844b637cf1bfedef60caa6a54ad515ebf9c0a937453b409101ad0d2ff254f79"
MAX_LOCAL_BYTES = 8 * 1024 ** 3
ALLOWED_CONTEXTS = {"default", "desktop-linux"}
DOCKER_OVERRIDE_KEYS = ("DOCKER_HOST", "DOCKER_CONTEXT", "DOCKER_CERT_PATH", "DOCKER_TLS_VERIFY")

class Stop(Exception):
    pass

def need(ok, reason):
    if not ok:
        raise Stop(reason)

def review(wsl_version, environment, context, endpoint, daemon_info, image_info):
    need("microsoft" in wsl_version.lower(), "OWNER_LOCAL_WSL_REQUIRED")
    need(not any(environment.get(k) for k in DOCKER_OVERRIDE_KEYS), "DOCKER_REMOTE_OVERRIDE")
    need(context in ALLOWED_CONTEXTS, "DOCKER_CONTEXT_NOT_ALLOWED")
    need(isinstance(endpoint, str) and endpoint.startswith("unix:///") and
         "\n" not in endpoint and "\r" not in endpoint, "DOCKER_ENDPOINT_NOT_LOCAL")
    need(isinstance(daemon_info, dict) and daemon_info.get("OSType") == "linux" and
         any(word in str(daemon_info.get("OperatingSystem", "")).lower()
             for word in ("wsl", "desktop", "ubuntu")),
         "LOCAL_DOCKER_DAEMON_NOT_VERIFIED")
    need(isinstance(image_info, list) and len(image_info) == 1 and
         isinstance(image_info[0], dict), "IMAGE_INSPECT_SHAPE")
    image = image_info[0]
    config = image.get("Config") or {}
    need(isinstance(config, dict), "IMAGE_CONFIG_INVALID")
    need(image.get("Id") == IMAGE_ID and IMAGE in (image.get("RepoTags") or []),
         "FROZEN_LOCAL_IMAGE_ID_NOT_FOUND")
    need(image.get("Os") == "linux" and image.get("Architecture") == "amd64",
         "WRONG_IMAGE_PLATFORM")
    need(config.get("User") == "appuser" and
         config.get("Entrypoint") == ["/usr/bin/node"] and
         config.get("Cmd") == ["functions/staging-marketplace/product-read-server.mjs"],
         "RUNTIME_CONFIG_DRIFT")
    size = image.get("Size")
    need(type(size) is int and 0 < size <= MAX_LOCAL_BYTES,
         "LOCAL_IMAGE_SIZE_UNAVAILABLE_OR_UNEXPECTED")
    # Docker image inspect Size is a local storage/uncompressed-size estimate.
    # It must NEVER be mistaken for compressed upload bytes or a billing promise.
    return {"local_bytes": size, "local_mib": round(size / (1024 ** 2), 2),
            "image_id": IMAGE_ID, "context": context}

def run_readonly(args, timeout=20):
    try:
        p = subprocess.run(args, capture_output=True, text=True, timeout=timeout)
    except (OSError, subprocess.TimeoutExpired) as e:
        raise Stop("LOCAL_DOCKER_INSPECTION_UNAVAILABLE") from e
    need(p.returncode == 0 and len(p.stdout) <= 2 * 1024 * 1024,
         "LOCAL_DOCKER_INSPECTION_FAILED")
    return p.stdout.strip()

def main():
    try:
        need(Path("/mnt/d").is_dir(), "OWNER_D_DRIVE_MISSING")
        version = Path("/proc/version").read_text("utf-8")
        need("microsoft" in version.lower(), "OWNER_LOCAL_WSL_REQUIRED")
        env = dict(os.environ)
        need(not any(env.get(k) for k in DOCKER_OVERRIDE_KEYS),
             "DOCKER_REMOTE_OVERRIDE")
        context = run_readonly(["docker", "context", "show"])
        need(context in ALLOWED_CONTEXTS, "DOCKER_CONTEXT_NOT_ALLOWED")
        endpoint = json.loads(run_readonly([
            "docker", "context", "inspect", "--format", "{{json .Endpoints.docker.Host}}"]))
        need(isinstance(endpoint, str) and endpoint.startswith("unix:///"),
             "DOCKER_ENDPOINT_NOT_LOCAL")
        daemon_info = json.loads(run_readonly(["docker", "info", "--format", "{{json .}}"]))
        inspected = json.loads(run_readonly(["docker", "image", "inspect", IMAGE]))
        result = review(version, env, context, endpoint, daemon_info, inspected)
    except (Stop, OSError, ValueError, TypeError) as exc:
        print("C0_LOCAL_METADATA=STOP")
        print("REASON=" + (str(exc) if isinstance(exc, Stop) else "LOCAL_PARSE_OR_IO_ERROR"))
        print("DO_NOT_BUILD_SCAN_PUSH_OR_RETRY_BLINDLY")
        return 2
    print("C0_LOCAL_METADATA=PASS")
    print("LOCAL_IMAGE_ID=" + result["image_id"])
    print("LOCAL_IMAGE_SIZE_BYTES=" + str(result["local_bytes"]))
    print("LOCAL_IMAGE_SIZE_MIB=" + str(result["local_mib"]))
    print("SIZE_TYPE=LOCAL_UNCOMPRESSED_NOT_REGISTRY_STORAGE_OR_TRANSFER")
    print("REGISTRY_UNIQUE_DESTINATION=UNVERIFIED")
    print("REGISTRY_AUTHORIZED_WRITER=UNVERIFIED")
    print("BILLING_ACCOUNT_OTHER_ARTIFACTS_AND_QUOTA=UNVERIFIED")
    print("ESTIMATED_PROVIDER_CHARGES=NOT_CALCULABLE_FROM_LOCAL_SIZE_ONLY")
    print("OWNER_REGISTRY_UPLOAD_CONSENT=NOT_GIVEN")
    print("BUILDER_SLSA_PROVENANCE=UNVERIFIED")
    print("REGISTRY_PUSH_AND_CLOUD_CHANGES=NONE")
    print("STEP04_RELEASE=HOLD")
    return 0

if __name__ == "__main__":
    sys.exit(main())
