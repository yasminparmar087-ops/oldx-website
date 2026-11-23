# OLDX Step 04 G8 — provider-wide gross cost STOP reality, bounded-control decision and owner choice

**24 November 2026 — SOURCE-ONLY decision proposal, NOT owner-approved for any new cost/work.** Repo `yasminparmar087-ops/oldx-website`, review branch `security-hardening-review`. This is the last separate Step04 G8 financial gate following the owner's distinct G2 and G4 **current A8 private/default-OFF residual risk acceptances**. It does not change Cloud Billing, service scaling, IAM, Firebase, quotas, alerts, traffic or production. No new billing snapshot.

## 1. Existing observed facts; no duplicate check

- One historic owner-observed **Cloud Run-specific ₹100/month spend cap** and broader **₹2,000/month alerts-only budget** were already recorded. These historical settings are NOT re-verified here and must **not** be described as current verified settings or project-wide absolute spending protection. The actual owner-approved small OFF-only B1 trials and R1 tag cleanups are CONSUMED; the 21-Nov [prior bounded, OFF-only trial G8 owner acceptance](OLDX_STEP04_G8_SERVICE_CAP_AND_OFF_ONLY_DECISION_2026-11-21.md) and 24-Nov new A8 B1/R1 approval applied **only to those trials**.
- **Current A8 tagged trial was closed:** exact immutable signed `oldx-owner-read-00012-vib` postwrite PASS_WITH_LIMITS, new `a8off23nov` tag removed by approved R1, old `oldx-owner-read-00001-8kr=100%` main and historical tags preserved; **new A8 revision and latest service template remain**. No fresh hosted HTTP, Firebase or ADC. Removing tag does NOT delete all resource costs, permanently stop an already billed service or restore prior latest service template. [Actual one-shot record](OLDX_STEP04_A8_B1_R1_R2_OWNER_ACTION_CONSENT_ONE_SHOT_2026-11-24.md).
- **Official Google Cloud Billing spend caps, currently documented (24 Nov):** each spend cap is scoped to **one project + one eligible service**; published eligible services are Cloud Run, Cloud Run functions, Gemini API and Gemini Enterprise Agent Platform. Firestore, Storage, Auth, Artifact Registry, Cloud Logging and general networking are NOT all jointly covered by a single guaranteed project-wide cap. Enforced service caps can **overshoot** because enforcement isn't instantaneous; during next month's cycle caps reset. [Official eligible services and limitations](https://docs.cloud.google.com/billing/docs/how-to/budgets-spend-caps).
- **Official alerts-only budgets:** merely notify, **do not automatically cap or stop billing**. [Official Google Cloud](https://docs.cloud.google.com/billing/docs/how-to/budgets). A hard universal ₹2,000 spending limit **cannot be claimed** based on the existing historical OLDX setup, even with alerts.
- **Other services and residual exposure:** registry bytes, Artifact Registry storage, Cloud Logging, Firestore/Storage/Auth/network egress or already-present resources may incur costs while a newly tagged default-OFF Cloud Run route is absent. Actual current all-provider spend is **NOT known** from this source-only evidence. Do not invent rupee costs, balances or guaranteed total.

## 2. Practical finite-cost and STOP plan for future *separately approved* staging

1. **No automatic new operation** from this G8 risk acceptance. Future write/test needs its own exact project, service, image, resource, intended number of calls and synthetic-resource TTL, permitted time window, immutable source/image custody, named owner/operator, plan for recovery, separate scoped R1 tag cleanup/R2 NO-OP or incident restore, and an expected gross-charge estimate including storage/logs/network.
2. Use **one precisely scoped staging trial at a time**. Default OFF and no Firebase/ADC access unless a NEW approved enabled test explicitly includes it. Keep Cloud Run min instances 0, max instances 1, concurrency 1, 1 CPU/512 MiB, 30-second timeout only where approved and verified for exact revision; finite requests/CPU/log volume, no concurrent deployments, no extra database purely to prove negative access.
3. **Cost operating triggers**: treat user's preferred **₹1,000 monthly planning target** as a *human review/STOP-before-new-paid-operations threshold* and **₹2,000 monthly ceiling** as the **risk budget goal**, not as automatically enforced guarantees; actual current spend and any billed but unreported charges must be examined at the time a new money-incurring trial is separately requested. If current projected spend is at or approaching a trigger, **STOP NEW paid actions**, evaluate alternatives, and ask owner, instead of assuming free credit prevents future charges.
4. Maintain existing alerts/service caps if currently configured; do not modify any through this document. If in the future the owner approves an AUTOMATED STOP workflow, specify trigger, costs/time-delays, account permissions and failure modes separately; disabling project billing as emergency action could disable unrelated required services and is **NOT** authorized by this decision.
5. **Owner rollback boundary:** the person operating any separately authorized trial must be able to stop new requests and remove only the trial's unique new tag with independent verification. Tag removal is **not** a project spending stop nor full deletion of persistent resources. No blanket `--clear-tags`, `--to-latest`, rev deletion or IAM/billing mutation is implied.

## 3. New explicit G8 owner decision to request (PROPOSED, NOT YET APPROVED)

**Exact owner-facing consent text:**

> હું જાણું છું કે OLDXની `oldx-staging` Cloud Run service માટે અગાઉનો spend cap અને ₹2,000 budget alert બધી Google Cloud સેવાઓના કુલ ખર્ચને ખાતરીપૂર્વક ₹2,000 નીચે અટકાવતા નથી. Cloud Run spend cap પણ ચોક્કસ eligible service સુધી મર્યાદિત છે અને વિલંબથી વધારાનો ચાર્જ થઈ શકે છે. હાલની default-OFF staging સ્થિતિ અને પહેલેથી પૂર્ણ થયેલા A8 trial સંબંધિત બાકી ખર્ચની અનિશ્ચિતતા હું મર્યાદિત રીતે સ્વીકારું છું. આગળ કોઈ નવી paid staging કસરત પહેલાં અંદાજિત સંપૂર્ણ ખર્ચ, ₹1,000 planning review/STOP trigger, ₹2,000 risk-budget goal, સમય/કૉલ મર્યાદા અને STOP/rollback યોજના અલગથી ચકાસીને મારી નવી મંજૂરી લેવી. આ G8 નિર્ણયથી કોઈ billing setting, Cloud deployment, Firebase API, IAM કે productionમાં ફેરફાર મંજૂર થતો નથી. તે ₹2,000નો guaranteed hard cap હોવાનું પ્રમાણ નથી.

If the owner explicitly accepts **THIS** statement, record only `G8_OWNER_CURRENT_DEFAULT_OFF_FINANCIAL_RESIDUAL_RISK=ACCEPTED_WITH_LIMITS` and `G8_OWNER_GROSS_COST_STOP_PLAN=ADOPTED_AS_PLANNING_CONTROL`, **not** `G8_WHOLE_PROJECT_SPEND_HARD_CAP=PASS`. Existing early Cloud Run-only B1 G8 consent is already consumed; this is a **fresh decision about the post-A8 existing DEFAULT-OFF configuration and future release gating**, not a second request for an already authorized B1 operation.

**No auto-execution** and no permission to lift a spend cap, configure billing alerts, enable Firebase or production. Any future enabled/production cost risk acceptance and exact execution remains distinct.

## 4. Decision-dependent Step04 status

- BEFORE this new owner choice: `G8_NEW_OWNER_FINANCIAL_PLAN=PROPOSED_NOT_APPROVED`, `G8_GUARANTEED_PROVIDER_WIDE_HARD_STOP=NOT_PROVEN`. G2/G4 current A8 private default-OFF owner limited risk decisions **DONE**, but neither is a technical all-clear. Original Step04 technical exit **HOLD**; Step05 NOT AUTHORIZED; production NO-GO.
- AFTER an explicit scoped acceptance, at most: owner **G8 bounded-planning risk disposition complete with limits**; provider-wide hard STOP **still NOT PROVEN**, fixed monthly cost guarantee **still UNAVAILABLE**. Under original owner-locked Step04 technical exit, `STEP04=ACTIVE_HOLD` until genuinely required technical access/hosted/cost gates are satisfied or owner separately approves an administrative decision-only handoff that carries ALL such requirements forward intact. **A signed owner risk acceptance is a decision, not an assertion of impossible cloud capabilities.**

**No redoing of A8 Build/SLSA/Grype/local runtime, B1/postwrite/R1, G4 corrected Cloud Asset analyzer, default-DB inventory, old billing reads or CI.** This doc creates no cloud operations.


## 24 November 2026 — ACTUAL OWNER APPROVAL OF G8 FINITE-BUDGET PLAN: ACCEPTED_WITH_LIMITS

The owner explicitly replied **"ha svikaru chhu"** (“Yes, I accept”) immediately after the assistant asked whether to accept the **specific G8 post-A8 DEFAULT-OFF staging financial risk** under the documented thresholds. This directly authorizes the following **risk disposition and planning controls only**, and **nothing operational**:
1. Existing scoped Cloud Run service-specific spend cap (historically observed ~₹100/month) and older ₹2,000 billing budget alerts **do NOT guarantee** an all-Google-provider/project spending ceiling. Cloud Billing reporting/enforcement latency, Firestore/Auth/Storage/Artifact Registry/Logging/networking and already existing usage can create charges beyond the goal. The user accepts this **residual uncertainty for the current post-A8 DEFAULT-OFF configuration only**.
2. **₹1,000/month** is an owner-adopted **manual review/STOP-before-new-paid-operation trigger**, not an automatic Cloud Billing cap, stop of ongoing usage, or a verified current balance. **₹2,000/month** is the owner's **risk-budget goal**, not a guaranteed or technically enforced hard stop.
3. Before ANY new paid Cloud trial, operator must scope exact project/service/image/accounts, predicted *gross* all-provider charges (including registry/logs/networking), finite calls/time/synthetic resources/cleanup and rollback, observe actual recent billing including lag, and ask fresh explicit owner release consent. If projected or actual spend approaches the review trigger, pause **new paid actions** pending owner review. Do not assume trial credits or alerts guarantee free usage.
4. The owner's acceptance **does not authorize** billing/spend-cap/alert edits, service deployment/re-tag/routing or revision deletion, Firebase/ADC/Data-plane activation, IAM/Rules change, a hosted request, a new database, Step05, production/website launch or automatic billing shutdown. No new cloud provider action is executed in this documentation update.

**Final narrow owner decision status (supersedes earlier PROPOSED heading for this same exact scope):**
- `G8_OWNER_CURRENT_DEFAULT_OFF_FINANCIAL_RESIDUAL_RISK=ACCEPTED_WITH_LIMITS`
- `G8_OWNER_GROSS_COST_STOP_PLAN=ADOPTED_AS_MANUAL_PLANNING_CONTROL`
- `G8_OWNER_DECISION_FOR_THIS_SCOPE=COMPLETE`
- `G8_UNIVERSAL_2000_INR_HARD_CAP=NOT_PROVEN_AND_NOT_PROMISED`
- `G8_CURRENT_ACTUAL_MONTH_SPEND=NOT_FRESHLY_VERIFIED`
- `G8_FUTURE_ENABLED_OR_PRODUCTION_RISK=NOT_AUTHORIZED`
- `G2_OWNER_CURRENT_A8_OFF_ONLY=ACCEPTED_WITH_LIMITS`, `G4_OWNER_CURRENT_A8_OFF_ONLY=ACCEPTED_WITH_LIMITS`
- `G4_EFFECTIVE_INVOKER_EXCLUSIVITY=UNVERIFIED`, `G4_NONDEFAULT_DB_NEGATIVE_DENIAL=UNVERIFIED`
- `STEP04_ORIGINAL_TECHNICAL_EXIT=ACTIVE_HOLD`, `STEP05=NOT_AUTHORIZED`, `PRODUCTION=NO_GO`

The previously completed A8 private signed immutable `00012-vib` B1/postwrite/R1 remains **CONSUMED**; `a8off23nov` tag removed, original `00001-8kr=100%` main and old tags preserved, A8 latest template/revision remains, no hosted HTTP or enabled Firestore test. This G8 decision **does not retroactively establish** the missing original technical gross-cost hard-stop guarantee or release all other technical gates. **No old billing/IAM/DB observations, scans, builds, SLSA or A8 Cloud Run commands were repeated.**
