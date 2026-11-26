# OLDX Step05 C2 origin snapshot regression — Node missing in Owner WSL; no old-work replays

**26 November 2026 ~22:23 IST** actual owner WSL terminal screenshot. Repo `yasminparmar087-ops/oldx-website`, branch `security-hardening-review`.

## Exact new result

Owner executed the documented two GitHub raw HTTPS downloads for the ONE new C2 origin regression source, and BOTH `git hash-object` checks passed (execution advanced past them):
- `functions/staging-marketplace/c2-website-node-http.mjs` at pinned commit `8c12450fc01e7a6fec288a142728626550fb57f4`, blob `14b111c25fb08282f5fa5616f318f2f436910213`;
- `tests/integration/step05-c2-origin-snapshot.test.mjs` at same commit, blob `dc0f768d251520bd668f1cc40b9a1cd72ac6896f`.

Next command `node --test "$d/tests/integration/step05-c2-origin-snapshot.test.mjs"` failed **before Node started** with exact shell message:
```text
Command 'node' not found, but can be installed with:
apt install nodejs
```
**Actual new test status: `BLOCKED_RUNTIME_NODE_NOT_IN_WSL_PATH`**, **NOT A TEST FAILURE**, and no Node test PASS claimed. Already downloaded hash-verified two files in the current Owner WSL `$d` variable/directory. Do NOT repeat downloads, source work, old browser/provider suites, image build/SBOM/Grype/Registry push, W0/W1/W3V/W3-W6/W6SA or Cloud checks.

Assistant tried exactly one local raw GitHub fetch for an independent test, but DNS resolution `Could not resolve host: raw.githubusercontent.com` made it impossible; no substitute bytes were run, so **no claimed local PASS**.

## Fastest no-install option: reuse the ALREADY built local H1A Node24 image as an offline test runner

Earlier *already completed* H1A receipt shows local retained WSL image tag `oldx-h1a-c2-mediator-off:local-20261124t195244z`, platform linux/amd64. Its **GitHub-verified Dockerfile** `functions/staging-marketplace/Dockerfile.c2-mediator-off` sets `ENTRYPOINT ["/nodejs/bin/node"]`, and Node24 base. Reusing it for a **different NEW focused regression** is **NOT rebuilding, scanning, uploading, running hosted endpoints or rerunning H1A smoke**.

On current SAME WSL root terminal, retain existing `d` path (shell variable is still defined). One-paste command:
```bash
test -n "${d:-}" &&
test -f "$d/functions/staging-marketplace/c2-website-node-http.mjs" &&
test -f "$d/tests/integration/step05-c2-origin-snapshot.test.mjs" &&
docker image inspect 'oldx-h1a-c2-mediator-off:local-20261124t195244z' >/dev/null &&
docker run --rm --pull never --network none --read-only \
  --cap-drop ALL --security-opt no-new-privileges \
  --user 0 --pids-limit 64 --memory 256m \
  --mount "type=bind,source=$d,target=/work,readonly" \
  'oldx-h1a-c2-mediator-off:local-20261124t195244z' \
  --test /work/tests/integration/step05-c2-origin-snapshot.test.mjs
```
Reason for `--user 0` **inside this sandboxed disposable container only**: previous source temp files were created with `umask 077` (dirs0700), so the baked image nonroot user cannot traverse/read the volume. All Linux caps dropped, no-new-privileges, network none (loopback only for the test server), read-only root FS and **read-only** bind source, no Firebase/Cloud credentials mounted or passed, no provider calls. It is a new ephemeral process using a retained Node runtime, **not H1A smoke repetition**. The image is **not pulled** (`--pull never`), so missing image/daemon returns an explicit STOP with no new work. `--rm` deletes only this ephemeral test container, not the old retained image. No image build/scan or cloud writes; Node.js installation not needed. Do not automatically start a different package installation if Docker unavailable; report output and choose another narrowly-scoped test runner.

Expected success from the NEW test (not yet measured): `# tests 1`, `# pass 1`, `# fail 0`. Errors from `docker` or `node` mean test was **not PASS** and should be reported. No automatic retries.

## Prior status remains unchanged

H1B private W3–W6 four statuses 403/200/503/404 PASS and new Cloud Run service UID-bound deleted. W6SA test SA UID `115445220422157278526` disabled 26 Nov 22:14:17 IST, **not deleted**, earliest separate 24-hour dependency review **27 Nov 22:14:17 IST**. No W6SA rerun, no production/H2 enabled. This independent Step05 C2 G1 source fix is committed and its runtime verification is pending. Step05 true enabled hosted authenticated seller/buyer thin slice and C2 G2–G6 remain open.

**Status:** `C2_G1_ORIGIN_FIX=SOURCE_COMMITTED`, `GIT_BLOBS=VERIFIED_OWNER`, `NODE_WSL=NOT_INSTALLED_OR_NOT_IN_PATH`, `ONE_NEW_REGRESSION=NOT_EXECUTED`, `NEXT=EXISTING_LOCAL_NODE24_DOCKER_TEST_ONCE`, `STEP05=NOT_DONE`, `PRODUCTION=NO_GO`.
