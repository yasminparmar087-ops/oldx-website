# OLDX Step 05 — C1A removed; residual service-account and exact image metadata confirmed

**26 Nov 2026 ~01:41 IST, actual Owner Cloud Shell screenshot**, repo `yasminparmar087-ops/oldx-website`, branch `security-hardening-review`.

## Latest read-only result

After the independently verified C1A Cloud Run deletion operation `DONE_NO_ERROR` and exact service GET `404_NOT_FOUND` ([canonical removal confirmation](OLDX_STEP05_C1A_OPTION_B_SERVICE_DELETION_CONFIRMED_2026-11-26.md)), Owner ran a small **read-only** command to check the historically frozen residual identities. Exact screenshot outputs:

```text
C1A_SA=EXACT_UID_PRESENT
C1A_IMAGE=METADATA_READ_OK
C1A_OTHER_REFERENCES=NOT_YET_CHECKED
CLOUD_WRITES=NONE
```

The Owner's read command used exactly:
- Service account `oldx-step05-gateway@oldx-staging.iam.gserviceaccount.com` and verified returned uniqueId **`102194769236111252832`** (same as historic frozen C1A).
- Registry pinned exact image `asia-south1-docker.pkg.dev/oldx-staging/oldx-staging-images/oldx-step05-gateway-off@sha256:612f3c02806a93d991127f87e34391646edf9bad251bb22b8aace90a434bc30a`; `gcloud artifacts docker images describe` succeeded, but this script did **not** inspect the returned metadata for other references.
- The command used `--account=yasminparmar087@gmail.com`, `--project=oldx-staging`, redirected raw CLI output/errors into ephemeral files and removed them on exit. No IAM/API enable/disable or write.

**Evidence limit:** This confirms the **SA exact identity is currently present** and **the pinned image metadata was readable**. It **does not establish that either is unused**, nor whether an image tag is shared, whether another Cloud Run service/revision, Cloud Build, or external principal/workload still depends on either asset. The C1A service itself **is confirmed removed**; that fact is not reverted by presence of these leftovers. Do not delete the SA, any image, tag, shared `oldx-staging-images` repository or other project resources based on these metadata checks alone.

## Next action — minimal independent reference scope; do not block Step05 H1B work

1. Keep the two residual assets **unchanged** while doing one bounded **read-only** reference inventory; begin with current Cloud Run services/revisions on project `oldx-staging` and the relevant Cloud Run region(s), checking exact `serviceAccount` or digest matches; check identity's effective IAM/external possible references separately only if scope is sufficient. Fail closed if inventory is incomplete, region unknown, list denied or other dependencies cannot be excluded.
2. Retain the shared repository regardless of C1A state. Deleting a digest/tag may impact other revisions/tags; any exact image cleanup requires independent scoped evidence and **separate approval**. SA deletion is irreversible for its identity and requires separate approval, not automatically covered by old C1A service-only Option B exception.
3. Do not repeat C1A service deletion (its old one-shot `WRITE_ATTEMPTED=TRUE` and subsequent readback `CONFIRMED_REMOVED` markers **CONSUMED**), the prior temporary Eventarc Viewer grant (revoked verified), build, Grype/image scan, S3/S3B, or earlier C1A probes. Historical Eventarc inventory was unknown, explicitly accepted **only for the old C1A service deletion**; it is not an automatic risk exception for SA or image.
4. Prioritize H1B source-only planning and any separately authorized staging steps while retaining residual resources. Do **not** claim Step 05 fully complete, no H1B W1–W6, H2, production or Firebase rules deployment from this residual presence check.

**Canonical state:** `C1A_SERVICE_DELETE=CONFIRMED_REMOVED`; `C1A_RESIDUAL_SA=EXACT_UID_PRESENT`; `C1A_RESIDUAL_IMAGE=METADATA_READ_OK`; `C1A_OTHER_REFERENCES=NOT_YET_CHECKED`; `C1A_RESIDUAL_DELETE=NOT_AUTHORIZED_OR_EXECUTED`; `CLOUD_WRITES=NONE_IN_THIS_METADATA_CHECK`; `STEP05=NOT_COMPLETE`.
