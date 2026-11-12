# ArchPilot — Product Requirements Document (PRD)

| Field | Value |
|---|---|
| Document ID | ARCHPILOT-PRD-001 |
| Version | **1.1 — Simplified four-month MVP** |
| Date | 11 November 2026 |
| Status | **MVP direction agreed; detailed technical choices proposed pending owner review** |
| Owner | Solo developer / aspiring AI Solutions Architect |
| Delivery horizon | Approximately 16 weeks, part-time (planning assumption: 8–12 hours/week) |
| Companion document | `02-SYSTEM-ARCHITECTURE.md` v1.1 |
| Supersedes | `01-PRD.md` v1.0 on MVP priorities and release gates |

> **Implementation authority:** This document is the primary source for **what must be built** in ArchPilot's first release. The v1.0 PRD, v1.0 HLD, and `ArchPilot_CodeBuddy_Development_Blueprint_v1.1.md` describe a larger target vision. Where they conflict with this revised MVP, **this PRD and the matching HLD v1.1 take precedence**. Future-scope ideas are not implementation instructions. Detailed schemas belong in `03-DATA-CONTRACTS.md`; task sequencing belongs in `04-DEVELOPMENT-PLAN.md`.

## 1. Executive summary

**ArchPilot** is a web-based AI assistant for Solutions Architects (SAs) and AI Solutions Engineers. It turns an incomplete customer brief into a structured requirements summary, helps the SA ask the **right follow-up questions**, proposes a **logical system architecture**, suggests suitable services from a **small curated AWS catalog**, and checks the resulting design against **explicit deterministic rules**.

ArchPilot is a **decision-support and review tool**, not an autonomous architect or a compliance certifier. The user makes the final design decisions. The product should distinguish customer-confirmed facts from assumptions and unknowns, and label preliminary designs as **provisional**.

### 1.1 First-release product in one sentence

> Help an SA discover what a customer actually needs, generate an explainable draft architecture from those requirements, and spot known problems before sharing the design.

### 1.2 Four-month outcome

1. **Month 1 — Discover:** An SA enters a brief, receives prioritized questions with explanations, answers them over several rounds, and gets a structured requirements summary.
2. **Month 2 — Design:** A second AI role produces a provider-neutral architecture graph and attaches grounded AWS service suggestions from a small catalog.
3. **Month 3 — Validate and review:** Deterministic checks run against the graph; a simple browser workspace presents the requirements, diagram, findings, and options to revise the design.
4. **Month 4 — Evaluate and deploy:** Test unfamiliar briefs, compare with a single-agent/direct-prompt baseline, fix the most consequential defects, and deploy a public-data-only portfolio demo.

**First-release agent count:** Two AI roles — **Requirements Analyst** and **Architecture Designer**. They may use the **same model/provider** with different instructions and typed outputs; they are not separate servers. The service catalog and validation engine are **ordinary software**, not additional agents.

### 1.3 What makes it more useful than free-form LLM prompting?

- The SA sees the **open questions, reasons, assumptions, and updated answers** in one structured discovery workspace.
- Architecture is represented as **nodes and edges with requirement links**, not only prose or a static picture.
- **Known structural flaws are checked by code**, with repeatable rule IDs and reproducible results.
- The user can revise and **revalidate** a design rather than starting an unstructured conversation from scratch.

We will **test**, not assume, whether these features improve quality or efficiency over direct LLM prompting.

## 2. Decision ledger and scope boundaries

| Area | Status | v1.1 decision |
|---|---|---|
| Primary user and problem | **Agreed** | SAs handling ambiguous early-stage cloud / AI solution briefs. |
| Product focus | **Agreed** | Consultative discovery → logical design → validation/review. |
| Time horizon | **Agreed** | Four-month incremental MVP, not a complete enterprise architecture platform. |
| Agent design | **Agreed** | Start with **two** specialist roles. No independent Cloud Specialist, Reviewer, or Documentation Agent for MVP. |
| Service selection | **Agreed direction** | Use a small, hand-curated AWS catalog as data/tools accessible by the Designer. |
| Verification | **Agreed** | Separate deterministic rule findings from model-generated design advice. |
| User control | **Agreed** | SA reviews/accepts or asks for revision; critical unknowns remain visible; no automatic final approval. |
| Technology | **Proposed** | Python/FastAPI/Pydantic backend, Next.js/React frontend, React Flow when editable diagram is justified. |
| Coordination | **Proposed** | Plain Python functions/services; no LangGraph required for MVP. |
| Storage | **Proposed** | In-memory during early API prototypes; simple durable project persistence before deployed demo, such as SQLite. |
| Hosting | **Open** | Select low-cost deployment in Month 4; portfolio demo contains synthetic/public data only. |
| More agents, complex governance | **Deferred** | Consider only if evaluation demonstrates real user benefit. |
| Automated cost engine, advanced impact graph | **Deferred** | Not needed to demonstrate the core product. |

### 2.1 In scope for MVP

- Text briefs; English for the initial user interface, with multilingual brief interpretation only where supported by the chosen model and tested.
- Structured extraction of functional and non-functional needs, constraints, assumptions, unknowns, and contradictions.
- **Adaptive** discovery with follow-up questions, rationale, priorities, multiple rounds, and explicit decision to proceed provisionally.
- Architecture composition from a **bounded capability vocabulary**; no hardcoded whole-use-case selection.
- Initial AWS service suggestions from roughly **10–15 maintained catalog entries**; unsupported options reported as unknown.
- Architecture graph JSON and an understandable diagram with basic change/review interaction.
- The six named `ARCH-001` through `ARCH-006` checks, bounded to what their rule definitions can verify.
- Basic project save/reload for a usable demo, user acceptance/revision, simple Markdown summary, and comparative evaluation.

### 2.2 Explicitly outside first release

- Automatic deployment of proposed customer architectures; Terraform generation; writing to customer cloud accounts.
- Enterprise IAM/SSO, multi-user approval chains, real customer data, regulatory/compliance certification.
- Full AWS inventory, multi-cloud optimization, real-time price accuracy, workload performance certification.
- Five-role multi-agent pipeline, independent critic/reviewer agent, specialized documentation agent, distributed orchestration infrastructure.
- Full architecture version history with immutable snapshots, graph-based change-impact engine, multi-user collaboration, sophisticated approval workflows.
- Production SLA guarantees or claims that a graph passing checks is production-ready.

## 3. Users and problem context

### 3.1 Primary persona: Solutions Architect / AI Solutions Engineer

**Situation:** A customer supplies a vague or inconsistent brief; the SA needs to prepare clarifying questions, an early design, and a defensible explanation. **Success:** The SA knows what is confirmed, what to ask, which components are proposed, and what is still risky.

### 3.2 Secondary persona: Reviewer / interviewer (demo only)

An external reviewer can inspect a sample brief, see the generated artifacts, reproduce named validator findings, and understand trade-offs. This is **not** a separate authenticated product role in the MVP.

### 3.3 Main problem to solve

Typical customer briefs omit crucial information about volume, peak traffic, budgets, integration boundaries, privacy/data residency, availability, or action permissions. SAs can use ChatGPT or Claude to discuss such gaps, but may lose the decision trail between prompts and find it difficult to verify that a proposed diagram satisfies documented constraints. ArchPilot's narrow opportunity is **a repeatable discovery-to-design workflow**.

## 4. Key user journeys

### UJ-001 — Consultative discovery (primary)

1. SA creates a local project and pastes a customer brief.
2. Requirements Analyst separates **stated facts**, **inferences/assumptions**, **unknowns**, and **contradictions**.
3. SA sees **3–5 prioritized questions per round** (proposed usability default), with *why they matter* and affected architecture decisions.
4. SA answers, skips, defers, or marks not applicable. The app records those statuses without inventing facts.
5. The AI updates the requirements and asks **only relevant remaining/follow-up questions**.
6. SA chooses **Continue discovery**, **Proceed to design**, or **Proceed provisionally**. The system never silently decides that all answers are confirmed.

### UJ-002 — Architecture proposal

1. Architecture Designer receives the selected requirements snapshot and supported capability catalog.
2. Designer proposes reusable logical components and directed connections; each major component has a purpose and requirement link or recorded cross-cutting rationale.
3. Designer suggests supported AWS services where the catalog is sufficient; it explicitly marks unverified or unavailable mappings.
4. Backend parses the graph and prepares a visual diagram. The design is labeled **draft/provisional**, not certified.

### UJ-003 — Validate and refine

1. Validator executes named rule checks and returns errors, warnings, and readiness notes separately.
2. SA inspects an issue and associated graph elements and can request an AI revision or make a basic edit.
3. The graph is revalidated after modification; the user can **accept as reviewed** or leave it in draft.
4. The app exports a concise architecture summary with unresolved issues visible.

### UJ-004 — Compare with direct LLM prompting

Using synthetic, previously unseen briefs, run ArchPilot and a documented direct-prompt/single-agent baseline. Record critical missing questions, seeded structural issues, artifact validity, time/cost, and reviewer-rated usefulness. Report limitations and negative results.

## 5. Functional requirements — stable IDs, revised commitments

**Priority labels:** `MVP` = required for four-month release; `Lite MVP` = simplified behavior required, advanced behavior deferred; `Optional` = only if core is stable; `Future` = specifically **not an implementation task now**. The original **FR-001–FR-024 IDs are preserved** for traceability. Acceptance criteria below replace v1.0 MVP scope where they conflict.

| ID | Requirement | Release | Acceptance criteria (minimum, test or demo) |
|---|---|---|---|
| **FR-001** | Create project from brief | **MVP** | Accept named brief; preserve raw text; reject blank/oversized input; project/session has stable ID. |
| **FR-002** | Extract structured requirements | **MVP** | Separate functional/non-functional, fact/assumption/unknown; output conforms to schema; no invented numerical constraints. |
| **FR-003** | Prioritized clarification questions | **MVP** | High-impact questions include priority, why it matters, and relevant unresolved requirement/decision. |
| **FR-004** | Multi-round adaptive discovery | **MVP** | Three rounds preserve earlier answers; answered questions are not simply repeated; new answers change subsequent questions. |
| **FR-005** | Unknown/deferred/N/A states | **MVP** | User can mark these separately; none is misrepresented as confirmed. |
| **FR-006** | Contradiction handling | **MVP** | “EU-only processing” followed by “US-only inference” is flagged with both claims; not silently overwritten. |
| **FR-007** | Discovery readiness and provisional flow | **MVP** | Explicit readiness state; user can proceed provisionally with labeled open constraints; no auto-approval. |
| **FR-008** | Full discovery audit history | **Lite MVP** | Preserve answers and resolved question state during use and basic save/reload; immutable event history is future. |
| **FR-009** | Capability decomposition | **MVP** | Different briefs reuse vocabulary/building blocks, not full prewritten architecture templates; unknowns called out. |
| **FR-010** | Structured logical architecture graph | **MVP** | Typed nodes/edges, valid references, requirement links, and exportable JSON. |
| **FR-011** | Catalog-backed AWS recommendations | **MVP** | Designer uses ~10–15 curated entries; no unlisted service labeled catalog-verified; rationale/limitations shown. |
| **FR-012** | Detailed architecture alternatives | **Optional** | One meaningful alternative and trade-off when time permits; not a release blocker. |
| **FR-013** | Deterministic `ARCH-001`–`006` validation | **MVP** | Positive/negative fixtures prove each named check; same canonical input/version gives same findings. |
| **FR-014** | Separate AI Architecture Reviewer agent | **Future** | No agent required; users see deterministic findings and may ask Designer for a revision. |
| **FR-015** | Multi-agent coordination | **Lite MVP** | Simple sequential Requirements Analyst → Architect Designer with explicit user pause, error handling and bounded retries; no five-agent orchestrator. |
| **FR-016** | Human review/acceptance | **Lite MVP** | SA explicitly accepts/requests changes for a design identified by ID/revision; this is **not** enterprise immutable approval workflow. |
| **FR-017** | Discovery Workspace UI | **MVP** | SA can enter brief, answer questions and view current requirements/readiness without editing JSON. |
| **FR-018** | Architecture Studio UI | **Lite MVP** | Render graph, inspect node details and findings, request revision; one simple edit-and-revalidate path. Rich editor is optional. |
| **FR-019** | Agent execution transparency | **Lite MVP** | Show current stage, errors and reasons for failed/retried actions; full provider traces are future. |
| **FR-020** | Persistence / immutable versioning | **Lite MVP** | Basic save/reload of brief, answers and current graph; immutable version/event store is future. |
| **FR-021** | Graph-based change-impact analysis | **Future** | On edited inputs/design, re-run checks; automated dependency-diff engine is not required. |
| **FR-022** | Proposal and ADR generation | **Lite MVP** | Export clear Markdown summary containing requirements, design rationale, graph, checks, unknowns and review status; no Documentation Agent. |
| **FR-023** | Cost estimation engine | **Future** | No priced estimates required. If later added, use dated inputs and disclose missing prices. |
| **FR-024** | Evaluation and single-agent comparison | **MVP** | Use held-out synthetic briefs, score defined criteria, publish latency/cost and at least a few failure examples. |

### 5.1 Three must-pass acceptance stories

**AS-01 — Incomplete customer-support brief:** Given 10,000 conversations/day, English + Chinese, internal documentation, sensitive data, and “limited budget,” the Analyst records known facts and asks about **actual budget, geography/data handling, peak load, and whether the assistant only answers or performs actions**. Answers persist across three rounds. It does **not** invent an SLA or monthly spend.

**AS-02 — Contradiction:** After “all customer data must stay in the EU,” the SA records “inference must use a US-only region.” Both statements remain visible until the SA resolves the conflict; the system does not silently accept the latest answer.

**AS-03 — New architecture type:** Given a synthetic invoice-processing brief **not used as an end-to-end template**, the Designer should combine ingestion, processing, data storage and review/notification capabilities as appropriate, explain any unknowns, and produce a schema-valid graph; supported mappings must come from the catalog.

## 6. Non-functional requirements

Original NFR identifiers are retained. Commitments are revised to avoid unnecessary enterprise-grade requirements.

| ID | MVP expectation | How to verify |
|---|---|---|
| **NFR-001 — Privacy** | Synthetic/public data only in demos; no proprietary Tencent/customer materials without authorization. | Test fixture review; README limitation and acceptable-use notice. |
| **NFR-002 — Secrets** | API keys supplied from environment/secret store; never committed or returned to browser. | Repository secret scan and configuration tests. |
| **NFR-003 — Untrusted input** | Treat customer text and catalog descriptions as data, not agent instructions; agents have no shell/cloud-change tools. | Prompt-injection and tool-boundary negative tests. |
| **NFR-004 — Typed output integrity** | Validate LLM outputs against Pydantic models before forwarding. | Malformed-output fixtures fail safely. |
| **NFR-005 — Deterministic rules** | Same input, catalog and rules version → same normalized validator findings. | Repeatability tests. |
| **NFR-006 — Failure handling** | Timeouts, malformed output and limited retries result in visible errors; no infinite agent loops. | Mocked LLM failure tests. |
| **NFR-007 — Requirement traceability** | Nodes have associated requirement IDs or recorded infrastructure rationale; unresolved needs remain visible. | Graph/report inspection. |
| **NFR-008 — Maintainability** | Modular backend, short contracts, automated tests and README. No mandatory microservices. | CI/test run and source review. |
| **NFR-009 — Basic observability** | Correlation/run ID, stage duration and error category logged without secret/PII leakage. | Inspect mocked run logs. |
| **NFR-010 — Usability** | Browser workflow for brief → questions → draft graph → findings without editing raw JSON. | Human demo. |
| **NFR-011 — Cost/performance awareness** | Measure calls, latency and approximate API usage in evaluation; no arbitrary production SLA. | Evaluation results. |
| **NFR-012 — Deployment repeatability** | Document local setup and deploy a demo in Month 4; Docker optional if chosen environment benefits. | Clean-environment start and smoke test. |
| **NFR-013 — Data retention** | Prefer no sensitive data; state/demo data can be cleared or reset. Formal retention policy deferred. | Manual data reset test. |

## 7. Minimal AI roles and software responsibilities

| Element | Primary job | Input | Output | Boundary |
|---|---|---|---|---|
| **Requirements Analyst (AI role)** | Extract, reconcile, ask follow-ups, summarize readiness | Brief + current answers/questions | Typed requirements + question proposals | Cannot approve; may not invent confirmed facts. |
| **Architecture Designer (AI role)** | Choose capabilities, construct candidate graph, explain service suggestions | Chosen requirements + capability/AWS catalog | Typed graph + rationale and catalog-backed suggestions | Cannot certify availability/price or override validation. |
| **Python coordinator (software)** | Call roles in order; manage simple session states and human stops | Session/project state | Updated state and API response | No autonomous agent debate or infinite repair loop. |
| **Catalog module (software/data)** | Supply known capabilities and limited AWS metadata | Catalog query | Curated entries with caveats | No claim of full AWS coverage/current pricing. |
| **Validator (software)** | Run `ARCH-001`–`006` rules | Requirements + graph + catalog semantics | Stable findings | Does not evaluate holistic production readiness. |
| **Browser UI (software)** | Show Q&A, diagram, findings, accept/revise actions | API data | User decisions | Client actions are always server-validated. |

### 7.1 Discovery readiness policy (MVP)

Represent at least three **review states**: `needs_clarification`, `ready_for_design`, `provisional`. A conflict or unanswered critical item prevents automatic `ready_for_design`. The SA may choose **provisional** explicitly, with the unresolved items carried into all drafts and exports. A separate `design_review_status` is `draft`, `accepted_by_sa` or `revision_requested`; **accepted is not certified**. Details are **proposed contracts** for `03-DATA-CONTRACTS.md`.

### 7.2 Deterministic validator rules (preserve stable IDs)

| Rule | Condition | Expected handling |
|---|---|---|
| **ARCH-001** | Duplicate node IDs or duplicate edge IDs | Structural error. |
| **ARCH-002** | Edge references nonexistent source/target node | Structural error. |
| **ARCH-003** | Explicitly required capability has no matching graph element | Coverage error; capability matching uses controlled vocabulary. |
| **ARCH-004** | Node references a nonexistent requirement ID | Structural/traceability error. |
| **ARCH-005** | Catalog semantics require a queue consumer but none is represented/connected | Warning if semantics are uncertain; stronger only with explicit supported evidence. |
| **ARCH-006** | Critical unresolved/contradictory requirement or unaccepted assumption | **Readiness warning/blocker**, not a graph topology error. Provisional design may still be shown. |

No check promises a secure, cost-effective, legally compliant, or production-ready system. Surface the rule coverage and known limitations.

## 8. UX scope: three focused screens

1. **Discovery Workspace** — brief; extracted known/assumed/unknown facts; prioritized questions; answer controls; readiness and explicit provisional choice. **First screen to deliver.**
2. **Architecture Workspace** — architecture diagram and component purpose/requirement links; catalog-backed suggestions and unknowns; validate/revise/accept controls. A generated diagram with a small edit capability meets MVP.
3. **Summary / Evaluation** — concise Markdown export, findings, unresolved assumptions, basic run stats. A dedicated dashboard is optional.

Avoid building separate dashboards, organization settings, service-marketplace views, or comprehensive approvals/version histories in MVP.

## 9. Development scope and legacy Phase 0–8 mapping

The old nine phase labels remain **reference identifiers**, not a mandate to implement their original advanced scope or order. The revised monthly outcomes are the governing delivery plan; update `04-DEVELOPMENT-PLAN.md` accordingly.

| Month | Main outcome | Existing phase IDs repurposed or slimmed |
|---|---|---|
| **1** | Working consultative discovery through minimal UI or test client; answer continuity | Phase 0 foundation; **Phase 2** Analyst/discovery; minimal Phase 5 coordination; early Phase 6 discovery UI. |
| **2** | Design a graph from requirements; support AWS catalog suggestions | **Phase 3** Designer; slim **Phase 4** catalog **without separate agent**; graph schema from Phase 1. |
| **3** | Complete deterministic validation and simple architecture review UI; basic save/reload | **Phase 1** named rules; Phase 6 architecture UI; **Phase 7** basic persistence only; Phase 5 user decisions. |
| **4** | Evaluate on new briefs, refine and deploy | **Phase 8** evaluation/export/deploy. |

**Sequencing caveat:** Graph schemas and a minimal validator can begin in Month 2, before final validation work in Month 3. Similarly, a minimal Discovery UI can precede the full Architecture Studio. Nothing requires building a Reviewer or Documentation Agent at the original Phase 5/8 milestones.

### 9.1 Month-by-month exit gates

- **M1:** Three-round discovery demonstrated; important questions prioritized, prior answers preserved, contradiction and provisional handling visible.
- **M2:** At least two different synthetic brief types yield inspectable, schema-valid candidate graphs; grounded catalog suggestions and unknowns shown.
- **M3:** All six ARCH checks pass seeded tests; SA can view findings, revise and revalidate a design, and reopen a saved sample project.
- **M4:** Deployed demo works with synthetic/public data; evaluation uses held-out briefs and publishes comparison results, limitations and setup instructions.

## 10. Evaluation and success criteria

Evaluation must answer **whether ArchPilot offers value beyond a direct LLM conversation**, not only whether its UI looks convincing.

| Area | Core measurement | Proposed release expectation |
|---|---|---|
| Discovery usefulness | Recall of labeled critical missing questions; repeated resolved questions | Review 10–20 synthetic briefs; report actual recall/repetition, with failure cases. |
| Requirements integrity | Loss or silent overwrite of confirmed answers | Zero in the deterministic state tests; contradictions preserved. |
| Graph integrity | Schema validity and seeded `ARCH-001`–`006` behavior | All written positive/negative fixtures pass. |
| Generalization | Supported components composed for held-out brief types | Show at least two materially different workloads; disclose unsupported capabilities. |
| User decision control | Accidental implicit acceptance | Zero in acceptance tests. |
| Compared with baseline | Human-reviewed quality, elapsed time, call count/token cost | Use equivalent reference information where feasible; publish measured trade-offs, including unfavorable ones. |

**Target values for semantic AI quality** should be baselined before declaring percentage thresholds. Evaluation must identify which dimensions are human-rated and which are deterministic.

## 11. Risks, mitigations, and assumptions

| Risk | Why it matters | Response |
|---|---|---|
| Scope creep | Five agents, full visual editing, cost engine and version history exceed a solo MVP. | Protect the three core jobs; treat future features as out-of-scope. |
| Hallucinated requirements | Model may invent numbers, regions or policies. | Source labels, typed output, SA verification, readiness checks. |
| Hallucinated cloud advice | Service information may be incomplete or stale. | Small curated catalog with provenance, unverified markers and no pricing guarantee. |
| Agent errors / latency | Multiple model calls may be slow or inconsistent. | Two roles, bounded retries and error states; evaluate against one-agent baseline. |
| Unreliable architecture score | A few checks cannot certify real-world quality. | Explain exact rule coverage and need for professional review. |
| Confidentiality | User may paste internal briefs. | Synthetic/public-only MVP; do not collect private Tencent/company data in demos. |
| Documentation drift | Old blueprint implies broader MVP. | PRD/HLD v1.1 take precedence; revise development plan and instructions before coding. |

**Assumptions:** Part-time solo delivery; one LLM provider initially; limited budget to be set by the owner; cloud-service evidence manually curated; no requirement to connect to actual AWS or customer infrastructure; one SA user per demo.

## 12. Decisions still requiring approval

| ID | Proposed decision | Decide by |
|---|---|---|
| OD-001 | LLM provider/model and structured-output API | Before Month 1 Analyst integration |
| OD-002 | Simple Python coordinator rather than agent framework | Before Month 2 agent handoff |
| OD-003 | Exact critical-question/readiness policy | Before first discovery acceptance test |
| OD-004 | Canonical graph and edge semantics | Before graph generation |
| OD-005 | AWS catalog entries, allowed evidence, update method | Before service suggestions |
| OD-006 | Local JSON/SQLite persistence and migration approach | Before Month 3 save/reload |
| OD-007 | Deployment host and safeguards for public demo | Before Month 4 deployment |
| OD-008 | Small-edit UI versus read-only diagram plus revision prompt | Before Month 3 frontend build |
| OD-009 | Benchmark protocol and scoring rubric | Before Month 4 evaluation |

These are *proposals*, not silent commitments. No approval of a PRD implies automated approval of an AI-generated customer architecture.

## 13. Acceptance and governance

**MVP accepted when:** (a) all **MVP/Lite MVP** acceptance behaviors are demonstrated, with any explicitly approved deferrals documented; (b) user can complete multi-round discovery, generate a candidate design, receive deterministic findings, request and inspect revisions, and export a reviewable summary; (c) a deployed demo and evaluation evidence exist; and (d) limitations and unknowns are transparent.

**Document hierarchy:** `01-PRD.md` (product scope) → `02-SYSTEM-ARCHITECTURE.md` (system design) → `03-DATA-CONTRACTS.md` (schemas/endpoints) → `04-DEVELOPMENT-PLAN.md` (task order) → `05-EVALUATION-PLAN.md` (benchmarks) → `CODEBUDDY.md` (coding guidance). The old blueprint is **historical context**, not independent current scope authority.

**Change control:** Preserve stable `FR-*`, `NFR-*`, `ARCH-*`, and `OD-*` IDs. Meaningful scope changes require updating this PRD and checking the HLD; implementation refactors belong in technical docs/ADRs. Have CodeBuddy/Codex propose changes instead of silently expanding the system.

### Revision log

| Version | Change |
|---|---|
| 1.0 | Broad five-agent, complex approval/versioning and change-impact target. |
| **1.1** | **Agreed** four-month streamlined MVP: two agents; discovery first; catalog as data; deterministic validator; simpler UI/persistence; Reviewer, Documentation Agent, advanced history/impact and costing deferred; IDs preserved. |

*End of ArchPilot PRD v1.1 — draft technical details for owner approval.*
