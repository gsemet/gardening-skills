---
name: harness-gardening
description: 'Audit, realign, and incrementally improve a repository agent harness while preserving evidence, ownership, and approval boundaries.'
metadata:
  keywords: [harness, preflight, agent-loop, lint, testing, feedback-loop, harness-engineering, justfile, makefile, agent-readiness, dx, adr, glossary, tech-debt, maintenance]
  recommended-models: [GPT 5.6 Luna (copilot)]
---

# harness-gardening

Maintain the repository's agent harness as a connected system. A harness includes
the agent-facing guides, deterministic quality gates, architectural decision records,
shared vocabulary, memory bank, and the documentation that wires them together.

This skill is the standalone owner of harness audits and approved harness repairs. It
discovers evidence, identifies drift and debt, and applies repairs using the artifact
contracts in [`references/artifact-contracts.md`](references/artifact-contracts.md).
It does not invent a second format for existing project artifacts.

Use the custom agent named `Gardening Researcher` as the default read-only
subagent for repository discovery and harness analysis. If that custom agent is
unavailable, use an equivalent read-only subagent and report the fallback.

## Mutation boundary

Audit and Reflection modes do not change files. Maintenance mode applies only repairs
that the user explicitly approves, one coherent batch at a time, through the owning
workflow. Never silently change project policy, accepted ADRs, domain definitions, or
uncertain tacit knowledge.

## When to Use It

Use this skill when the user asks to:

- audit or realign a repository's harness;
- refresh `AGENTS.md`, `CONSTITUTION.md`, guidelines, instructions, ADRs, glossary,
  memory bank, or harness documentation;
- repay harness-related technical debt;
- check whether quality gates and agent guidance still agree; or
- run a regular harness-maintenance pass.

If the user asks only to explore trade-offs, use **Reflection mode**. If the user asks
to refresh or repair artifacts, use **Maintenance mode**. A regular maintenance run
terminates after its report and approved repairs; only Reflection mode is an infinite
question loop.

## What Is a Harness

The Agentic Harness is the infrastructure that is put in place around the LLM.
It includes the coding agent, its loop and configuration, and the infrastructure
provided by the project developer.

This skill focuses on optimizing the **project's specific agentic harness**,
especially the **feedback loops run inside the agent coding cycle**: the checks an
agent or developer runs to know work is correct before declaring done. CI is a related
sensor and source of drift, but the harness must remain usable inside the local loop.

The simplest harness: one target that runs everything (`just preflight`,
`make check`, `npm run check`). `preflight` or `all` or `quality-gates` are
common names.

That is the ideal starting point.
The challenge is that as a project grows, this single target becomes
too slow, too broad, or poorly sequenced — and optimization requires
deliberate choices.

## The Taxonomy (Fowler)

Every harness control belongs to one of four quadrants:

|  | Guide (feedforward) | Sensor (feedback) |
|--|---------------------|-------------------|
| **Inferential** | AGENTS.md, CONSTITUTION.md, guidelines, skills, copilot instructions, ADRs (`.agents/adr/`) — steer the agent before it acts using semantic/LLM reasoning | AI code review, review agents, LLM-as-judge — observe output after the agent acts using semantic analysis |
| **Computational** | LSP servers, MCP servers, codemods, pre-commit hooks — steer the agent deterministically | Linters, type checkers, tests, structural analysis — observe output deterministically |

**Key properties:**
- **Computational controls** are deterministic, fast (milliseconds to seconds), cheap to run on every change.
- **Inferential controls** are semantic, slower, more expensive, non-deterministic — valuable for judgment that cannot be formalized.
- **Guides (feedforward)** increase the probability of good results on the first attempt.
- **Sensors (feedback)** allow the agent to self-correct after the fact.

**The core upgrade insight**: when an inferential guide contains a rule that is
*precise and structural* (e.g., "always add type hints", "no circular imports",
"max function length 50 lines"), a computational sensor can enforce it
deterministically. The inferential guide says the rule; the computational sensor
catches violations. Rules requiring *semantic judgment* (e.g., "avoid over-engineering")
cannot be formalized — they stay inferential.

**Three regulation categories** help organize what the harness is supposed to govern:
- **Maintainability** — code quality, style, complexity, test coverage
- **Architecture fitness** — module boundaries, conventions, performance budgets
- **Behaviour** — functional correctness, specification conformance

## What Is a Guideline?

A **guideline** is a reusable, project-committed prompt document that states
thematic engineering rules, best practices, and conventions developers or coding
agents must follow. A repository may keep guidelines in a dedicated directory,
copy them from another source, or use a different local arrangement. Treat the
repository's own documented convention as authoritative. A guideline is part of
the repository's feedforward harness, not an informal note or a generic
recommendation.

Keep these resource types distinct during an audit:

| Resource | Purpose | Scope and loading | Audit question |
|---|---|---|---|
| **Guideline** | Establish project rules, patterns, and conventions | Thematic or domain scope; normally loaded through an `AGENTS.md` pointer and an explicit “when to load” instruction | Is the file committed, discoverable, scoped, actionable, and consistent with the project? |
| **Instruction** | Apply coding guidance to matching files or paths | File-pattern scope, commonly expressed with `.instructions.md` frontmatter such as `applyTo` | Does the pattern match the intended files and avoid unintended overlap? |
| **Skill** | Provide reusable domain knowledge and a workflow | Broad task scope with progressive disclosure through `SKILL.md` and references | Is the skill triggered, internally wired, and consistent with its references? |

When a repository defines a guideline convention, inspect guideline files for the
metadata and structure required by that repository, and for a clear rule-oriented
body. Do not force a guideline to use `applyTo`: that field belongs to file-pattern
instructions unless the repository explicitly defines another convention. Preserve
the local format when it differs, but make the scope and load trigger equally
explicit.

### Audit scoped guidance

For every guideline or instruction discovered:

1. Find its source and installed copy, then verify that the installed file is
  committed and that `AGENTS.md` points to it when the project expects deliberate
  loading.
2. Record its scope, load trigger, owner, and rule categories. Treat a missing or
  ambiguous scope as a **coverage gap**, not as permission to invent a rule.
3. Check links, referenced paths, commands, examples, and version-sensitive claims
  against the repository. Mark stale or contradictory guidance with exact evidence.
4. Compare precise structural rules with the sensor catalog. Record whether each
  rule has computational enforcement, inferential review only, or no sensor.
5. Separate a broken pointer or malformed contract from a policy change. Repair the
  former only when unambiguous; obtain approval before changing the latter.

Load [`references/artifact-contracts.md`](references/artifact-contracts.md) for the
detailed guideline and instruction contract before inspecting or repairing these
files.

## Operating Modes

### Mode A — Audit and Snapshot

Use when the user asks to verify, inspect, assess, or run a regular check.

1. Read the project entry guidance and the referenced knowledge sources.
2. Inventory the harness and produce the structure from
   [`references/harness-snapshot.md`](references/harness-snapshot.md): quality gates,
   sensors, guides, agent instructions, and explicit invocation rules.
3. Cross-check the connected artifacts listed in **Component Alignment** below.
4. Report stale pointers, contradictions, missing wiring, obsolete instructions,
   dead targets, undocumented checks, unresolved placeholders, and other evidence-based
   debt. Do not change files in audit-only mode.

### Mode B — Maintenance and Repair

Use when the user asks to refresh, realign, garden, fix, or repay harness debt.

1. Run Mode A first and present a prioritized repair queue grouped by component.
2. Ask for approval when the requested scope is ambiguous or a repair changes project
   policy. Do not silently change accepted ADRs, domain definitions, or foundational rules.
3. Apply one coherent repair batch at a time, preserving each component's owner and
   format. Keep an evidence ledger: finding, files changed, reason, and validation.
4. Re-run the relevant checks and repeat the snapshot scan until the approved scope is
   aligned or a blocker is documented.

### Mode C — Reflection

Use when the user asks to think through harness trade-offs or optimize without asking
for edits. Build the snapshot, confirm its accuracy, then run the question loop below.
Produce a tensions map only after at least three substantive iterations and an explicit
request for synthesis. Do not edit project files in this mode.

### Mode D — Closeout

At the end of any maintenance run, report completed repairs, skipped or blocked items,
remaining debt, checks run, and the suggested trigger for the next maintenance pass.

## Component Alignment

Load [`references/artifact-contracts.md`](references/artifact-contracts.md) when the
audit reaches onboarding files, ADRs, glossary content, memory-bank content, or git
history. It contains the local contracts and approval boundaries needed to inspect or
repair those artifacts without relying on another workflow.

Treat these as one system and check both content and wiring:

| Component | Check | How this plugin handles it |
|---|---|---|
| Quality gates | `justfile`, `Makefile`, task runner, hooks, CI, test/build configs agree on commands and scope | This skill; load `references/justfiles-optim.md` when relevant |
| Agent entry guide | `AGENTS.md` points to current commands, architecture, guidelines, ADRs, glossary, and memory bank | This skill; use the artifact contracts reference |
| Foundational rules | `CONSTITUTION.md` contains only current, enforceable project rules | This skill; use the artifact contracts reference |
| Scoped guidance | Guidelines and instructions have explicit, non-overlapping scope, valid metadata or pattern declarations, correct `AGENTS.md` wiring, and no stale paths | This skill; load `references/artifact-contracts.md` |
| ADRs | Directory, frontmatter, status links, immutability, and regeneration-window state are coherent | This skill; use the artifact contracts reference |
| Shared vocabulary | `.agents/glossary/index.md` and glossary files follow the project glossary contract and are linked where needed | This skill; use the artifact contracts reference |
| Memory bank | `INDEX.md`, load-when triggers, pointers, and `AGENTS.md` wiring reflect current structure | This skill; use the artifact contracts reference |
| Harness documentation | README, contributing docs, skill references, and examples describe the same workflow | This skill |

### Alignment Rules

- Prefer repository evidence over assumptions. Mark unknown rationale as unknown.
- Fix broken pointers and mechanically verifiable drift directly only when the target
  is unambiguous; ask before changing policy or tacit knowledge.
- Accepted ADRs are immutable outside an explicitly open regeneration window. If an
  ADR needs new rationale, interview the user and use the ADR contract in
  `references/artifact-contracts.md`; if candidates must be mined from git, inspect
  history for decisions that remain observable and present the evidence before asking
  the user to select candidates.
- Do not turn a code observation into an ADR automatically. ADRs document expensive,
  non-obvious decisions and require human rationale.
- Do not expand a glossary into an acronym dump. Keep only terms whose ambiguity could
  change implementation or communication, and resolve definitions with the user.
- Do not copy detailed architecture or code into `AGENTS.md` or a memory bank. Keep
  entry guides pointer-based and keep the memory bank token-efficient.
- Generated artifacts must be regenerated by their project command, not hand-edited.
- Never claim alignment until the relevant command, link, frontmatter, or file path has
  been checked after the repair.

## Artifact Repair Boundaries

Use the local artifact contracts reference for the format, interview, immutability,
and validation rules of each harness artifact. Apply only approved changes. Keep
mechanical repairs separate from changes that require human policy, rationale,
definition, or tacit-knowledge decisions.

## Maintenance Queue

Classify findings before proposing repairs:

| Class | Examples | Default action |
|---|---|---|
| Broken wiring | Link or pointer targets a missing file; command name no longer exists | Repair after verification |
| Contract drift | Frontmatter, ADR status links, glossary shape, or memory-bank index is invalid | Apply the local contract, then validate |
| Contradiction | Guide says one command while CI or the task runner executes another | Present evidence and request policy choice |
| Coverage gap | A quality rule has no sensor, or a sensor is not documented | Recommend a targeted change; do not add generic checks |
| Obsolete guidance | Rule describes removed tooling or workflow | Confirm before removal or replacement |
| Tech debt | Dead target, stale workaround, unresolved placeholder, duplicated instruction | Prioritize by agent-loop cost and risk |
| Rationale gap | Observable expensive decision has no ADR or has missing rationale | Gather evidence, interview the user, and propose an ADR |
| Vocabulary gap | Ambiguous project term causes inconsistent guidance | Gather evidence, resolve the meaning with the user, and update the glossary |

Each queue item should include:

```text
ID: HG-###
Class: <class above>
Evidence: <file path and exact section, command, or observed mismatch>
Impact: <agent-loop cost or correctness risk>
Owner: this skill
Action: <smallest proposed repair>
Validation: <specific command, link check, or re-scan>
Status: proposed | approved | complete | skipped | blocked
```

## Reflection Loop

This loop is used only in Reflection mode. Exit when the user explicitly says `done`
or `stop`.

### Initialization

Use a read-only explorer to build the Harness Snapshot. Include:

- every step in every local quality gate and relevant CI gate;
- computational versus inferential type, timing, regulation category, and duration;
- `AGENTS.md`, `CONSTITUTION.md`, referenced guidelines, instructions, skills, ADRs,
  glossary, and memory-bank guide coverage;
- phase-gate candidates discovered in task-runner files, presented for confirmation;
- sensor gaps, timing misplacements, type imbalance, and ADR-wiring gaps.

Present the snapshot and signals before asking the first question. Load
[`references/harness-snapshot.md`](references/harness-snapshot.md) for the output contract.

### Iteration

```text
<loop_iteration N>
  1. REFLECT — state the current harness hypothesis
  2. QUESTION — use `vscode_askQuestions` for one probing question from
     references/question-bank.md
    3. ANALYZE — dispatch the `Gardening Researcher` custom agent as a read-only
      subagent using the user's answer
  4. SURFACE — state the evidence-backed tension; do not resolve it
  5. UPDATE — append the finding to .agents/thinking/harness-gardening/log.md
  6. CONTINUE — ask whether to continue or stop
</loop_iteration>
```

Questions must surface a trade-off the snapshot cannot answer. Never ask a
question whose answer is already in the snapshot. For each analysis subagent, return
file paths, quotes, and the tension or gap; do not ask it to prescribe a solution.

### Synthesis

After three or more substantive iterations, when the user asks what to change, load
[`references/synthesis-guide.md`](references/synthesis-guide.md). Produce its Tensions
Map and, when applicable, its Upgrade Candidates appendix. Recommendations are separate
from approved repairs.

## Output Contract

Every completed run returns:

1. **Harness snapshot** — entry points, sensors, guides, and component inventory.
2. **Alignment report** — findings grouped by component and debt class, with evidence.
3. **Repair ledger** — files changed or deliberately left untouched, with owner and reason.
4. **Validation** — commands, link/frontmatter checks, and the final re-scan.
5. **Remaining work** — skipped, blocked, unresolved-rationale, and next-pass items.

In audit-only or Reflection mode, the repair ledger must explicitly say that no files
were changed. In Maintenance mode, do not report success for a component that was not
re-scanned after editing.

## Anti-Goals

- Do not produce lists of generic best-practices. The user already knows them.
- Do not silently edit project policy, accepted ADRs, tacit glossary definitions, or
  uncertain memory-bank content.
- Do not invent rationale from code or git history.
- Do not add generic sensors or “best practices” without project evidence.
- Do not replace human rationale with a guess or bypass an approval boundary.
- Do not call CI “the harness” while ignoring the local agent feedback loop.

## Taxonomy Reference (Quick Cheat-Sheet)

| Dimension | Values |
|---|---|
| Direction | `guide` (feedforward) / `sensor` (feedback) |
| Execution type | `computational` (deterministic, CPU) / `inferential` (semantic, GPU/LLM) |
| Timing | `task-quality-gate` / `phase-quality-gate` / `CI` |
| Regulation category | `maintainability` / `architecture-fitness` / `behaviour` / `?` (ambiguous) |
| Confidence | *(omit if high)* / `confidence: low` |

The most impactful harness improvement is usually: find an **inferential guide rule**
that is precise and structural → verify no computational sensor exists for it →
recommend the computational sensor. This converts a probabilistic control into a
deterministic one at lower cost.

## Reference Materials

| File | When to load |
|---|---|
| [`references/justfiles-optim.md`](references/justfiles-optim.md) | Project uses `just`, `make`, `task`, or a similar task runner with CI targets |
| [`references/gitlab-ci-optim.md`](references/gitlab-ci-optim.md) | Project uses GitLab CI/CD and its pipeline is slow, monolithic, or hard to reproduce locally |
| [`references/harness-snapshot.md`](references/harness-snapshot.md) | Capturing the current state of the harness before planning optimizations |
| [`references/question-bank.md`](references/question-bank.md) | Interviewing a developer about the harness to identify improvement areas |
| [`references/synthesis-guide.md`](references/synthesis-guide.md) | Synthesizing findings from the harness review into an optimization plan |
