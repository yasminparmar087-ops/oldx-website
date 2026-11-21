# OLDX Step 04 — G4 OFF-only boundary and effective IAM gate (21 Nov 2026)
Status: **SOURCE-ONLY REVIEW / NOT AN EXECUTION ORDER**. Repo `yasminparmar087-ops/oldx-website`, branch `security-hardening-review`.

## Owner decisions now available
- C4: Owner accepted **only residual risk for the six frozen scanner severe findings** (1 CRITICAL, 5 HIGH) for a *single future, separately authorized, private, 0%-main, DEFAULT-OFF/503* B1, **not** enabled API, production or a scanner PASS.
- G8: Owner separately accepted a **limited but not guaranteed hard capped financial residual risk** for the same possible OFF-only staging trial, NOT a deployment/billing change.
- Previously recorded G4 project Owner/Editor nonexclusive-invoker risk acceptance is only for one future separate OFF-only B1; effective exclusive IAM and cross-DB authorization are NOT verified.
- No separate B1/R1/R2 execution approval exists. Step04 HOLD, production NO-GO.

## G4 evidence frozen (do not repeat)
Earlier owner-observed ~17:03/17:07 read-only Cloud Run + IAM snapshots, without current-state lock:
- Service `oldx-owner-read` in `oldx-staging`, `asia-south1`, ingress `all`, no public `allUsers`/`allAuthenticatedUsers` direct service IAM members. One named service-level `roles/run.invoker` member (identity intentionally omitted); project-level Owner count 2 and Editor count 1, possible additional authenticated invokers; inherited org/folder grants not fully inspected. Service template `run.googleapis.com/invoker-iam-disabled` annotation NOT_SET — default IAM behavior consistent, but not proof of effective exclusive auth.
- Two exact latest template feature flags `OLDX_PRODUCT_READ_ACTIVATE_STAGING=false` and `OLDX_PRODUCT_READ_STAGING_ADC=false`; 100%-traffic old revisions showed MISSING for both flags, **not** proof old runtime is safely disabled. A 0%-main tagged URL remains invokable by a permitted principal.
- C5 later completed three read-only revision metadata GETs. Protected cached traffic: main `00001-8kr=100%` untagged, `00002-tid` `healthcheck`, `00003-nus` **`step3rc14`** exact tag; proposed `ownerreadv2` absent. No new revision or service mutation.
- Runtime-SA project/default-db IAM condition previously reviewed and one-document positive create/update and negative delete 403 + operator cleanup evidence already consumed. **Not evidence of effective denial on another Firestore database**, or exclusivity of IAM from any broader conditional/unconditional grant.

## New source-only boundary continuity (actual source reviewed)
The pinned npm-free frozen source commit `fcc96574b6388dc441a0b5d3eade48e79c7ebb24` and current review branch matched GitHub blobs:
- `functions/staging-marketplace/product-read-server.mjs` SHA `135e43d064c479a59a6f4b91a001c2bae9fb83f4`
- `functions/staging-marketplace/runtime.mjs` SHA `749f4259068c4d9dd2f46706222c7a43ba47fb59`
- `Dockerfile.product-read.bellsoft-npm-free` SHA `c833e8372324cbdf80f6497bf3968ac421cadfc4`.

At source level, only `OLDX_PRODUCT_READ_ACTIVATE_STAGING === 'true'` enters the staging initialization branch; `OLDX_PRODUCT_READ_STAGING_ADC === 'true'` separately gates Admin initialization. Other values (including explicit `false`) lead to the disabled product route `503 ENFORCEMENT_UNAVAILABLE`; health routes may remain 200. No claim about future runtime image actually deployed or all other paths/native code. This narrows the OFF-only trial *without replacing* IAM evidence.

## Split two gates, never conflate

### G4-A: ONE future private DEFAULT-OFF/503 B1 (still gated)
Requirements to assess **just before a separately authorized B1**, not now:
1. Immutable proposed npm-free OCI **index** `sha256:0844b637cf1bfedef60caa6a54ad515ebf9c0a937453b409101ad0d2ff254f79`; verify exact C3 local signature/bundle identity at release, no claim of independently trusted original SLSA builder.
2. **Fresh** single bounded read-only exact service IAM/ingress/`run.googleapis.com/invoker-iam-disabled`/project inherited grants/preimage/digest/roles as needed for release; if any public invoker, explicitly disabled IAM check, unapproved caller, or structural drift -> **STOP**. Existing 2 Owner/1 Editor potential invokers cannot be called exclusive owner-only.
3. Future new revision `ownerreadv2` tagged **0%-main**, no public access, exact product flags FALSE (and verify startup default-OFF in runtime), expected project/service account, no Product API enabled, no Auth/Firestore request, no hosted smoke invocation, no new data, no extra IAM privileges.
4. Preserve `00001-8kr` **100%** main and both existing tags; R1 remove only proposed tag if created; R2 NO-OP if root/tags unchanged, else separate fresh-state incident procedure. Never `--to-latest` or `--clear-tags`.
5. Explicit separately authorized B1 write and specific R1/R2 fallback, supervisor present, narrow resource/cost plan with owner-recorded G8 financial risk. **No cloud write is approved by this document**.
6. If any ambiguity in effective IAM, service-specific auth policy or OFF-only target invariants -> HOLD. Conditional risk acceptance does not cure an exploitable access path.

**Important:** Even if G4-A is later accepted for OFF-only operation, do not label `G4_EFFECTIVE_OTHER_DB=PASS`, `G4_EXCLUSIVE_INVOCATION=PASS`, or authorize enabled B2; log narrower `G4_OFF_ONLY_CONTAINMENT=PROVISIONALLY_SOURCE_SUPPORTED` until exact hosted preflight.

### G4-B: Firestore-enabled Product API / multi-database isolation (NOT authorized)
Separate gated future work: independently establish runtime service account effective IAM including **all** project, folder, organization, direct and inherited permissions and any unconditional roles, plus effective database-scoped condition; verify unauthorized database access is denied using an approved, non-destructive method, not a second arbitrary database creation. No product Auth/Firestore data-plane enablement until this gate is independently met and explicitly authorized. Prior default-DB one-doc positive/DELETE negative evidence and deny-all Firestore Rules are **insufficient** for other-database IAM isolation.

## Provider official references (research, not cloud execution)
- Cloud Run [access control with IAM](https://docs.cloud.google.com/run/docs/securing/managing-access): project owners/editors may invoke; Invoker IAM check and public configuration have separate semantics.
- Cloud Run [auth overview](https://docs.cloud.google.com/run/docs/authenticating/overview): authorization may arise from project-level principals.
- Firestore [Rules conditions](https://firebase.google.com/docs/firestore/security/rules-conditions): server/admin SDK uses IAM and bypasses Firestore Security Rules.
- Firestore [native IAM](https://docs.cloud.google.com/firestore/native/docs/security/iam): inspect effective IAM separately from client Rules.
- Firestore [database creation/access](https://docs.cloud.google.com/firestore/native/docs/manage-databases): Google Console can misrepresent database-level IAM condition enforcement; console view alone is not negative permission proof.

## Final status / next handoff
`C4_OFF_ONLY_OWNER_SIX_CVE_RISK=ACCEPTED_WITH_LIMITS`
`G8_OFF_ONLY_OWNER_FINANCIAL_RISK=ACCEPTED_WITH_LIMITS`
`G4_OFF_ONLY_SOURCE_DEFAULT_OFF_GUARD=SUPPORTED`
`G4_EFFECTIVE_INHERITED_INVOCATION=UNVERIFIED`
`G4_OTHER_DATABASE_EFFECTIVE_DENY=UNVERIFIED`
`G4_ENABLED_API=NO_GO`
`C5_REVISION_READ_ONLY=COMPLETE`
`C5_R1_R2=SOURCE_ONLY_PLAN_COMPLETE`
`B1_R1_R2=NOT_AUTHORIZED_OR_EXECUTED`
`STEP04=HOLD`
`PRODUCTION=NO_GO`

**Next action:** Reuse existing evidence, prepare ONE finite/fresh pre-B1 read-only IAM+service+traffic gate (not repeat old diagnostic); only if target scope and risk evaluation can be made safe should owner be presented an **exact separate B1/R1/R2 consent**. Do not create a second database, re-run C1–C5, build/scan/upload, invoke a hosted endpoint, or change IAM/Rules/billing/deploy under this source-only approval.
