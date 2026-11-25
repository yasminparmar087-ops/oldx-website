# OLDX Step 05 — C1A Option B Cloud Run service deletion independently CONFIRMED

**Owner's actual Google Cloud Shell screenshot, 26 November 2026 ~01:37 IST.** Repository `yasminparmar087-ops/oldx-website`, branch `security-hardening-review`.

## Verified result, no guessing

The Owner executed the previously prepared immutable, independent, **read-only** check `scripts/step05_c1a_option_b_readonly_delete_operation_verify_once_20261126.py` pinned at `6036b39261f7092fb7c64cb756868f9573b875f1`. The screenshot shows the following exact output:

```text
C1A_OPERATION_STATE=DONE_NO_ERROR
C1A_SERVICE_STATE=404_NOT_FOUND
C1A_READBACK_RESULT=CONFIRMED_REMOVED
C1A_REASON=OPERATION_SUCCESS_AND_C1A_SERVICE_404
C1A_CLOUD_WRITES=NONE
C1A_SERVICE_ACCOUNT_DELETED=NO
C1A_REGISTRY_IMAGE_DELETED=NO
```

The earlier **owner-approved Option B** C1A service-only exact-UID/ETag Cloud Run v2 DELETE was accepted, then the independent read-only verification now confirms BOTH **long-running delete operation DONE_NO_ERROR** and **exact same C1A service GET 404_NOT_FOUND**. Thus **`oldx-step05-gateway` Cloud Run service cleanup = COMPLETE**. This is not a claim that Step 05/15 or C1A's leftover image and SA cleanup is complete, or that global Eventarc dependencies were inventoried.

The independent readback one-shot marker `~/.oldx-step05-c1a-option-b-service-delete-readback-once-20261126` is now **CONSUMED**. Original Option B deletion marker `~/.oldx-step05-c1a-option-b-conditional-service-delete-once-20261126` is also **CONSUMED**, with `WRITE_ATTEMPTED=TRUE`. **NEVER rerun any C1A DELETE or old C1A v1/v2 diagnostic/Cloud Shell one-shot, never reset or delete markers.** The prior Eventarc API remained absent from the successfully fetched enabled-services list; the owner *explicitly accepted* unknown historical Eventarc dependency risk for deletion **only** of this specific old service. Earlier temporary Viewer grant was independently `REMOVED_AND_VERIFIED`.

## Scope boundaries and next work

- **Service:** `projects/oldx-staging/locations/asia-south1/services/oldx-step05-gateway`; frozen old UID `bf441d37-e39b-4afd-b4c8-0e6edee7269b`. Gone from Cloud Run v2 GET following DONE_NO_ERROR operation. Do not recreate it for test.
- **Dedicated runtime SA** `oldx-step05-gateway@oldx-staging.iam.gserviceaccount.com` (historical unique ID `102194769236111252832`) is **NOT DELETED**. Before any deletion, independently inventory other live resource references, effective IAM dependencies, external workload use, and retain on uncertainty.
- **Pinned container image** `asia-south1-docker.pkg.dev/oldx-staging/oldx-staging-images/oldx-step05-gateway-off@sha256:612f3c02806a93d991127f87e34391646edf9bad251bb22b8aace90a434bc30a` is **NOT DELETED**. Artifact Registry repository `oldx-staging-images` may be shared and MUST NOT be deleted. Check distinct other image digest/tag/revision uses before considering exact image cleanup; never delete only by display name.
- `oldx-owner-read`, other Cloud Run services, H1B/W1–W6, H2, Firebase/Auth/Firestore, security rules, IAM and production were not targeted in C1A deletion/readback and must remain unchanged without separate scope approval.
- Do not rerun old H1A/S1/S1R/S2/S3/S3B builds, scans, security reviews, C1A staging tests, or already consumed cloud operations.
- **Next:** separate read-only targeted dependency inventory of C1A's residual runtime SA and image. If access/inventory incomplete, leave assets and record `PARTIAL_CLEANUP_WITH_LIMITS`; do not block H1B source-only planning or misstate Step05 complete. No authority for automatic removal of shared resources.
- Prior C1A OFF retention permission lasted through 28 November 2026 23:19 IST. Service removed before that deadline; no timer or further auto actions.

**Current canonical status:** `C1A_SERVICE_DELETE=CONFIRMED_REMOVED`, `C1A_DELETE_OPERATION=DONE_NO_ERROR`, `C1A_SERVICE_GET=404_NOT_FOUND`, `C1A_RESIDUAL_SA_IMAGE=PRESENT_OR_UNVERIFIED_NOT_DELETED`, `H1B_W1-W6/H2/PRODUCTION=NO_GO`.
