#!/usr/bin/env python3
"""ONE public read-only OCI manifest diagnostic. Never builds/pulls/scans images."""
import datetime as dt
import hashlib
import json
import os
from pathlib import Path
import sys
import urllib.error
import urllib.request

PIN = "sha256:49559f4ee6632a11a13a7e198183efee1226de7a8f437df83c180b01bd8253ec"
URL = "https://gcr.io/v2/distroless/nodejs24-debian13/manifests/" + PIN
ACCEPT = ",".join((
    "application/vnd.oci.image.manifest.v1+json",
    "application/vnd.oci.image.index.v1+json",
    "application/vnd.docker.distribution.manifest.v2+json",
    "application/vnd.docker.distribution.manifest.list.v2+json",
))
APPROVED = {
    "functions/staging-marketplace/Dockerfile.c2-mediator-off": "ec36707fce197150e3f5f1b4bd1d0f30d8cbf7fa",
    "functions/staging-marketplace/Dockerfile.c2-mediator-off.dockerignore": "fc1944d7165bccc1bef5c06901841792724f751d",
    "functions/staging-marketplace/c2-mediator-off-server.mjs": "68e65e2e1cdce5994780a5588c8a02da3e1f4be7",
}
LIMIT = 1024 * 1024


class NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        return None


def git_blob_sha(data):
    return hashlib.sha1(b"blob " + str(len(data)).encode("ascii") + b"\x00" + data).hexdigest()


def main():
    os.umask(0o077)
    root = Path(__file__).resolve().parent.parent
    for name, expected in APPROVED.items():
        path = root / name
        if not path.is_file() or git_blob_sha(path.read_bytes()) != expected:
            print("STOP: approved Git blob mismatch or missing file:", name, file=sys.stderr)
            return 2
    if PIN not in (root / "functions/staging-marketplace/Dockerfile.c2-mediator-off").read_text():
        print("STOP: Dockerfile does not contain the exact approved pin", file=sys.stderr)
        return 2
    home = Path.home()
    marker = home / ".oldx-h1a-base-raw-manifest-once-20261125"
    if marker.exists():
        print("STOP: this raw-manifest diagnostic marker already exists; do not repeat", file=sys.stderr)
        return 2
    evidence = home / ("oldx-h1a-base-manifest-diagnostic-" + dt.datetime.now(dt.timezone.utc).strftime("%Y%m%dT%H%M%SZ"))
    evidence.mkdir(mode=0o700, exist_ok=False)
    started = dt.datetime.now(dt.timezone.utc).isoformat()
    try:
        fd = os.open(marker, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
        with os.fdopen(fd, "w", encoding="utf-8") as file:
            file.write(json.dumps({"started_utc": started, "evidence": str(evidence), "url": URL}) + "\n")
    except FileExistsError:
        print("STOP: diagnostic was already initiated", file=sys.stderr)
        return 2

    report = {
        "mode": "one_public_raw_manifest_GET_only", "started_utc": started,
        "requested_reference": URL, "requested_digest": PIN,
        "source_git_blobs": APPROVED, "status": "UNRESOLVED",
        "http_code": None, "response_headers": {}, "raw_sha256": None,
        "raw_bytes": 0, "proxy_configured": any(os.environ.get(k) for k in ("HTTP_PROXY", "HTTPS_PROXY", "http_proxy", "https_proxy")),
        "build": "NOT_RUN", "sbom": "NOT_RUN", "grype": "NOT_RUN", "runtime": "NOT_RUN",
    }
    response = None
    try:
        request = urllib.request.Request(URL, headers={
            "Accept": ACCEPT, "Accept-Encoding": "identity", "User-Agent": "OLDX-H1A-raw-manifest-readonly/1.0",
        }, method="GET")
        opener = urllib.request.build_opener(NoRedirect)
        try:
            response = opener.open(request, timeout=15)
        except urllib.error.HTTPError as error:
            response = error
        report["http_code"] = response.status
        report["response_headers"] = {
            field: (response.headers.get(field) or "")[:250]
            for field in ("Content-Type", "Content-Length", "Docker-Content-Digest",
                          "Content-Encoding", "Docker-Distribution-API-Version")
        }
        challenge = response.headers.get("WWW-Authenticate", "")
        if challenge:
            report["auth_challenge_scheme"] = challenge.split(" ", 1)[0][:32]
        if response.status != 200:
            report["status"] = "HTTP_STATUS_UNRESOLVED"
        else:
            body = response.read(LIMIT + 1)
            report["raw_bytes"] = len(body)
            if len(body) > LIMIT:
                report["status"] = "OVERSIZE_RESPONSE_UNRESOLVED"
            else:
                (evidence / "raw-manifest.bin").write_bytes(body)
                actual = "sha256:" + hashlib.sha256(body).hexdigest()
                report["raw_sha256"] = actual
                expected_header = response.headers.get("Docker-Content-Digest", "").strip()
                encoding = response.headers.get("Content-Encoding", "identity").lower()
                report["header_matches_pin"] = expected_header == PIN if expected_header else None
                report["raw_matches_pin"] = actual == PIN
                if encoding not in ("", "identity"):
                    report["status"] = "ENCODED_RESPONSE_UNRESOLVED"
                elif actual != PIN:
                    report["status"] = "RAW_MISMATCH_STOP"
                elif expected_header and expected_header != PIN:
                    report["status"] = "HEADER_MISMATCH_STOP"
                else:
                    report["status"] = "RAW_SHA256_MATCH" if expected_header else "RAW_SHA256_MATCH_HEADER_ABSENT"
                try:
                    parsed = json.loads(body)
                    report["schema_version"] = parsed.get("schemaVersion")
                    report["manifest_media_type"] = parsed.get("mediaType")
                    if isinstance(parsed.get("manifests"), list):
                        report["index_descriptor_count"] = len(parsed["manifests"])
                except (ValueError, AttributeError, UnicodeError):
                    report["json_parse"] = "UNAVAILABLE"
    except Exception as error:
        report["status"] = "NETWORK_OR_TLS_UNRESOLVED"
        report["error_type"] = type(error).__name__
        report["error_summary"] = str(error)[:240]
    finally:
        if response is not None:
            response.close()
        report["finished_utc"] = dt.datetime.now(dt.timezone.utc).isoformat()
        payload = json.dumps(report, indent=2, sort_keys=True) + "\n"
        (evidence / "receipt.json").write_text(payload, encoding="utf-8")
        print("H1A_RAW_DIAGNOSTIC=" + report["status"])
        print("EVIDENCE=" + str(evidence))
        print("HTTP_STATUS=" + str(report["http_code"]))
        print("BODY_DIGEST=" + str(report["raw_sha256"]))
        print("RECEIPT_SHA256=" + hashlib.sha256(payload.encode("utf-8")).hexdigest())
    return 0 if report["status"] in ("RAW_SHA256_MATCH", "RAW_SHA256_MATCH_HEADER_ABSENT") else 2


if __name__ == "__main__":
    sys.exit(main())
