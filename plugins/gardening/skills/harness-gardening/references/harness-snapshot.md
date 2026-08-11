# Harness Snapshot Template

Use this as the output structure for the initialization sub-agent scan.
Populate from the actual repository; do not guess.

---

## Harness Snapshot: `<repo-name>`

**Scanned**: YYYY-MM-DD

---

### The Preflight Entry Point

| Item | Value |
|------|-------|
| Primary task-quality-gate command | e.g. `just preflight` / `make check` / `npm run check` |
| Defined in | e.g. `justfile:42` / `Makefile:10` |
| Phase-quality-gate | *(present / absent — confirm with user)* |
| Invocation by agents | How agents are instructed to run it (AGENTS.md, README?) |

---

### Sensor Catalog

List every discovered sensor (feedback control) — every step in every quality gate.
For each sensor, classify it using the taxonomy.

**Timing values**: `task-quality-gate` / `phase-quality-gate` / `CI`
**Type values**: `computational` / `inferential`
**Regulation Category**: `maintainability` / `architecture-fitness` / `behaviour` / `?` (ambiguous)
**Confidence**: omit when confident; add `⚠ low` when the classification is a best-guess

| Order | Step Name | Command / Target | Type | Timing | Duration | Regulation Category |
|-------|-----------|-----------------|------|--------|----------|---------------------|
| 1 | format | `ruff format --check` | computational | task-quality-gate | ~2s | maintainability |
| 2 | lint | `ruff check src/` | computational | task-quality-gate | ~5s | maintainability |
| 3 | typecheck | `mypy src/` | computational | task-quality-gate | ~30s | maintainability |
| 4 | unit tests | `pytest tests/unit` | computational | task-quality-gate | ~45s | behaviour |
| 5 | arch-check | `import-linter` | computational | phase-quality-gate | ~10s | architecture-fitness |
| 6 | ai-review | code-review skill | inferential | task-quality-gate | ~60s | maintainability ⚠ low |
| 7 | e2e tests | `pytest tests/e2e` | computational | CI | ~5min | behaviour |

**Total task-quality-gate (no skips)**: ~Xmin
**Total phase-quality-gate**: ~Xmin
**CI additional**: ~Xmin

---

### Guide Catalog

**Discovery scope**: `AGENTS.md` + `CONSTITUTION.md` + all files they reference, recursively.

#### File-Level Summary

| File | Referenced From | Rules Total | Rules With Sensor Backup | Rules Without Sensor Backup |
|------|-----------------|-------------|--------------------------|------------------------------|
| `AGENTS.md` | root | ~N | ~X | ~Y |
| `CONSTITUTION.md` | root | ~N | ~X | ~Y |
| `.github/copilot-instructions.md` | AGENTS.md | ~N | ~X | ~Y |
| `skills/foo/SKILL.md` | AGENTS.md | ~N | ~X | ~Y |
| … | | | | |

> **Note**: "Rules With Sensor Backup" counts rules whose enforcement is covered by a step
> in the Sensor Catalog above. Cross-reference: see the per-rule breakdown for specifics.

#### Per-Rule Breakdown *(on-demand only — generate when the user asks to drill into a file)*

When requested, produce for each guide file:

| Rule Snippet | Judgment | Has Sensor? | Candidate Tool |
|--------------|----------|-------------|----------------|
| "always add type hints to all functions" | structural | YES → mypy (Sensor row 3) | — |
| "avoid circular imports between modules" | structural | NO | `import-linter` |
| "write clear, concise docstrings" | semantic | NO | *(inferential only — cannot be formalized)* |
| "max 50 lines per function" | structural | NO | `ruff` complexity rules |

**Judgment values**: `structural` (precise, formalizable) / `semantic` (requires LLM judgment) / `both`.

---

### Agent Instruction Files Found

| File / Folder | Present? | Type |
|---------------|----------|------|
| `AGENTS.md` | ✅ / ❌ | inferential guide |
| `CONSTITUTION.md` | ✅ / ❌ | inferential guide |
| `.github/copilot-instructions.md` | ✅ / ❌ | inferential guide |
| `.agents/` folder | ✅ / ❌ | inferential guide (folder) |

---

### Harness Instruction to Agents

Quote exactly what agents are told about how to run the harness and what "done" means:

> _"[exact quote from AGENTS.md, README, or equivalent]"_

If no explicit instruction exists: **ABSENT — agents have no guidance**.

---

### Auto-Detected Signals *(feed into the question loop — do not resolve)*

These are patterns observed in the scan that deserve a probing question in the loop.
Do **not** prescribe solutions here — surface them as inputs to the questioning cycle.

#### Sensor Gaps
Inferential guide rules found with no corresponding computational sensor:

- e.g. `AGENTS.md: "always add docstrings"` → no linter/docstring checker in Sensor Catalog
- e.g. `CONSTITUTION.md: "no direct database access from API handlers"` → no architecture test in Sensor Catalog

#### Timing Misplacements
Sensors that appear to be in the wrong lifecycle position:

- e.g. `inferential sensor (AI review) in task-quality-gate` — expensive, runs on every task change
- e.g. `fast computational sensor (ruff) only in CI` — could be shifted left to task-quality-gate

#### Type Imbalance
Notable imbalances in the harness composition:

- e.g. all sensors are computational, zero inferential sensors — semantic issues never caught
- e.g. zero computational sensors, only inferential guides — no deterministic enforcement at all
- e.g. no guides present — agents receive no feedforward steering at all

---

## When to Load This Document

Load `harness-snapshot.md` when:
- Initializing a harness-gardening session (sub-agent output target)
- Needing to recall what was found in the initial scan
- Cross-referencing a tension against the actual preflight structure
- Keywords: "snapshot", "preflight command", "what did we find", "harness scan",
  "initialization", "sensor catalog", "guide catalog", "upgrade candidate"
