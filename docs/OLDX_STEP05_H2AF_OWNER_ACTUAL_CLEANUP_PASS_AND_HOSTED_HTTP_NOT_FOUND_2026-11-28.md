# BAJUTO / OLDX Step05 — H2AF OWNER ACTUAL TEMPORARY CLEANUP PASS

## Owner evidence, 28 Nov 2026 ~01:11 IST, Ubuntu WSL root screenshot

Owner executed previously approved immutable H2AF source `scripts/step05_h2af_exact_temp_cleanup_default_false_sa_guard_once_20261128.py`, pinned creation commit `9a40a36ab0815758de4e3c051720f8582d6b1191`, verified Git blob `3f82e4c9bbbaad08aa9970657fba11784a80097b`; shell verified Git blob and Python AST before invocation. Exact relevant actual terminal output:

```text
H2AF_SA_PREWRITE_EMAIL_UID_ENABLED=VERIFIED
H2AF_SA_DISABLED_FIELD_PRESENT=FALSE
H2AF_EXISTING_EXACT_ATTEMPT_STARTED=1
H2AF_EXISTING_EXACT_ATTEMPT_FINISHED=1
H2AF_FINISHED_STATUS=NOT_FOUND
H2AF_MARKER=CONSUMED_NO_REPEAT
H2AF_STAGE=DELETE_EXACT_PAUSED_JOB
H2AF_JOB=DELETED_404_VERIFIED
H2AF_STAGE=REMOVE_ONLY_PROBE_INVOKER_PRESERVE_OWNER
H2AF_GATEWAY_INVOKER=OWNER_ONLY_VERIFIED
H2AF_STAGE=DISABLE_TEMP_SA_UID
H2AF_PROBE_SA=DISABLED_UID_VERIFIED
H2AF_STAGE=DELETE_SAME_TEMP_SA_NUMERIC_UID
H2AF_PROBE_SA=DELETED_404_VERIFIED
H2AF_CLOUD_RUN_GATEWAY_INGRESS_IMAGE=UNMODIFIED
H2AF_OTHER_IAM_KMS_FIRESTORE_PRODUCT_WRITES=NONE
H2AF_HTTP_HEALTH=NOT_VERIFIED_NOT_RETRIED
H2AF_H2_PRODUCTION=NO_GO
H2AF_DO_NOT_REPEAT=TRUE
H2AF_RESULT=EXACT_TEMP_JOB_PROBE_INVOKER_SA_CLEANUP_PASS
```

**Verified outcomes:** The one temporarily created Scheduler job `projects/oldx-staging/locations/asia-south1/jobs/oldx-h2ad-off-healthz-20261128` is DELETED, and a post-delete exact GET returned 404. Cloud Run `projects/oldx-staging/locations/asia-south1/services/oldx-c2-h2-private-gateway` retains the **Owner only** direct `roles/run.invoker` binding (temporary probe principal removed, fresh ETag write and readback). Exact temporary IAM probe SA `oldx-h2ad-probe-20261128@oldx-staging.iam.gserviceaccount.com`, immutable UID `110217058111344002447`, was disabled with UID check, then deleted by numeric UID and readback 404. No change to Gateway ingress or image, no Firebase/KMS/Product writes by H2AF. **H2AF cleanup PASS**; not a live marketplace PASS.

**Root cause identified for H2AE preflight STOP:** H2AF printed `H2AF_SA_DISABLED_FIELD_PRESENT=FALSE`, and still verified correct immutable email+UID and enabled default state. Therefore H2AE's earlier `sa.get("disabled") is False` check was incorrectly treating the omitted ProtoJSON `disabled=false` field as a state mismatch. This is now supported by actual owner output, not only a hypothesis. H2AE STOP occurred before its marker and any Cloud write. Do not repeat it.

**Remaining H2 hosted HTTP gate:** H2AD8 single Scheduler `:run` returned API HTTP200 but H2AD9 proved 1 AttemptStarted + 1 AttemptFinished with status `NOT_FOUND`, and **0 exact Cloud Run request logs**, so **hosted GET /healthz HTTP 200 / JSON OFF response was NOT verified**. Do not retest the deleted Scheduler job, create replacement identical probes, or infer success from H2AF cleanup. Existing OFF-only private Gateway image and service are separate preserved infrastructure; never broaden ingress or enable Product without distinct approval.

**No-repeat markers:** H2AF `/root/.oldx-step05-h2af-exact-temp-probe-cleanup-once-20261128` CONSUMED; older H2AE, H2AD0–9, H2AC/H2AB/H2AA/H2Z and related H2/H1B builds/tests/scans/registry/G2 IAM stages must NOT be repeated merely to refresh evidence. No rerun of one-shot secrets, no marker deletion/reset. GitHub branch remains `security-hardening-review`; no production deploy.

## Highest-value Step05 continuation

Move from low-yield repeated private Scheduler probes to the **real G2–G6 product backend and seller/buyer flow** based on existing code and source evidence. Inspect existing canonical G2–G6 docs, scoped KMS provisioning/signing and Firebase Auth/Firestore/media gates before choosing a single new authorized action. Distinguish source-only validations from actual cloud integration. Step05 remains `ACTIVE` and H2/production `NO_GO`. This handoff is a checkpoint, not proof of remaining gates.
