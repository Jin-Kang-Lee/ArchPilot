# ArchPilot — Evaluation & Quality Assurance Plan

| Field | Value |
|---|---|
| Document ID | ARCHPILOT-EVAL-005 |
| Version | **1.0 — Four-month, two-role MVP** |
| Prepared | 12 November 2026 |
| Document status | **Proposed evaluation protocol — owner approval required before benchmark freeze** |
| Primary product source | `01-PRD.md` v1.1 |
| Architecture source | `02-SYSTEM-ARCHITECTURE.md` v1.1 |
| Contract source | `03-DATA-CONTRACTS.md` v1.0 |
| Delivery source | `04-DEVELOPMENT-PLAN.md` v1.0 |
| Owner | Solo developer / AI Solutions Architect project owner |
| Audience | Project owner, CodeBuddy / Codex, future reviewers |
| Evaluation horizon | Continuous tests during Months 1–3; frozen comparative benchmark and release review in Month 4 |

> **Scope and authority.** This plan evaluates the *simplified MVP*: (1) consultative discovery by the Requirements Analyst, (2) logical architecture composition by the Architecture Designer with a **small curated AWS catalog**, (3) independent `ARCH-001`–`ARCH-006` deterministic checks, and (4) the SA-facing discovery and architecture review workflow. It does **not** authorize an extra Cloud Specialist, Reviewer, or Documentation Agent, enterprise governance, full-cost estimation, automatic deployments, or a new evaluation platform. The PRD controls product requirements; contracts control implemented payload semantics. All percentages below are **targets or illustrative calculation examples**, not results.

---

## 1. Executive summary

### 1.1 What we need to learn

ArchPilot must demonstrate more than “an LLM can draw an architecture.” Evaluation asks:

1. **Discovery:** Does it identify important missing information, ask useful prioritized questions, preserve the customer’s answers, expose contradictions, and avoid inventing facts?
2. **Design:** Does it turn those requirements into an understandable **provider-neutral graph**, cover explicitly required capabilities, link major nodes to requirements, and make defensible AWS suggestions grounded in our limited catalog?
3. **Verification:** Do the named rules catch their exact defined errors reproducibly without claiming that a passing design is secure, compliant, scalable, or production-ready?
4. **User control:** Can an SA review and revise without silent promotion of assumptions, lost answers, hidden blockers, or model-generated approval?
5. **Differentiation:** Compared with an ordinary prompted LLM and a deliberately strong single-role baseline, does the integrated workflow provide measurable advantages **worth its additional latency and cost**?

### 1.2 Four types of evidence

| Evidence type | Example | Source of truth | Can run offline? |
|---|---|---|---|
| **Contract and state tests** | Answering a question preserves prior answers; stale revision fails | `03-DATA-CONTRACTS.md` + pytest | Yes |
| **Deterministic rule fixtures** | A dangling edge raises `ARCH-002` | Named rules + hand-built graph fixtures | Yes |
| **Model-behavior benchmark** | Critical missing-question recall on unseen briefs | Frozen synthetic cases + human gold labels | No; saved outputs can be rescored offline |
| **Human usability/quality review** | Design makes sense; rationale helps an SA decide | Anchored reviewer rubric and evidence | Yes, on saved artifacts |

**Success is not defined as “multi-agent wins.”** A truthful evaluation may find that a single-agent design is similarly good and cheaper. Report this rather than moving the goalposts.

### 1.3 Operating principles

- **User-provided statements outrank model inferences.** A confirmed fact requires traceable brief/SA evidence, not model confidence.
- **Frozen test data stay unseen by implementation prompts.** Do not tune to the held-out answer key.
- **Equal information access for comparisons.** The direct-chat, single-role, and two-role runs receive the same base facts and comparable catalog/reference content.
- **Separate objective and subjective metrics.** Code can verify IDs and rules; humans assess relevance, feasibility, and explanation quality.
- **Record errors and uncertainty.** “Unknown,” “unsupported,” and “insufficient evidence” are legitimate outputs.
- **No invented benchmark results.** Keep result tables blank until actual runs occur.
- **No proprietary data.** Use fabricated company names, documents, traffic, and answers; exclude Tencent/client materials.

---

## 2. Scope, traceability, and exclusions

### 2.1 In-scope requirements

| Evaluation area | PRD IDs | Contract / implementation anchor | Primary evidence |
|---|---|---|---|
| Brief ingestion, provenance | `FR-001`, `FR-002` | `ProjectCreate`, `Requirement`, `EvidenceRef`; `CT-001/002` | API + gold-label accuracy |
| Priority questions / gaps | `FR-003` | `ClarificationQuestion`, `QuestionPriority` | Critical-question recall and relevance |
| Multi-round discovery | `FR-004`, `FR-005`, `FR-008` | `DiscoveryState`, `QuestionResponse`; `CT-003/004` | Three-round scripted interactions |
| Contradictions | `FR-006` | `Claim`, `Contradiction`; `CT-005` | Conflict detection/preservation |
| Readiness / provisional flow | `FR-007` | `DiscoveryReadiness`, acknowledgement; `CT-006/007` | Exact state transitions |
| Capability decomposition / graph | `FR-009`, `FR-010` | `ArchitectureGraph`, `DesignerProposal` | Graph validity, coverage, traceability |
| AWS evidence | `FR-011` | `CatalogService`, `ServiceSuggestion`; `CT-009` | Verified catalog match and label integrity |
| Deterministic rule engine | `FR-013` | `ARCH-001`–`ARCH-006`; `CT-010`–`CT-015/018` | Positive and negative fixtures |
| Coordinator / SA control | `FR-015`, `FR-016`, `FR-019` | Server-owned state, review; `CT-008/017/019` | Bounded failures and explicit actions |
| UI and saved project | `FR-017`, `FR-018`, `FR-020` | Discovery/Architecture Workspace; `CT-016/020` | Manual E2E / reload test |
| Markdown handoff | `FR-022` | Current canonical summary | Export integrity test |
| Evaluation and comparison | `FR-024` | `M4-T02`, this plan | Reproducible benchmark package |

Check related `NFR-001`–`NFR-013` through the relevant safety, observability, determinism, maintainability, and deployment tests (Section 9).

### 2.2 Explicitly excluded

- Independent third/fourth/fifth agent quality comparisons for MVP; five-agent orchestration is **future scope** (`FR-014` is future).
- Automated technical compliance/security certification, measured SLA guarantees, live region eligibility, full AWS catalog, production resource sizing, and monthly AWS/LLM cost calculator (`FR-023` future).
- Immutable design history, automated dependency-diff change impact (`FR-021` future), enterprise approvals and real user accounts.
- Building a custom evaluation UI, evaluation microservice, model judge ensemble, vector database, or enterprise observability stack.

**Meaning of “passing”:** It means a **particular test** passed, *not* that the generated customer architecture is safe or deployable.

---

## 3. Evaluation artifacts and ownership

Build only small, version-controlled files and a Python runner. Recommended directory structure, introduced gradually:

```text
evaluation/
├── README.md                       # How to run tests and reproduce a report
├── protocol.md                     # Frozen settings, comparison rules and exclusions
├── rubric.md                       # Reviewer scoring anchors and examples
├── cases/
│   ├── development/               # Visible while building: a few worked examples
│   └── held_out/                  # Freeze before formal benchmark; do not tune on these
├── gold/                          # Human labels, separated from generation prompts
├── prompts/                       # Versioned baseline system/task prompts
├── scripts/
│   ├── run_benchmark.py            # Optional small batch runner
│   └── score_saved_outputs.py      # Deterministic scoring where possible
├── runs/                           # Generated outputs; ideally Git-ignored except samples
└── reports/
    ├── results-template.md
    └── final-results.md            # Populate from observed runs only

backend/tests/
├── test_discovery_contracts.py
├── test_architecture_rules.py
├── test_catalog_mapping.py
└── test_agent_failures.py
```

**Avoid duplicate sources of truth:** actual Pydantic models/OpenAPI are the runtime schema; the contract document describes them. A gold file specifies expected customer facts/questions for one synthetic case, not a new product data contract.

### 3.1 Ownership and review

| Item | Owner | Verification |
|---|---|---|
| Cases and gold labels | Project owner; optionally one technically literate peer | Check labels against synthetic brief and answer scripts |
| Agent and baseline prompts | Project owner, with implementation help | Commit exact prompt versions before benchmark |
| Deterministic tests / runner | CodeBuddy or Codex may implement | Owner reviews assertions and runs tests |
| Subjective architecture scoring | Owner; ideally blind second reviewer for a subset | Anchored rubric; preserve disagreements |
| Release decision | Project owner | Review hard gates, semantic metrics, failures, limitations |

---

## 4. Benchmark dataset: small, synthetic, and truly held out

### 4.1 Dataset sizes

**Proposed protocol (approve under `OD-009`):**

- **Development set:** 3–5 synthetic briefs used openly for implementation, debugging, and prompt tuning; may include PRD stories `AS-01` and `AS-02` and the invoice example `AS-03`.
- **Held-out benchmark:** **12 synthetic briefs** (within PRD's 10–20 guidance); no answer key exposed in agent context. If capacity permits, extend to 16 but do not make this a release requirement.
- **Stability subset:** 4 of the 12 held-out briefs, repeated **3 runs each** per system if budget/time allows; report variability rather than taking only the best run.

These are **not evidence of broad real-world generalization**. A small hand-designed sample gives directional engineering signals and failure examples.

### 4.2 Case mix — 12 held-out briefs

| Case IDs | Count | Brief class | Intended challenge |
|---|---:|---|---|
| `H01–H03` | 3 | Incomplete AI support / internal knowledge systems | Budget, residency, peak traffic, access boundaries, action permissions |
| `H04–H06` | 3 | AI document ingestion / extraction / human review | Async processing, storage, audit needs, unsupported assumptions |
| `H07–H08` | 2 | Media/content processing | Queues, worker relationships, storage, review requirements |
| `H09–H10` | 2 | Event-driven or analytics-backed app | Data ingestion, persistence, notifications, peak load |
| `H11–H12` | 2 | Conflicting, adversarial, or underspecified cross-domain requests | Contradiction handling, uncertainty, untrusted brief instructions |

**Variation across cases:** include at least 2 alternative deployment/region needs, 2 missing quantitative constraints, 2 briefs requiring 3 discovery rounds, 2 with legitimate “not applicable” answers, 2 conflicts, 1 unknown capability, and 1 prompt-injection attempt. Some cases may satisfy multiple conditions. Do not manufacture graph requirements outside the controlled vocabulary just to force failures.

### 4.3 Case file contract (evaluation-only; not an API)

Each case should record:

```yaml
case_id: H01
case_version: '1.0'
brief: 'A synthetic business brief with incomplete constraints.'
scenario_family: 'support'
answer_script:
  - turn: 1
    answers:
      budget: 'Maximum USD 2,000 per month.'
      residency: 'EU-only processing.'
  - turn: 2
    answers:
      peak_load: 'Peak varies; customer has not measured it.'
  - turn: 3
    answers:
      permitted_actions: 'Read-only answers; no account changes.'
expected:
  explicit_facts: []                # Human-authored, anchored to brief/turn
  critical_missing_topics: []       # Human-authored; not exact question strings
  expected_contradictions: []       # Claim/evidence pairs when relevant
  required_capabilities: []        # Within supported vocabulary
  unsupported_capabilities: []
  check_specific_conditions: []     # e.g. provisional state is preserved
review_notes: ''
```

This is a **template with placeholder content**, not a completed hidden benchmark. For each case, fill `expected` explicitly before running the formal comparison. Store gold separately from material shown to models.

### 4.4 Writing the gold answer key

For each case, the owner should annotate:

1. **Explicit facts** with a short quote/source turn and expected `functional` / `non_functional` / `constraint` categorization when relevant.
2. **Critical missing topics**, expressed semantically: e.g., `monthly_budget_amount`, `data_processing_region`, `peak_concurrency`, rather than one exact English sentence. Add priority and a one-line reason.
3. **Answer script** and any known `answered`, `deferred`, `skipped`, `not_applicable` dispositions.
4. **Contradiction pairs** with two source statements and whether conflict is unresolved or explicitly resolved.
5. **Minimum capability coverage** within the approved vocabulary (not a unique canonical architecture); list acceptable alternatives and known unsupported needs.
6. **Safety/UX conditions:** e.g., must stay provisional, must not silently mark design accepted, must not claim catalog support.

Have a second person review at least 3 cases if practical. If no independent reviewer is available, label the gold as **single-author judgments** and include that limitation.

### 4.5 Data leakage controls

- Prepare and **freeze** held-out cases, answers, labels, rubrics and prompts before the Month 4 comparative run.
- Record hashes/commit SHAs. Do not load gold labels into the Analyst/Designer model inputs or coding-agent prompts.
- Use development cases for all prompt engineering. If a held-out case is used to debug a model behavior, mark it **contaminated**, move it into development, and replace it with a new frozen case.
- Never include real customer/company data, proprietary documents or live cloud credentials.
- One deliberately adversarial synthetic brief may contain instruction-like text; treat it as untrusted input, not as instructions to the evaluator or product.

---

## 5. Requirements Discovery evaluation

### 5.1 Extraction: factuality, coverage, and categorization

Define a **gold fact** as a distinct requirement/constraint explicitly present in the brief or recorded SA answer. The same fact may be paraphrased; exact string match is *not* required.

| Metric | Definition | Scoring method | Interpretation |
|---|---|---|---|
| **Fact recall** | Correctly captured gold facts / all gold facts | Human semantic mapping using evidence references | Missed stated needs |
| **Fact precision** | Correct extracted facts / all claims labeled `confirmed` | Human semantic mapping; unsupported confirmations count false | Hallucinated/mislabeled facts |
| **Unsupported confirmed-fact count** | Number of claims marked confirmed with no matching brief/SA evidence | Inspect `EvidenceRef` and source transcript | Safety-critical false assertions |
| **Type classification accuracy** | Correct requirement kind / matched facts | Compare to annotated categories; document ambiguous labels | Functional vs NFR vs constraint quality |
| **Provenance coverage** | Confirmed requirements with valid, relevant evidence / all confirmed requirements | Inspect source ID and excerpt | Auditability of extracted facts |

**Example of an error:** “limited budget” becomes “monthly budget is USD 1,000” labeled confirmed. That is a fabricated fact. “Exact monthly budget is unknown” is correct.

**Important:** Code can check whether an `EvidenceRef` exists, but validating whether it actually supports a semantic claim generally needs a human or carefully reviewed offline annotation. Do not call provenance a validated fact merely because an excerpt is nonblank.

### 5.2 Question quality, prioritization, and rationale

| Metric | Formula / rubric | Evaluation intent |
|---|---|---|
| **Critical topic recall @ first two rounds** | Gold critical missing topics materially addressed by questions in rounds 1–2 / all gold critical topics; score semantic matches | Did the SA get the most important discovery prompts early? |
| **Question relevance** | Mean 0–3 reviewer score for each question (rubric below) | Are questions useful for this brief? |
| **Priority alignment** | Gold critical topics asked as `critical`/`high` / gold critical topics asked | Are impactful questions prioritized? |
| **Rationale quality** | Mean 0–3 reviewer score per question | Does the explanation connect answer to an architecture decision? |
| **Repeated resolved-topic rate** | Questions unnecessarily re-asking already settled topics / all questions after round 1 | Does the system remember what the SA said? |
| **Question overload** | Questions per round; share of redundant/low-value questions | Did the system bury priorities? |

**Proposed default:** Present **3–5 prioritized questions per round**, per PRD §4. This is a usability target, not an inflexible ban on fewer questions when fewer are necessary.

For semantic matching, use a mapping table (`predicted question ID -> gold topic ID`, or `unmatched`) with a reviewer rationale. One question may cover multiple topics if its wording clearly asks each; don't inflate recall from vague, generic questions.

### 5.3 Multi-round continuity and answer integrity

Script at least **three rounds** for selected cases:

1. Submit brief; record first question set and state.
2. SA answers/defer/skips specified questions using the evaluation answer script; run discovery again.
3. SA provides a changed constraint or a further answer; run discovery again.
4. Inspect every previous answer and question disposition.

| Metric | Automated expectation / manual note |
|---|---|
| **State retention pass** | No previous SA answer or disposition lost after valid reanalysis; all scripted cases pass |
| **Reconciliation fidelity** | New agent proposals do not silently overwrite confirmed facts; all seeded tests pass |
| **Question deduplication** | No exact or semantically equivalent settled question repeated without a documented reason |
| **Response action validity** | Empty `action=answer` rejected; skip/defer/N/A distinct; `CT-004` |
| **Revision safety** | Stale `expected_state_revision` returns conflict/no overwrite; `CT-016` |
| **Adaptive follow-up** | Reviewer 0–3 score: follow-up logically uses new answer instead of repeating initial generic checklist |

**Nuance:** An answered topic can be revisited when a **new contradictory statement** invalidates it; record that as a justified follow-up, not gratuitous repetition.

### 5.4 Contradiction and readiness evaluation

Use seeded cases including the PRD's EU-only versus US-only inference conflict (`AS-02`).

- **Contradiction recall:** expected incompatibilities detected / expected incompatibilities in annotated cases.
- **False conflict rate:** non-conflicting pairs flagged as conflicts / annotated non-conflicting pairs (report count, not inflated percentage from few cases).
- **Conflict preservation:** both source claims/evidence remain inspectable after detection; no silent last-write-wins behavior.
- **Resolution control:** only explicit SA correction/resolution closes a conflict.
- **Readiness policy:** unresolved critical questions/conflicts/unaccepted assumptions produce `needs_clarification`; explicit SA acknowledgement produces `provisional` while blockers remain; model cannot set `ready_for_design` or approve the graph.

**Example state test:** `needs_clarification` + unresolved residency + user explicit provisional acknowledgement ⇒ `provisional`, with same residency blocker in `blocking_item_ids`, graph and export. No automatic factual promotion.

### 5.5 Anchored human rubrics for discovery (0–3)

| Score | Question relevance | Rationale quality | Adaptive follow-up |
|---:|---|---|---|
| **0** | Irrelevant or misleading | Missing/incorrect or circular | Ignores new answer; repeats settled point |
| **1** | Broadly related but vague/redundant | Generic (“important for design”) | Some awareness but little connection to answer |
| **2** | Specific and relevant to a real gap | Correct, identifies affected design choice | Responds to the answer and asks a useful next question |
| **3** | High-impact, concise, and precisely targeted | Explains a concrete design consequence/trade-off | Refines discovery efficiently and avoids unnecessary repetition |

Report scores alongside examples. Do not collapse all three criteria into a single opaque “AI quality” number.

---

## 6. Architecture Designer and catalog evaluation

### 6.1 Structural/schema quality

- **Typed-output pass rate:** `DesignerProposal` parsed successfully / attempts; record any automatic retry separately.
- **Schema-valid graph rate:** graphs valid against Pydantic schema / successfully generated graphs.
- **Rule-violation rate:** proportion of proposals with one or more `ARCH-001`–`ARCH-005` findings; break down by ID and severity.
- **Graph reference integrity:** duplicates, dangling edges and unknown requirement references from `ARCH-001/002/004`; score these with deterministic tests.

Do not treat the model's own explanation that a graph is valid as evidence. Rule results are always backend-derived.

### 6.2 Coverage and traceability

| Metric | Definition | Caveat |
|---|---|---|
| **Explicit capability coverage** | Gold required capabilities represented in graph / gold required capabilities within supported vocabulary | Human must confirm the gold vocabulary reflects the actual brief |
| **Requirement traceability rate** | Major design nodes with valid requirement IDs **or** stated cross-cutting rationale / all major nodes | This is coverage, not proof the node is necessary |
| **Unsupported-capability disclosure** | Unavailable expected capabilities explicitly reported as unresolved / unavailable expected capabilities | Model must not invent catalog-backed capability IDs |
| **Functional architecture quality** | Reviewer 0–3 score for coherent data flow and basic fit to requirements | Human architectural judgment, not automated certification |
| **Explanation usefulness** | Reviewer 0–3 score: why nodes/edges exist and what remains uncertain | Do not reward confident but unsupported claims |

**Generalization test:** At least two different held-out workload families must generate inspectable, meaningful logical architectures. The benchmark includes multiple unrelated families; a strong result should not depend on selecting an entire hardcoded use-case template. “New combinations of supported components” is the actual claim, not universal architecture design competence.

### 6.3 AWS service grounding and overclaiming

The Month 2 catalog is a locally versioned, hand-reviewed dataset of approximately 10–15 entries. **Matching a catalog entry does not certify cloud suitability** or current regional, quota, compliance or pricing properties.

| Metric | Test |
|---|---|
| **Supported mapping validity** | Every `catalog_supported` suggestion references an actual service ID, compatible capability ID, and selected catalog version |
| **Unknown-service honesty** | A non-catalog suggestion is `unverified` or `unsupported`, never falsely `catalog_supported` |
| **Grounded rationale** | Rationale and limitations are supported by the saved catalog record; human spot-check |
| **Overclaim count** | Claims of confirmed region/pricing/compliance/availability absent explicit evidence; count and list |
| **Catalog freshness trace** | Record `catalog_version`, service `last_reviewed_on` when available and source URL, where documented |

Use the implementation's versioned catalog. A baseline can be given the **same catalog snapshot**, even if it is delivered as readable text instead of a lookup API; note interface differences.

### 6.4 Anchored human rubrics for architecture (0–3)

| Score | Functional fit / graph coherence | Explanation and uncertainty |
|---:|---|---|
| **0** | Cannot represent required user flow; serious unsupported assertion | Misleading or asserts facts not provided |
| **1** | Includes some right components but missing essential flow/relations | Vague rationale or hides major uncertainty |
| **2** | Plausible draft satisfying most key functional needs with review items | Explains key decisions, limitations and unresolved requirements |
| **3** | Coherent, appropriately scoped draft that covers critical needs with defensible trade-offs | Clear requirement-to-node reasoning; candid and actionable caveats |

Do **not** require all architectures to use the same components: alternative valid compositions are allowed. Record evidence of why a design fails rather than grading by string similarity to a template.

---

## 7. `ARCH-001`–`ARCH-006`: deterministic verification plan

The six rule definitions below mirror the PRD and Data Contracts; **do not expand their semantics in evaluation tests**.

| Rule | Positive fixture (should not flag) | Negative fixture (should flag) | Required assertion |
|---|---|---|---|
| `ARCH-001` | Distinct node/edge IDs | Reused node ID or edge ID | `error`, duplicate ID in `affected_ids` |
| `ARCH-002` | Every edge endpoint exists | Edge points to unknown `node_missing` | `error`, edge and missing node identified |
| `ARCH-003` | Explicit required capability present in a node | Requirement needs `document_retrieval`; graph lacks it | `error`, requirement/capability identified |
| `ARCH-004` | Every node's `requirement_ids` exists | Node points to `req_missing` | `error`, invalid requirement reference identified |
| `ARCH-005` | Queue has `consumes` edge queue → worker with `async_worker` | Catalog-semantic queue has no connected consumer | Finding only when catalog semantics support it; uncertain metadata is `warning`, not proven error |
| `ARCH-006` | No open critical items, contradictions or unaccepted assumptions | Open critical region question or unresolved conflict | Readiness blocker/warning; **does not by itself set** `graph_rules_passed=false` |

### 7.1 Mandatory automated acceptance checks

All `CT-010`–`CT-015` and `CT-018` must pass, including:

- **Positive and negative fixtures** for every rule, with exact `rule_id`, severity, IDs, and bounded interpretation.
- **Repeatability:** same canonical requirements, graph, catalog/rule versions ⇒ identical normalized findings and order.
- **No model call:** monkeypatch or fake adapter asserts validator does not invoke an LLM or network.
- **No mutation:** validate on copy; input is unchanged by rule execution.
- **Schema versus findings:** malformed data fails Pydantic/API validation; schema-valid bad graph returns structured rule findings.
- **Readiness versus topology:** structurally valid graph can have `graph_rules_passed=true` while `ARCH-006` reports blockers; provisional acknowledgement does not clear them.
- **Queue ambiguity:** missing catalog semantics cannot be silently upgraded to proven `error`.

### 7.2 Mutation tests (lightweight)

For at least one valid hand-built graph, programmatically apply six single-defect mutations (one per named rule). Verify the corresponding rule detects the defect and reports relevant IDs. Use direct pytest cases/parameterization; do **not** add a mutation-testing service.

### 7.3 Failure taxonomy

Record separately: `schema_parse_error`, `graph_integrity_error`, `capability_coverage_issue`, `catalog_mapping_issue`, `readiness_blocker`, `human_quality_issue`. A case can have more than one. This avoids the misleading single label “valid architecture.”

---

## 8. Fair baseline comparison: direct LLM vs single role vs two roles

### 8.1 Systems under comparison

| System | Definition | What it can do | Why compare |
|---|---|---|---|
| **A — Direct LLM prompting** | One general chat session with a strong documented SA prompt, same model family/settings when available, same brief and access to equivalent catalog descriptions | Ask clarification questions, ingest answers, propose a graph/diagram and explain it | Measures value over a skilled user's ordinary AI-assisted workflow |
| **B — Single-role structured baseline** | One AI role handles discovery and design, with typed outputs, same backend contracts, curated catalog and **same deterministic validator** after generation | One consolidated model role, user pauses and comparable support tools | Isolates whether splitting Analyst/Designer roles adds value beyond structure and software |
| **C — ArchPilot MVP** | Two sequential specialist roles, shared canonical state, approved provisional choice, same catalog and deterministic validator | Full intended discovery→design→review workflow | Candidate product |

**Important validity distinction:** If A does not use a validator and B/C do, the result is an **end-to-end workflow comparison**, not evidence that the multi-agent model itself is superior. Compare B vs C to isolate the effect of role separation while holding tools/contracts constant. Don't compare B/C validator error counts against A as though A had identical automatic checking tools.

### 8.2 Comparable resources and conditions

Before collecting results, freeze and record:

- Exact model/API version, model provider, prompt text/commit hash, temperature or supported sampling settings, token/output caps, date of run.
- Same frozen synthetic brief, discovery answer script and gold topic expectations.
- Same AWS catalog **content and freshness** for A, B and C; offer direct-chat baseline a readable version and disclose that its interface differs.
- Same total **information availability** at each discovery turn. Answer only asked questions in the primary comparison; do not give a system extra hidden customer facts. Use semantic matching to select the scripted answer to a question. If a system never asks a critical question, it does not receive that answer.
- Same cap of **three discovery rounds**, same instruction to ask approximately 3–5 focused questions/round; same explicit customer decision to proceed/proceed provisionally where warranted.
- One first-pass run per case for all three arms; no cherry-picking the best response. Additional stability repetitions use identical frozen settings and are reported separately.
- No private benchmark gold labels, expected graph, or human scores in system prompts.

Where the plain chat format cannot emit an exact `ArchitectureGraph`, use a **documented normalization step**: a reviewer maps components/edges and citations into the common scoring sheet. Do not silently grant the other systems a structural advantage by treating chat prose as invalid JSON. If you ask A to emit the same JSON graph, record that as a separate structured-prompt variant rather than claiming it is ordinary chat.

### 8.3 Reproducible three-round interaction procedure

For **each case and system**:

1. Start a clean session/state with no prior case history; provide identical synthetic brief and relevant catalog description.
2. Request clarification questions; save raw output, question list, priorities, rationales, and timing.
3. Match asked questions to answer-script topics. Provide the corresponding answer; when no scripted answer exists, use a predefined `unknown`/`deferred` response and record why. Do not invent answers live.
4. Repeat for up to three rounds; when the workflow considers discovery done, record readiness and the stopping rationale. A case with unresolved critical items proceeds only if the standardized SA script explicitly authorizes provisional design.
5. Request the candidate logical architecture and AWS suggestions; save raw artifact and structured/normalized graph.
6. Apply the same human scoring rubric. For B/C, additionally record typed validation outputs from the common validator. For A, evaluate graph flaws manually or normalize into the same validator **and label this as post-hoc comparison**.
7. Record latency, model calls, token totals and estimated API cost, with `N/A` if the provider does not report a field. Also record human interaction time separately.
8. Do not revise prompts using held-out case outcomes. If correcting an implementation defect is necessary, report original outcomes and move the case out of held-out status if it influenced tuning.

**Prevent answer-script bias:** Prewrite topic-level answers, not responses tailored to a system's wording. If two systems ask semantically equivalent questions, both receive the same fact. Ambiguous or compound questions receive only facts clearly requested; note adjudications.

### 8.4 Outcome table (template only; fill after runs)

| Metric | A Direct Chat | B Single Role | C ArchPilot Two Roles | Notes |
|---|---:|---:|---:|---|
| Cases completed / attempted | TBD | TBD | TBD | Same 12 cases planned |
| Critical question recall | TBD | TBD | TBD | Human semantic matching |
| Unsupported confirmed facts (count) | TBD | TBD | TBD | Lower is better |
| Repeated resolved-topic rate | TBD | TBD | TBD | Lower is better |
| Contradictions detected / expected | TBD | TBD | TBD | Relevant subset |
| Architecture functional fit (0–3) | TBD | TBD | TBD | Blind scoring where possible |
| Capability coverage (%) | TBD | TBD | TBD | Supported gold capabilities |
| Catalog overclaims (count) | TBD | TBD | TBD | Lower is better |
| Total model calls | TBD | TBD | TBD | Count all retries |
| Median wall-clock latency | TBD | TBD | TBD | Also report range/p90 if meaningful |
| Median observed token cost | TBD | TBD | TBD | Same currency/pricing date |
| Manual intervention time | TBD | TBD | TBD | Distinct from model latency |
| Hard safety/state test failures | N/A | TBD | TBD | Not equivalent capabilities in A |

**No synthetic performance statistics may be presented as observed results.** After evaluation, report both differences and counterexamples, not only averages that flatter C.

### 8.5 Efficiency formulas and budget control

Calculate actual (not assumed) usage when the API returns token counts:

\[
\text{Per-run model cost} = \sum_i \left(\frac{\text{input tokens}_i}{10^6} P_{\text{input},i} + \frac{\text{output tokens}_i}{10^6} P_{\text{output},i}\right)
\]

Add any provider-specific billed categories only when known and documented; otherwise mark the estimate partial. Cache discounts must use actual billed/usage categories rather than guessed savings.

Record `wall_clock_ms` from beginning to final artifact, `stage_latency_ms` where available, `llm_call_count`, `input_tokens`, `output_tokens`, `retry_count`, `provider_error_count`, `price_snapshot_date`, and `estimated_usd` (nullable). Record **model wait time** and **SA answer time** separately where measured; don't compare manual chat typing time against fully automated calls without qualification.

**Proposed benchmark spending guardrail:** Owner sets a maximum evaluation budget (for example USD 20–40) before live runs and uses dry-run/mock tests first. The amount is a planning option, **not** an expected project cost or guarantee of sufficient budget.

If total benchmark runs would exceed the approved limit, **run the same reduced case subset across all systems** and report the reduced sample; do not selectively cut weak cases for one system.

### 8.6 Human review and disagreement

- Use blinded labels such as `System X/Y/Z` for quality ratings wherever feasible; redact branding/UI formatting and randomize sample order.
- Score question relevance, rationale, adaptivity, functional architecture fit, and uncertainty disclosure independently on the 0–3 rubrics.
- For **at least 3 held-out cases** (if a peer is available), ask a second reviewer to score independently; record per-criterion disagreement and resolve via a short written explanation. Without a second reviewer, clearly state single-rater limitations.
- Never replace rubric scoring with an uncalibrated LLM-as-judge number. An LLM may help organize saved artifacts, but the owner reviews all high-stakes architectural quality labels.
- Report sample size, scoring variance and a few examples of errors/strengths; avoid statistical significance claims from 12 synthetic cases.

---

## 9. Automated quality, robustness, and security gates

### 9.1 Contract test coverage

Use the existing `CT-001`–`CT-020` meanings from Data Contracts §10.1; don't rename or redefine them in this plan.

| Gate | Related tests | Expected result |
|---|---|---|
| Input and provenance | `CT-001/002` | Blank/oversized input rejected; fabricated confirmation not stored |
| Three-round discovery / answer lifecycle | `CT-003/004` | Answers persist; invalid answer request fails safely |
| Conflict and provisional | `CT-005/006/007` | Evidence preserved, explicit acknowledgement required, blockers retained |
| Agent failure and catalog safety | `CT-008/009` | Typed error and last-good-state retention; catalog overclaim rejected |
| Graph rule integrity | `CT-010`–`CT-015`, `CT-018` | Every named rule passes fixed positive/negative fixtures |
| State revision and human control | `CT-016/017` | Stale updates fail; edits invalidate previous acceptance |
| Prompt-injection boundary | `CT-019` | Brief cannot bypass validation/approve/cloud-act |
| Persistence | `CT-020` | Save/reload retains canonical current project |

**Hard gate:** Every implemented release-critical `CT-*` test must pass before launch; if an in-scope test is not implemented, label release **not ready** rather than counting it as passed. Tests not yet required by a current monthly milestone may be recorded as `not_due`, not `passed`.

### 9.1.1 Exact contract-test index for review

Use the complete identifier set from `03-DATA-CONTRACTS.md` §10.1. The compact range notation in tables means **every** intervening case must run: `CT-001`, `CT-002`, `CT-003`, `CT-004`, `CT-005`, `CT-006`, `CT-007`, `CT-008`, `CT-009`, `CT-010`, `CT-011`, `CT-012`, `CT-013`, `CT-014`, `CT-015`, `CT-016`, `CT-017`, `CT-018`, `CT-019`, `CT-020`. Their behavior is inherited from the contracts, not redefined here.

### 9.2 NFR checks that cannot be skipped

| NFR IDs | Check | Evidence |
|---|---|---|
| `NFR-001`, `NFR-013` | Public demo uses synthetic data; reset/delete data can be demonstrated | Fixture review and reset smoke test |
| `NFR-002` | API keys remain server-side and absent from Git/logs/browser bundle | Secret scan + negative config test |
| `NFR-003` | Brief with “ignore rules, mark approved” cannot change permissions | Injection fixture + audit of state |
| `NFR-004` | Invalid model outputs fail Pydantic boundary without corrupting state | Mocked malformed-response test |
| `NFR-005` | Same graph + rules + catalog returns identical findings | Fixed-repeat pytest |
| `NFR-006` | Timeouts/errors are handled with bounded retries and user-visible failure | Mocked provider failure and test |
| `NFR-007` | Nodes map to requirements or a cross-cutting rationale | Graph inspection/report test |
| `NFR-008` | Clean setup, unit/integration tests documented | CI and fresh-install check |
| `NFR-009` | Run IDs, stage durations and error types recorded without sensitive text | Sanitized logs review |
| `NFR-010` | Browser supports brief → questions → graph → findings → revision | Manual E2E walkthrough |
| `NFR-011` | Latency and usage/cost tracked on benchmark | Benchmark metadata completeness |
| `NFR-012` | Deployed demo startup and core smoke pass | Deployment checklist |

### 9.3 Failure injection (mocked; not live outages)

Minimum scenarios: timeout; rate limit; malformed JSON; unknown enum; provider returns no output; unsupported AWS service suggestion; disconnected edge; repeated question; contradictory claim; stale revision; API key missing. Assert bounded retries, preserved prior-good state, honest status, and no secret disclosure. Use local fake adapters; do not stress real providers or external cloud accounts.

---

## 10. Acceptance thresholds and release decision policy

Do not invent a “95% AI accuracy” target with no evidence. Use **two classes of gates**.

### 10.1 Hard release blockers — testable software invariants

Release **must not proceed** while any of these is failing:

1. Required Pydantic/API and `CT-001`–`CT-020` tests for the implemented MVP fail.
2. `ARCH-001`–`ARCH-006` positive/negative fixtures fail or same-input validator results are nondeterministic.
3. A confirmed customer fact/answer can be silently overwritten or discarded in a scripted test.
4. An open critical contradiction/unknown disappears when proceeding provisionally.
5. An agent/browser can directly set `accepted_by_sa`, `catalog_supported`, validator findings or readiness without server checks.
6. An unapproved architecture is presented as accepted/certified; editing a reviewed graph improperly preserves acceptance.
7. Demo leaks model keys/secrets, handles genuine private data as test fixtures, or cannot recover/reset data as designed.
8. The main synthetic happy-path E2E or deployed smoke test fails.

For deterministic invariants, the expectation is **100% pass across the specified fixtures**. This is not a claim of general absence of bugs.

### 10.2 Proposed semantic quality targets (review after baseline; not automatically binding)

These are **initial investigation thresholds**, not product guarantees. Validate them on the development set first; freeze any changed thresholds **before** running held-out comparisons. If the model misses a target, evaluate severity and document it honestly rather than silently changing the goal.

| Measure | Initial investigation target | Rationale / how to use |
|---|---|---|
| Critical missing-topic recall in first two rounds | **≥ 80%** on annotated held-out topics | Focus on discovery value; failures analyzed individually |
| Question relevance | **Median ≥ 2/3** | Questions should be specific, not generic filler |
| Rationale quality | **Median ≥ 2/3** | “Why this matters” should affect an architecture choice |
| Fact recall | **≥ 85%** on explicit brief/answer facts | Foundational extraction quality; false confirmations are a more severe issue |
| Confirmed-fact precision | **≥ 95%** | Investigate any invented confirmed number, region or permission |
| Capability coverage | **≥ 80%** of gold supported capabilities | Tests broad utility without requiring identical graph shapes |
| Architecture functional fit | **Median ≥ 2/3** | Coherent early-stage draft, not certified design |
| Catalog overclaims | **0 in deterministic catalog-mapping tests** | Verified-state truthfulness must be enforced in code |

**Owner decision required:** Approve, lower, or replace the numerical investigation targets after inspecting development-set performance. Since a 12-case benchmark is small, report numerators/denominators and per-case distributions, not only percentages. For semantic failure severity, a single particularly serious fabrication may be unacceptable despite a high aggregate score.

### 10.3 Go / conditional go / no-go

| Decision | Conditions | Action |
|---|---|---|
| **Go** | All hard gates pass, qualitative results meet reviewed expectations, synthetic demo safe, limitations disclosed | Publish with benchmark and caveats |
| **Conditional go** | All safety/state/validation hard gates pass; some semantic targets missed but failures are noncritical and explicitly disclosed | Owner may publish as **experimental portfolio prototype**, not production-ready |
| **No-go** | Any hard blocker fails, benchmark integrity compromised without re-run, or unresolved serious fabricated confirmations persist | Fix or restrict demo; do not claim release readiness |

An unfavorable comparison with the single-agent baseline is **not** by itself a release blocker. It is a design finding and may justify simplifying the agent workflow in a future iteration.

---

## 11. Month-by-month evaluation schedule (aligned to 21 development tasks)

| Month / owner tasks | Build-time evaluation activities | Exit evidence |
|---|---|---|
| **M1 — `M1-T01`–`M1-T02`** | Freeze input/model/schema examples; `CT-001`; set up pytest and fake provider; draft rubric/gold template | Clean schema tests + three synthetic development briefs |
| **M1 — `M1-T03`–`M1-T04`** | Fact provenance (`CT-002`), parsing error (`CT-008`), critical-question labels, manual relevance/rationale review | Extracted known/unknown facts; prioritized questions; no invented confirmations in seeded checks |
| **M1 — `M1-T05`–`M1-T06`** | Three-round scripts, status/contradiction/provisional (`CT-003`–`CT-007`), first live smoke, thin UI walkthrough | Three-round discovery demo with blockers and persistence during session |
| **M2 — `M2-T01`–`M2-T02`** | Graph schema/refs, requirement links; test 2 different development-brief families | Inspectable provider-neutral graphs; no hardcoded whole use-case selector |
| **M2 — `M2-T03`–`M2-T05`** | Catalog grounding (`CT-009`), known/unknown capability tests, stage latency and call instrumentation | Graph + catalog suggestions grounded in saved snapshot; unknowns labeled |
| **M3 — `M3-T01`** | Complete all six positive/negative rules, repeatability (`CT-010`–`CT-015`, `CT-018`) | Deterministic validator test suite green |
| **M3 — `M3-T02`–`M3-T05`** | User-edit/revalidate, stale revision, acceptance/reload (`CT-016/017/020`); manual E2E | SA sees findings, reviews revised graph, reopens project |
| **M4 — `M4-T01`** | Export completeness and provisional/unknown preservation | Valid summary from current stored project |
| **M4 — `M4-T02`** | Freeze prompts, gold, 12 held-out cases; run three-arm comparison; save outputs and score | Honest result tables; success and failure examples; latency/usage recorded |
| **M4 — `M4-T03`** | Fix significant failures, test prompt injection and secrets (`CT-019`), rerun regression suite | Issues/limitations documented; no hard blocker |
| **M4 — `M4-T04`–`M4-T05`** | Deployment smoke, reset, fresh clone, release checklist and portfolio review | Reproducible safe demo + evaluation report |

**Exact implementation task coverage:** Month 1: `M1-T01`, `M1-T02`, `M1-T03`, `M1-T04`, `M1-T05`, `M1-T06`; Month 2: `M2-T01`, `M2-T02`, `M2-T03`, `M2-T04`, `M2-T05`; Month 3: `M3-T01`, `M3-T02`, `M3-T03`, `M3-T04`, `M3-T05`; Month 4: `M4-T01`, `M4-T02`, `M4-T03`, `M4-T04`, `M4-T05`. This plan assigns evaluation evidence to each existing development task without creating extra mandatory coding phases.

**Schedule note:** Formal held-out runs happen in Month 4; freeze the scoring rubric and benchmark protocol **before inspecting held-out output**. You can draft cases earlier and use only the development cases while coding.

---

## 12. Running the evaluation: practical procedure for CodeBuddy / Codex

### 12.1 Suggested minimal runner behavior

Implement no more than these commands unless needed:

```bash
# Deterministic CI checks; no paid model access required
python -m pytest backend/tests -q

# Manual/controlled benchmark (example command interface, not preexisting code)
python evaluation/scripts/run_benchmark.py \
  --dataset evaluation/cases/held_out \
  --systems direct_chat single_role archpilot \
  --output evaluation/runs/run_001

# Recompute deterministic metrics from saved outputs, no new API charges
python evaluation/scripts/score_saved_outputs.py \
  --run evaluation/runs/run_001 \
  --gold evaluation/gold \
  --output evaluation/reports/results.json
```

CLI arguments are proposed interface examples. They should not force a large runner architecture; a short script or notebook plus a Markdown review sheet is sufficient for a solo MVP.

### 12.2 Per-run manifest (keep saved with outputs)

```json
{
  "run_id": "benchmark_001",
  "protocol_version": "1.0",
  "timestamp_utc": null,
  "git_commit": null,
  "dataset_hash": null,
  "gold_hash": null,
  "prompt_hashes": {},
  "model_id": null,
  "model_settings": {},
  "catalog_version": null,
  "rule_set_version": null,
  "case_ids": [],
  "systems": ["direct_chat", "single_role", "archpilot"],
  "reported_results_status": "not_run"
}
```

All null and empty values are **placeholders**, not logged results.

### 12.3 Per-case score sheet

```text
Case ID:
System label (blind where possible):
Brief/answer script version:
Gold critical topics:
Questions asked and matched topics:
Explicit facts captured / missed / falsely confirmed:
Repeated settled topics:
Contradictions detected / missed / false positives:
Graph schema / ARCH findings (if applicable):
Supported capabilities covered:
AWS suggestion IDs and status:
Question relevance (0–3), with evidence:
Rationale (0–3), with evidence:
Adaptive follow-up (0–3), with evidence:
Architecture functional fit (0–3), with evidence:
Explanation/uncertainty (0–3), with evidence:
Total latency, model calls, token usage, estimated cost:
Main failure mode and severity:
Reviewer / review date:
```

### 12.4 Result aggregation

Use total counts and denominators. Example: critical-topic recall = total matched gold critical topics divided by all eligible gold critical topics across evaluated cases. Report per-case values too; macro-average is optional but distinguish it from pooled average. For medians use actual observed samples. Include `N/A` whenever a metric cannot be validly applied (e.g., plain chat has no API state revision).

**Never claim statistically significant superiority, production accuracy, security certification, or general real-customer success from this small benchmark.**

---

## 13. Failure analysis and corrective action

### 13.1 Incident register (minimal table)

| Field | Definition |
|---|---|
| `issue_id` | EVAL-001, EVAL-002, etc. |
| `case_id` and `run_id` | Reproducible reference |
| `stage` | extract / questions / answers / reconcile / design / catalog / validate / review / export |
| `category` | fabricated_fact / missing_question / repeat_question / lost_answer / false_conflict / graph_error / catalog_overclaim / state_control / model_failure / UX |
| `severity` | blocker / major / minor |
| `expected` / `observed` | Concise description with evidence |
| `root_cause_hypothesis` | Prompt / model / reconciliation / contract / rule / catalog / UI / unknown |
| `fix_and_regression_test` | Code/test reference, or `not_fixed` with reason |
| `status` | open / fixed / accepted_risk |

### 13.2 Prioritization

1. **Blocker:** leaks secrets, overwrites facts, bypasses explicit SA action, suppresses critical blockers, or produces incorrect deterministic findings for seeded tests.
2. **Major:** misses high-impact questions repeatedly, fabricates catalog support, or generates noninspectable graphs in common supported cases.
3. **Minor:** awkward phrasing, some redundant questions, cosmetic diagram issues, or optional documentation gaps.

For every fix, add a development regression case and document any benchmark case contaminated by using it for tuning. No “fix by hiding the failed output” practice.

### 13.3 Honest evaluation narrative

The final portfolio report should explain:

- What ArchPilot improved **and did not improve** versus the two baselines.
- Whether two roles contributed benefit after accounting for structured state and the validator.
- Representative customer questions and how they changed later design decisions.
- Most serious residual failures and architecture limitations.
- Which rules are guaranteed by deterministic tests and which qualities remain human-judged.
- Why the MVP deliberately did not include extra agents, advanced cost estimates, or automatic deployment.

---

## 14. Release checklist and evidence package

Use this as the final owner sign-off checklist. Check only after evidence exists.

- [ ] `01-PRD.md` v1.1, `02-SYSTEM-ARCHITECTURE.md` v1.1, `03-DATA-CONTRACTS.md` v1.0 and `04-DEVELOPMENT-PLAN.md` v1.0 remain consistent with the implemented MVP.
- [ ] `CT-001`–`CT-020` completed for in-scope behaviors; all required fixtures pass.
- [ ] Every `ARCH-001`–`ARCH-006` positive/negative and repeatability test passes.
- [ ] Three-round discovery, contradictions, provisional choice and human accept/revise work end to end.
- [ ] The architecture graph is inspectable and service suggestions disclose unsupported/unverified status.
- [ ] No automatic final design approval, false catalog support, or silent confirmed-fact overwrite.
- [ ] Held-out cases, gold annotations, baseline prompts, catalog snapshot and run settings were frozen and recorded.
- [ ] Benchmarks for A/B/C report numerator/denominator, scoring caveats, latency/usage/cost and at least three concrete failure examples if observed (or explicitly state fewer occurred).
- [ ] Human-review scores and any disagreements are preserved.
- [ ] Secrets, private-data restrictions, fail-safe errors, input limits, and reset were verified.
- [ ] Markdown summary includes unresolved blockers, assumptions, rule limitations, and SA review status.
- [ ] Deployment smoke passes; clean setup and README are reproducible.
- [ ] Owner documented remaining open risks and the release/no-release decision.

**Required portfolio artifacts:** `README.md`, implementation-current diagram (not aspirational HLD only), 3-minute walkthrough, sample synthetic brief and screenshots, test results, benchmark table, failure analysis and a short note on architectural trade-offs.

---

## 15. Owner decision points (do not silently finalize)

| ID | Decision to approve | Proposed starting position |
|---|---|---|
| `OD-001` | LLM model and provider for all benchmark arms | Use same provider/model version where available, and freeze settings |
| `OD-003` | Critical question/readiness policy | Keep explicit critical blockers; require provisional SA acknowledgement |
| `OD-005` | AWS catalog entries and maintenance | Freeze one reviewed 10–15-service snapshot for the formal benchmark |
| `OD-009` | Evaluation protocol, reviewer rubric, sample and thresholds | 12 held-out briefs, three arms, 0–3 human rubrics, hard deterministic gates |
| `OD-007` | Deployment posture | Public-data-only, rate/spend-limited demo with reset and secret protection |

**Suggested owner approval questions:**

1. Is three-round discovery an appropriate benchmark for the intended SA workflow, or should the limit be case-dependent within the same cap?
2. Is a 12-case held-out benchmark affordable and large enough for an exploratory portfolio evaluation?
3. Can a second technical reviewer score at least three cases independently?
4. Are the proposed semantic investigation targets reasonable after development-set calibration?
5. What actual API spending ceiling is acceptable for the comparison?

The owner can approve changes before the formal evaluation freeze; update `protocol.md`, record the reason, and avoid retroactive success criteria.

---

## 16. References and consistency map

**Internal project documents (normative):**

1. `01-PRD.md` **v1.1**, especially §§4, 5, 7, 9–12 (`FR-001`–`FR-024`, `NFR-001`–`NFR-013`, user stories `AS-01`–`AS-03`, and `OD-009`).
2. `02-SYSTEM-ARCHITECTURE.md` **v1.1**, especially §§5–7, 12–14 (two-role boundaries, six rules, test layers, no extra services).
3. `03-DATA-CONTRACTS.md` **v1.0**, especially §§4–6 and §10.1 (`CT-001`–`CT-020`; enums and canonical state).
4. `04-DEVELOPMENT-PLAN.md` **v1.0**, especially §§5–10 (`M1-T01`–`M4-T05`, per-task evidence and month gates).

**Revision history**

| Version | Date | Change |
|---|---|---|
| 1.0 | 12 Nov 2026 | Initial four-month MVP evaluation plan. Baseline protocol, discovery and graph metrics, deterministic rule fixtures, 12-case held-out proposal, qualitative rubrics, release gates, and monthly task alignment. |

**Next document in design package:** `CODEBUDDY.md` — repository-level engineering instructions that enforce the approved product scope, contracts, test-before-merge rules, and small-task workflow. It must not implement the evaluation runner or change this protocol by merely being added to the repository.
