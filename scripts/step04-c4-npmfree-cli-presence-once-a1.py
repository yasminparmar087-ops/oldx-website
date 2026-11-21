#!/usr/bin/env python3
"""OLDX Step04 C4: ONE bounded local filesystem-path probe of frozen npm-free image.

Creates a Docker container but NEVER starts it; docker-cp reads only six paths.
Temporary stopped-container metadata is removed; no network/image/registry writes.
One exclusive local evidence receipt survives success or failure. DO NOT rerun.
"""
import json
import os
from pathlib import Path
import subprocess
import sys

IMAGE = "oldx-bellsoft-npmfree:20261120-a1"
DIGEST = "sha256:0844b637cf1bfedef60caa6a54ad515ebf9c0a937453b409101ad0d2ff254f79"
NAME = "oldx-c4-npmfree-cli-presence-a1"
REPORT = Path("/mnt/d/OLDX/G2/c4-npmfree-cli-presence-20261121-a1.json")
PATHS = (
    "/usr/bin/sqlite3", "/bin/sqlite3", "/usr/local/bin/sqlite3",
    "/usr/bin/ldd", "/bin/ldd", "/usr/local/bin/ldd",
)

class Stop(Exception):
    pass

def need(test, reason):
    if not test:
        raise Stop(reason)

def cmd(args, timeout=30, sink=False):
    return subprocess.run(
        args, stdin=subprocess.DEVNULL,
        stdout=subprocess.DEVNULL if sink else subprocess.PIPE,
        stderr=subprocess.DEVNULL, timeout=timeout,
        text=not sink
    )

try:
    need(REPORT.parent.is_dir() and not REPORT.exists(), "REPORT_EXISTS_OR_D_MISSING")
    need("microsoft" in Path("/proc/version").read_text().lower(), "NOT_OWNER_WSL")
    need(not any(os.environ.get(k) for k in
        ("DOCKER_HOST", "DOCKER_CONTEXT", "DOCKER_TLS_VERIFY", "DOCKER_CERT_PATH")),
        "REMOTE_DOCKER_OVERRIDE")
    ctx = cmd(["docker", "context", "show"])
    need(ctx.returncode == 0 and ctx.stdout.strip() in ("default", "desktop-linux"), "DOCKER_CONTEXT")
    ep = cmd(["docker", "context", "inspect", "--format", "{{json .Endpoints.docker.Host}}"])
    need(ep.returncode == 0 and json.loads(ep.stdout).startswith("unix:///"), "DOCKER_REMOTE_ENDPOINT")
    inspect = cmd(["docker", "image", "inspect", IMAGE], timeout=25)
    need(inspect.returncode == 0, "FROZEN_IMAGE_MISSING")
    entries = json.loads(inspect.stdout)
    need(len(entries) == 1, "IMAGE_INSPECT_SHAPE")
    item = entries[0]
    desc, conf = item.get("Descriptor") or {}, item.get("Config") or {}
    need(item.get("Id") == DIGEST and IMAGE in (item.get("RepoTags") or []),
         "FROZEN_IMAGE_ID_MISMATCH")
    need(desc.get("digest") == DIGEST and
         desc.get("mediaType") == "application/vnd.oci.image.index.v1+json" and
         desc.get("size") == 856, "FROZEN_OCI_INDEX_MISMATCH")
    need(item.get("Os") == "linux" and item.get("Architecture") == "amd64",
         "WRONG_PLATFORM")
    need(conf.get("User") == "appuser" and
         conf.get("Entrypoint") == ["/usr/bin/node"] and
         conf.get("Cmd") == ["functions/staging-marketplace/product-read-server.mjs"],
         "RUNTIME_CONFIG_CHANGED")
    occupied = cmd(["docker", "container", "inspect", NAME], timeout=15)
    need(occupied.returncode != 0, "CONTAINER_NAME_ALREADY_USED")
except Stop as error:
    print("STOP_C4_PREFLIGHT=" + str(error))
    sys.exit(2)
except Exception as error:
    print("STOP_C4_PREFLIGHT_EXCEPTION=" + type(error).__name__)
    sys.exit(2)

data = {"image": IMAGE, "oci_index_digest": DIGEST, "mode": "stopped_container_not_started",
        "status": "ATTEMPT_STARTED", "paths": {}, "cleanup": "NOT_YET"}
try:
    with REPORT.open("x", encoding="utf-8") as fp:
        json.dump(data, fp, sort_keys=True)
except OSError:
    print("STOP_C4_EXCLUSIVE_RECEIPT")
    sys.exit(2)

created = False
try:
    created_proc = cmd([
        "docker", "create", "--name", NAME, "--network", "none",
        "--read-only", "--cap-drop", "ALL", "--security-opt", "no-new-privileges",
        "--user", "appuser", "--entrypoint", "/usr/bin/node",
        IMAGE, "--help"
    ], timeout=45)
    need(created_proc.returncode == 0, "DOCKER_CREATE_FAILED")
    created = True
    print("C4_EXACT_FROZEN_IMAGE=PASS", flush=True)
    print("C4_CONTAINER_STARTED=NO", flush=True)
    for path in PATHS:
        copied = cmd(["docker", "cp", NAME + ":" + path, "-"], timeout=30, sink=True)
        state = "PRESENT" if copied.returncode == 0 else "NOT_CONFIRMED"
        data["paths"][path] = state
        print("C4_PATH=" + path + " STATE=" + state, flush=True)
    data["status"] = "INSPECTION_COMPLETE"
except Stop as error:
    data["status"] = "STOP_" + str(error)
    print("STOP_C4_INSPECTION=" + str(error), flush=True)
except Exception as error:
    data["status"] = "STOP_" + type(error).__name__
    print("STOP_C4_INSPECTION_EXCEPTION=" + type(error).__name__, flush=True)
finally:
    if created:
        try:
            removed = cmd(["docker", "rm", NAME], timeout=30)
            data["cleanup"] = "PASS" if removed.returncode == 0 else "MANUAL_RECOVERY"
        except Exception:
            data["cleanup"] = "MANUAL_RECOVERY"
    else:
        data["cleanup"] = "UNKNOWN_NO_CREATE_CONFIRMATION"
    try:
        REPORT.write_text(json.dumps(data, sort_keys=True, indent=2) + "\n", encoding="utf-8")
        print("C4_LOCAL_RECEIPT_SAVED=YES", flush=True)
    except Exception:
        print("STOP_C4_RECEIPT_WRITE", flush=True)
        sys.exit(2)
    print("C4_CONTAINER_CLEANUP=" + data["cleanup"], flush=True)
    print("C4_PROBE_STATUS=" + data["status"], flush=True)
    print("C4_CVE_DISPOSITION=STILL_REVIEW_REQUIRED", flush=True)
    print("C4_G2=HOLD", flush=True)

if data["status"] != "INSPECTION_COMPLETE" or data["cleanup"] != "PASS":
    sys.exit(2)
