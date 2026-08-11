# `harness-gardening`: Agent Harness Alignment and Maintenance

The `harness-gardening` skill helps GitHub Copilot inspect and improve the system
that surrounds an agentic coding workflow. It treats the repository's agent guides,
quality gates, architectural decisions, shared vocabulary, memory bank, and harness
documentation as one connected system rather than as unrelated files.

## What it provides

The skill can:

- inventory how agents are instructed to work;
- map the commands that tell developers and agents whether work is correct;
- classify quality controls as deterministic or semantic, feedforward or feedback;
- detect stale pointers, contradictory commands, dead targets, missing wiring, and
  undocumented checks;
- identify gaps between guidance and enforceable sensors; and
- support narrowly scoped repairs after the user approves the proposed work.

A harness is more than CI. It includes the coding agent and its loop, the project
configuration around that loop, and the local feedback controls that help an agent
know when it is safe to declare a task complete.

Repository discovery and harness analysis use the custom read-only `Gardening
Researcher` subagent by default, with `GPT 5.6 Luna (copilot)` as its configured
model.

## Guidelines, instructions, and skills

A **guideline** is a reusable, project-committed prompt document for thematic
engineering rules, best practices, and conventions. Repositories may keep
guidelines in a dedicated directory, copy them from another source, or use another
local arrangement. The repository's own documented convention is authoritative,
and `AGENTS.md` or an equivalent entry point should state when an agent should load
them. This makes them feedforward harness controls rather than informal advice.

Do not merge these concepts during an audit:

- **Guidelines** establish thematic or domain rules and are deliberately loaded
  through project guidance.
- **Instructions** apply to matching files or paths, commonly through `.instructions.md`
  frontmatter such as `applyTo`.
- **Skills** provide broader task knowledge and workflows, often with progressive
  disclosure through `SKILL.md` and reference files.

For each guideline, the skill checks identity and metadata, ownership, thematic
scope, `AGENTS.md` discoverability, actionable rules, broken references, and whether
precise rules have computational sensor coverage. It preserves the repository's
local format and does not add `applyTo` to a guideline unless that repository
explicitly uses it.

## When to use it

Use the skill when you want to:

- audit or realign a repository's agent harness;
- refresh `AGENTS.md`, `CONSTITUTION.md`, guidelines, instructions, ADRs, glossary,
  memory bank, or harness documentation;
- check whether project guidance agrees with its quality gates;
- repay harness-related technical debt; or
- think through trade-offs in the way a repository guides and evaluates agents.

If the request is only to explore trade-offs, use Reflection mode. If it requests
actual artifact repairs, use Maintenance mode. A regular maintenance run closes
with its report and approved repairs; it does not become an endless loop.

## Operating modes

### Audit and Snapshot

This mode is for inspection, verification, and regular maintenance checks. It:

1. reads the project's entry guidance and referenced knowledge;
2. inventories quality gates, sensors, guides, agent instructions, and explicit
   invocation rules;
3. checks that connected artifacts agree; and
4. reports evidence-based debt without changing files.

Its snapshot covers the preflight entry point, each sensor in the quality gates,
the guide catalog, agent instructions, and automatically detected signals such as
sensor gaps or timing misplacements.

### Maintenance and Repair

This mode runs the audit first, then presents a prioritized repair queue. It can
apply one coherent batch at a time only after the user approves the scope. The
workflow keeps an evidence ledger containing the finding, changed files, reason,
owner, validation, and status. It re-runs relevant checks and scans again after
editing.

Mechanical repairs, such as an unambiguous broken path, can be separated from
changes that require human policy, rationale, definitions, or tacit knowledge.
Accepted ADRs and foundational rules are not silently rewritten.

### Reflection

Reflection is a deliberate question loop for harness design trade-offs. It first
builds a snapshot, then asks one evidence-informed question per iteration, analyzes
the user's answer, and records the resulting tension. It does not edit project
files. After at least three substantive iterations, the user can request a
synthesis and receive a tensions map and, where appropriate, upgrade candidates.

### Closeout

Every maintenance run ends by reporting completed repairs, skipped or blocked work,
remaining debt, checks run, and a suggested trigger for the next maintenance pass.

## What it examines

| Component | Questions it asks |
| --- | --- |
| Quality gates | Do `justfile`, `Makefile`, hooks, CI, and test/build configuration agree on commands and scope? |
| Agent entry guide | Does `AGENTS.md` point to current commands, architecture, guidelines, ADRs, glossary, and memory bank? |
| Foundational rules | Does `CONSTITUTION.md` contain current, enforceable rules rather than stale or invented policy? |
| Scoped guidance | Do guidelines have explicit thematic scope and `AGENTS.md` load wiring, while instructions have valid file-pattern scope and paths? |
| ADRs | Are directories, frontmatter, status links, immutability, and regeneration windows coherent? |
| Shared vocabulary | Does the glossary define only terms whose ambiguity could change implementation or communication? |
| Memory bank | Do indexes, load-when triggers, pointers, and entry-guide links match the current structure? |
| Harness documentation | Do README files, contributing docs, examples, and skill references describe the same workflow? |

## The harness taxonomy

The skill uses two dimensions to make improvement opportunities easier to see:

|  | Guide (feedforward) | Sensor (feedback) |
| --- | --- | --- |
| **Inferential** | Agent instructions, skills, ADRs, and other semantic guidance steer work before it happens. | AI review and LLM-as-judge workflows inspect results using semantic reasoning. |
| **Computational** | LSP servers, MCP servers, codemods, and hooks steer behavior deterministically. | Linters, type checkers, tests, and structural checks measure results deterministically. |

It also records timing (`task-quality-gate`, `phase-quality-gate`, or `CI`) and
regulation category (`maintainability`, `architecture-fitness`, or `behaviour`).
This highlights the core improvement opportunity: when a precise structural rule
exists only in an inferential guide, a deterministic sensor may be able to enforce
it more cheaply and reliably.

## Repair queue and safety rules

Findings are classified as broken wiring, contract drift, contradiction, coverage
gap, obsolete guidance, technical debt, rationale gap, or vocabulary gap. Each
queue item includes:

- an identifier;
- exact evidence such as a path, section, command, or mismatch;
- the agent-loop cost or correctness risk;
- the owning workflow;
- the smallest proposed repair;
- the validation that will prove the repair; and
- a status such as proposed, approved, complete, skipped, or blocked.

The skill prefers repository evidence over assumptions. It does not:

- invent rationale from code or Git history;
- silently change accepted ADRs, project policy, or canonical definitions;
- turn every acronym into a glossary entry;
- copy detailed architecture into an entry guide or memory bank; or
- add generic sensors without evidence that the project needs them.

## What it brings to the user

- **A working map of agent readiness:** maintainers can see how guidance, commands,
  and feedback controls connect.
- **Earlier detection of harness drift:** stale commands and broken pointers are
  found before they mislead an autonomous coding session.
- **Better quality-control economics:** controls can be placed at the right point in
  the loop and classified by cost and determinism.
- **Safer maintenance:** proposed repairs preserve ownership and require approval
  where human policy or rationale is involved.
- **Traceable decisions:** repairs and remaining debt are recorded with evidence and
  validation instead of being treated as undocumented cleanup.
- **A path from reflection to action:** design tensions can be explored first, then
  turned into a focused upgrade plan when the user is ready.

## Output contract

A completed run returns four core artifacts in its final response:

1. a **harness snapshot** with entry points, sensors, guides, and component inventory;
2. an **alignment report** grouped by component and debt class;
3. a **repair ledger** listing changed or deliberately untouched files, owners, and
   reasons; and
4. **validation and remaining work**, including checks, re-scan results, blockers,
   unresolved rationale, and the next-pass trigger.

Audit and Reflection explicitly report that no files were changed. Maintenance can
report success for a component only after that component has been re-scanned.

## In short

The `harness-gardening` skill is a disciplined maintenance workflow for the
instructions and feedback loops that make autonomous development trustworthy. It
connects project guidance to executable quality checks, surfaces evidence-backed
debt, and repairs only what the user has approved.
