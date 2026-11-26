# OLDX Step05 — H1B owner actual W3–W6 PASS and safe NEW-SA disable-only closeout

**26 November 2026 ~22:09 IST**, actual owner WSL screenshot reviewed. Repo `yasminparmar087-ops/oldx-website`, branch `security-hardening-review`.

## Actual W3–W6 checkpoint — DONE, never rerun

```text
H1B_W3W6_NEW_SA_UID=115445220422157278526
H1B_W3W6_SERVICE_UID=83d724b3-fcf0-4607-8107-f111a2eacc31
H1B_W3W6_CREATE_ATTEMPTED=TRUE
H1B_W3W6_OWNER_INVOKER=EXACT_OWNER_ONLY_BINDING_VERIFIED
H1B_W3W6_HTTP_PROBES_ATTEMPTED=4
H1B_W3W6_SERVICE_CLEANUP=NEW_ONLY_RUN_SERVICE_DELETED_CONFIRMED
H1B_W3W6_SA_CLEANUP=RETAIN_PENDING_DEPENDENCY_GUARDS
H1B_W3W6_REGISTRY_IMAGE=RETAIN_NOT_REPUSHED
H1B_W3W6_RESULT=PASS_PRIVATE_OFF_FOUR_PROBES_AND_SERVICE_DELETED_SA_RETAINED
H1B_W3W6_REASON=EXPECTED_403_200_503_404
H1B_W3W6_DO_NOT_REPEAT=TRUE
```

Full [owner screenshot result and UID-custody](OLDX_STEP05_H1B_W3_W6_ACTUAL_PRIVATE_PROBES_PASS_SERVICE_DELETED_2026-11-26.md). New Cloud Run service `oldx-c2-website-mediator` was created, private access/IAM and expected HTTP codes 403/200/503/404 were proven, then deletion confirmed by W3–W6 script. **Do not redo** service create, delete, hosted requests, G2B push, prior H1A build/scan or old source checks. **Only new W1 service account** `oldx-c2-mediator@oldx-staging.iam.gserviceaccount.com` UID `115445220422157278526` and approved retained immutable H1B G2B Registry image remain; older C1A resources untouched.

## Decision: reversible disable is safer than immediate permanent deletion

Google IAM recommends disabling unused service accounts first, observing for **at least 24 hours**, and only then deleting if no dependent workloads fail. This is a bounded recommended observation, **not an unknown indefinite wait**. Google's documented API requires `iam.serviceAccounts.disable` and accepts exact numeric UID locator. Links:
- https://docs.cloud.google.com/iam/docs/reference/rest/v1/projects.serviceAccounts/disable
- https://docs.cloud.google.com/iam/docs/service-accounts-disable-enable
- https://docs.cloud.google.com/iam/docs/service-accounts-delete-undelete

Earlier owner explicit approval includes **guarded cleanup of the one newly created staging SA and service**. The proposed NEXT step is a strictly narrower **reversible disable**, not delete. This document/script does not perform it from ChatGPT: Owner must execute once within already authenticated native WSL; no new direct GCP connector access was available to the assistant.

## NEW one-shot W6SA source, not yet executed

`scripts/step05_h1b_w6sa_disable_new_uid_once_20261126.py`

- Pinned **first** source commit `3fbf984a5601a7d92055ecb1e5aab42cc35e9ca9`, exact verified Git blob `5d7dd786af6d2acd804afcdf328bbd78e3042a8a`.
- Separate one-shot marker `/root/.oldx-h1b-w6sa-exact-new-sa-disable-once-20261126`; do not delete/reset if any result after marker or repeat.
- Requires actual existing W1 success marker and exact numeric UID, successful W3W6 marker including new service UID `83d724b3-fcf0-4607-8107-f111a2eacc31`, four expected HTTP outcomes and **confirmed service deletion**. Does NOT re-run previous external probes.
- Uses the existing isolated native WSL SDK and Yasmin OAuth config; validates active account and `oldx-staging`.
- Fresh exact new Run service GET **404** and exact SA GET by numeric UID must match email, UID, and not already disabled. Targeted read-only `testIamPermissions` for **disable and enable** (rollback authority). Does NOT inspect/delete old service or shared Registry and does not claim comprehensive other-project dependency coverage.
- New marker then at most **one IAM POST `projects/oldx-staging/serviceAccounts/115445220422157278526:disable`**, readback exact UID/email/`disabled=true`; save sanitized UTC disable timestamp and explicit **24h observation recommendation**, **no permanent delete**.
- A failed/unknown response after attempting disable means `STOP_AFTER_MARKER`. Do not rerun and do not infer disabled or enabled without a separate read-only recovery. No SA keys, IAM binding modifications, image push, Cloud Run writes, Firebase or production.
- Success `H1B_W6SA_RESULT=PASS_EXACT_NEW_SA_DISABLED_UID_VERIFIED_24H_HOLD`. Even success is *disabled, not deleted*, image retained; Step05 broader launch not 100% and H2/production NO-GO.

### Owner ONE paste in CURRENT Ubuntu root WSL terminal

```bash
umask 077
d=$(mktemp -d /root/oldx-h1b-w6sa-source.XXXXXXXX) &&
curl --fail --silent --show-error --retry 0 --max-redirs 0 --max-time 40 --proto '=https' --output "$d/w6sa.py" 'https://raw.githubusercontent.com/yasminparmar087-ops/oldx-website/3fbf984a5601a7d92055ecb1e5aab42cc35e9ca9/scripts/step05_h1b_w6sa_disable_new_uid_once_20261126.py' &&
test "$(git hash-object "$d/w6sa.py")" = '5d7dd786af6d2acd804afcdf328bbd78e3042a8a' &&
python3 -B -c 'import ast,sys; ast.parse(open(sys.argv[1],encoding="utf-8").read())' "$d/w6sa.py" &&
python3 -B "$d/w6sa.py" --w6sa-disable-exact-new-sa-once
```

Expected verified result:
```text
H1B_W6SA_STAGE=ONE_EXACT_NEW_SA_REVERSIBLE_DISABLE
H1B_W6SA_SA_UID=115445220422157278526
H1B_W6SA_RUN_SERVICE=ABSENT_404_AT_PREFLIGHT
H1B_W6SA_SA_DISABLE_ATTEMPTED=TRUE
H1B_W6SA_RESULT=PASS_EXACT_NEW_SA_DISABLED_UID_VERIFIED_24H_HOLD
H1B_W6SA_REASON=EXACT_UID_DISABLED_READBACK_CONFIRMED
H1B_W6SA_SA_DELETED=FALSE
H1B_W6SA_CLOUD_RUN_AND_REGISTRY_WRITES=NONE
H1B_W6SA_DO_NOT_REPEAT=TRUE
```

Owner should send only sanitized `H1B_W6SA_*` result; no token/private config. A STOP is **not** permission to clear markers, rerun, grant roles or assume deletion. On success, record exact `DISABLED_AT_UTC`, count **at least 24 hours** before any separate dependency-guarded deletion discussion; meanwhile independent OLDX feature work may continue. Residual older C1A SA/image and existing old services remain separate and need their own scoped disposition.

**CURRENT**: `W3-W6_NEW_SERVICE=ACTUAL_PASS_AND_DELETED`; `W6SA=SOURCE_READY_OWNER_NOT_EXECUTED`; `NEW_SA=RETAINED_STATUS_ENABLED_NOT_FRESHLY_VERIFIED`; `G2B_REMOTE_IMAGE=RETAINED`; `H2/PRODUCTION=NO_GO`.
