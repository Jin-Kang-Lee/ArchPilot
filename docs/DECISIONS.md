# Owner Decision Ledger

Append-only record of decisions approved by the project owner. Normative scope stays in
`Markdown/01_PRD_v1.1.md` … `05-EVALUATION-PLAN.md`; this ledger records *when* a choice was
approved and *where* the spec text still has to catch up. Do not use it to add scope.

---

## D-001 — Baseline technology choices (approved 12 Nov 2026)

- Python **3.12**, dependencies managed with **uv**
- **FastAPI** + **Pydantic v2**
- **pytest** for tests, **Ruff** for lint/format
- **SQLite** chosen for lightweight persistence, introduced no earlier than `M3-T04`
- No ORM, no agent framework, no LLM SDK in the foundation task

Related: `OD-002`, `OD-006`, PRD §2.

## D-002 — LLM provider deferred, design stays provider-agnostic (approved 12 Nov 2026)

`OD-001` is **not** decided. No model SDK, API client or provider-specific field may enter
the codebase before `M1-T03` is approved. Agent boundaries must remain behind a thin
adapter so a provider can be chosen later without touching canonical models.

Related: `OD-001`, `03-DATA-CONTRACTS.md` §13.

## D-003 — Queue → consumer edge kind is `consumed_by` (approved 12 Nov 2026)

The HLD/contract text currently defines queue consumption as an edge of kind `consumes`
with the **queue as source** (`queue -> consumes -> worker`), which reads backwards.

Approved resolution: the directed edge is **`queue -> consumed_by -> worker`**
(`GraphEdgeKind` gains `consumed_by`; `consumes` remains available for consumer → dependency
statements if needed).

**Not yet applied to the specs.** Must be reflected, in this order, when each artifact is
touched:

1. `03-DATA-CONTRACTS.md` §3.3 `GraphEdgeKind` enum and §6.2 `ARCH-005` policy.
2. `02-System_Architecture_v1.1.md` §7.2 `ARCH-005` row.
3. `M2-T01` (graph DTOs) and `M3-T01` (`ARCH-005` implementation + fixtures).

Until `M3-T01`, no code may emit or validate queue-consumer edges using the old `consumes`
direction. `ARCH-005` detection logic must be `message_queue` source + `consumed_by` edge +
target node carrying `async_worker`.

Related: `OD-004`, `ARCH-005`.

## D-004 — Deterministic validator stays framework-free (approved 12 Nov 2026)

Validation logic lives under `app/rules/` as pure functions over Pydantic objects. It must
import no FastAPI, no HTTP client and no model SDK, and must be testable offline
(NFR-005). HTTP routes call the rules; the rules never call routes.

Related: `NFR-005`, `M3-T01`.

## D-005 — Minimal revision check, no merge workflows (approved 12 Nov 2026)

`state_revision` / `expected_graph_revision` fields are retained and stale writes are
rejected with `409 REVISION_CONFLICT`. No operational transform, three-way merge, conflict
UI or multi-writer reconciliation will be built.

Related: `OD-006`, `CT-016`.

## D-006 — Discovery readiness policy confirmed (approved 12 Nov 2026)

Critical unresolved requirements, open contradictions and unaccepted critical assumptions
prevent `ready_for_design`. The SA may explicitly choose `provisional`, which must keep the
blocking IDs visible in state, graph payloads and exports. Models and clients can never set
`ready_for_design` or `accepted_by_sa`.

Related: `OD-003`, `FR-006`, `FR-007`, `ARCH-006`.

## D-007 — `M1-T01` scope boundary (approved 12 Nov 2026)

Approved for implementation: backend bootstrap, `GET /health` returning exactly
`{"status": "ok"}`, pytest health test, Ruff configuration, minimal local instructions.

Not approved in this task: AI agents, LLM adapters, persistence, frontend, validation
rules, capability vocabulary, synthetic brief fixtures. `M1-T02` requires separate approval.

Related: `04-DEVELOPMENT-PLAN.md` §5 `M1-T01`.
