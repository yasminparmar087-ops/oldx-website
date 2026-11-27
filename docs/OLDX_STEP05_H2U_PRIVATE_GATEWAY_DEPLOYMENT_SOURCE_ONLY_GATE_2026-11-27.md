# BAJUTO / OLDX Step05 H2U — new private Gateway deployment readiness (SOURCE PLAN ONLY)

**Created 27 Nov 2026 after H2T Owner actual read-only inventory PASS_WITH_LIMITS.** No H2U live approval, deployment, image push/build or IAM change.

## Ground truth — not assumptions

[H2T actual one-region evidence](OLDX_STEP05_H2T_CLOUDRUN_READONLY_OWNER_APPROVED_2026-11-27.md): at 2026-11-27 15:51:20 UTC owner-reported complete `oldx-staging/asia-south1` Cloud Run v2 service list has **1 existing service**, **0 H2 candidate service matches**, **0 templates attached to the dedicated Gateway SA**. H2T **CONSUMED, NEVER REPEAT**. The one existing non-H2 service was *not* individually probed/modified; its name and IAM are not in the screenshot. This proves no currently recognized H2 Gateway host in that region, not global absence of a service across regions/projects nor permission to modify the other service.

Prior H2P2 verified three distinct SAs and Gateway `oldx-c2-private-gateway@oldx-staging.iam.gserviceaccount.com` immutable UID `107238619872767759560`. Prior H2R verified one CryptoKey signer-only grant. Prior H2N verified exact KMS /1 public SPKI fingerprint `69a50043b9979b8b695ca4dc426bcb58d14666b0dc2da27ce823f57f53d46aba` at that time. New synthetic signing adapter, OAuth metadata port, permanent one-sign ledger and independent version-status source have each passed their *separate new* focused 3/3 offline tests. Do not rerun or reset them. **No actual private Gateway runtime KMS signing**.

## Fastest next gate, without placeholder deployments

A new immutable **Gateway-specific** container and private Cloud Run runtime is now required, but it would be unsafe to deploy an old H1B image with the Gateway SA, because old H1B was an unrelated OFF-only mediator experiment whose service was deleted and prior Registry image retained for history. Source modules `functions/staging-marketplace/c2-h2-gateway-host-source.mjs` and `functions/staging-marketplace/c2-h2-gateway-runtime-credential-source.mjs` are **factories**, not an HTTP server. Their source-only readiness is NOT proof of an actual working container entrypoint.

**H2U source integration** (perform before asking to enable the runtime):
1. A minimal private Gateway HTTP server entrypoint that imports the existing H2S Gateway factory; retains an **OFF-only** default. It must handle the intended Cloud Run `PORT`, add no public web route and return authenticated health/OFF behavior, without making any KMS/Firestore call at startup. Missing injected trusted providers always yields fail-closed 503.
2. Bind the *actual* host-only inputs: Cloud Run Gateway metadata OAuth access token, a separately authenticated KeyVersion status reader, fixed permanent one-sign Firestore transaction and authenticated private Backend/website mediator ports. Inject exact key PEM in the host only, validated against pinned DER SPKI; neither Owner OAuth nor browser/SA JSON keys. If any port cannot be bound with least privilege, **keep OFF**; do not stub `ENABLED` or in-memory budget.
3. Prepare one new Gateway-specific nonroot, readonly OCI image with a frozen digest after build, not the historical H1B OFF-only image. Validate code includes the above H2S entrypoint and actual dependencies, health/permissions. **No build/push permitted by H2T approval.**
4. Stage a **new** service such as `oldx-c2-private-gateway` (only after name collision check) in `oldx-staging/asia-south1` attached to the verified Gateway SA. Require Cloud Run Invoker IAM check; **no** `allUsers` or `allAuthenticatedUsers` Invoker; only authorized mediator SA when route and its ID-token audience are verified. Ingress must reflect actual mediator network path; `ingress=internal` can break an external Vercel mediator, so do not choose it blindly. See [Cloud Run access control](https://docs.cloud.google.com/run/docs/securing/managing-access) and [Cloud Run ingress](https://docs.cloud.google.com/run/docs/securing/ingress).
5. Separate actual Cloud authorization: exact source image digest provenance, `run.services.create` rights, attached Gateway SA `iam.serviceAccounts.actAs`, allowed Invoker policy, separately authorized KMS status reader, and narrowly scoped real Firestore `(default)` one-sign document create/read transaction. Do not use the one-shot budget in a generic health probe. Verify no Firestore TTL on the permanent consumed marker; NEVER delete/reset it.
6. Only after the OFF runtime passes direct UID/image/ingress/IAM readback can a **new, separately authorized, short-lived synthetic** activation ask for exactly one Gateway-runtime `:asymmetricSign`, with independently verified current /1 key status and signing-ack reconciliation. An ambiguous KMS outcome consumes the permanent budget and must NOT retry automatically; Owner decision needed. Keep production OFF.

## Exact approval separation / no rework

- **Already approved and completed:** H2T one read-only region Cloud Run list; it did not grant permission for a Cloud Build, Registry push, Cloud Run create, IAM changes, Firestore transaction, KMS GET or sign. H2T one-shot is consumed. No new Cloud action is performed in this H2U packet.
- **Can do next without new Cloud approval:** source-only server entrypoint, host dependency analysis, immutable build definition and narrow *new* source/unit checks (do NOT rerun old groups).
- **Must obtain explicit new scoped Owner approval:** one real image build/push and new private default-OFF Gateway service deployment + allowed minimal IAM grants; any real KMS/Firestore operations require their own scope.
- **No shortcut:** the old H1B mediator SA and image, or the unrelated one regional Cloud Run service, are NOT a verified H2 Gateway deployment. Do not repurpose, mutate or delete them.

**Checkpoint:** `H2T=ACTUAL_PASS_WITH_LIMITS_CONSUMED`; `REGIONAL_H2_CLOUDRUN_MATCHES=0`; `H2U=SOURCE_PLAN_READY_NO_DEPLOY`; `STEP05=ACTIVE`; `H2/PRODUCTION=NO_GO`.
