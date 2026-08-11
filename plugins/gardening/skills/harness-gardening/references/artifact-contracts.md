# Harness Artifact Contracts

Use this reference when auditing or repairing repository guidance and knowledge
artifacts. It keeps the harness workflow self-contained: no other skill or package
is required to interpret, interview about, or update these artifacts.

## AGENTS.md and CONSTITUTION.md

`AGENTS.md` is the concise entry point for coding agents. Keep it pointer-based and
preferably under 200 lines. It should identify the project, stack, setup commands,
quality commands, project structure, architecture pointers, and contribution checks.
Do not copy detailed architecture or source code into it.

`CONSTITUTION.md` contains a small set of enforceable, durable rules for modifying,
evolving, testing, documenting, and releasing the project. Do not invent rules or
rationale. Keep project facts in `AGENTS.md` and foundational constraints in the
constitution.

When both files exist, use this default priority unless the repository documents a
more specific accepted order:

1. Accepted ADR constraints
2. `CONSTITUTION.md`
3. Scoped guidelines and instructions
4. `AGENTS.md`
5. Task-specific skills and prompts

If `.agents/adr/` exists, `AGENTS.md` should include an ADR Constraints section:

```markdown
## ADR Constraints

Before implementing a backlog task, scan `.agents/adr/` frontmatter (`title`, `status`).
Read the full body only for relevant ADRs. `status: accepted` overrides conflicting task
descriptions — note the conflict and do not implement the contradicted approach.
```

For every pointer added to `AGENTS.md`, verify that its target exists or is explicitly
optional. Check commands against the task runner or CI configuration before documenting
them.

## Scoped Guidelines and Instructions

A **guideline** is a reusable, project-committed prompt document that describes
thematic engineering rules, best practices, or conventions for developers and
coding agents. A repository may keep guidelines in a dedicated directory, copy
them from another source, or use a different local arrangement. Use the repository's
own documented convention as authoritative, and require `AGENTS.md` or an equivalent
entry point to state when the agent should load them. A guideline is feedforward
harness guidance: it establishes boundaries before work begins.

Do not confuse a guideline with:

- an **instruction**, which is usually file-pattern-scoped and commonly declares an
   `applyTo` glob in `.instructions.md` frontmatter; or
- a **skill**, which provides broader task knowledge and an executable or procedural
   workflow, often split across `SKILL.md` and progressive-disclosure references.

### Guideline contract

When a repository defines a guideline format, a guideline normally has:

- descriptive frontmatter containing `name` and `description`;
- relevant `metadata`, commonly including `owner`, `keywords`, and `guideline-id`;
- a title and purpose explaining the engineering concern;
- actionable rules or conventions, with rationale or examples where useful; and
- validation guidance when the rules can be checked by commands, tests, or review.

The project may use `.agents/guidelines/`, `.github/guidelines/`, or another
documented directory. Treat the repository's own convention as authoritative. Do
not add `applyTo` to a guideline merely to make it resemble an instruction file.
Instead, verify that its thematic scope and load trigger are explicit in the file,
its parent index, or `AGENTS.md`.

### Guideline audit

For each guideline, record:

| Field | Verification |
|---|---|
| Identity | Name, path, frontmatter, and any catalog/source identifier agree |
| Ownership | An owner or responsible team is identifiable when the local convention requires it |
| Scope | The affected domain, artifact type, or workflow is stated and does not unintentionally overlap another guide |
| Discoverability | `AGENTS.md` or the project guide points to the file and says when to load it |
| Rule quality | Rules are specific and actionable rather than generic advice or copied documentation |
| Wiring | Links, referenced paths, commands, examples, and version claims resolve against repository evidence |
| Sensor coverage | Precise structural rules are mapped to computational sensors; semantic rules are marked inferential or unsensed |
| Lifecycle | The file is committed, maintained by a clear owner, and not an obsolete duplicate of an instruction or skill |

Classify a missing pointer, invalid frontmatter, or stale path as broken wiring or
contract drift when the repair is unambiguous. Classify an unclear scope, changed
rule, or disputed definition as a review-needed policy decision. Never invent a
guideline's rationale, owner, canonical definition, or sensor just to complete the
checklist.

## Architecture Decision Records

Use an ADR for a decision that is expensive to reverse and non-obvious from the
current code. Do not create ADRs for routine feature delivery, dependency updates,
style choices, or implementation details with no durable rationale.

Prefer `.agents/adr/`; accept `.github/adr/` when that is the repository convention.
Use filenames in the form `ADR-NNN-short-kebab-title.md` and hybrid Markdown plus YAML
frontmatter:

```yaml
---
id: ADR-NNN-short-title
title: 'Short title of solved problem and solution'
status: proposed
supersedes: null
superseded_by: null
---
```

An ADR must cover context and problem, decision drivers, considered alternatives,
decision outcome, rationale, consequences, and links. If rationale is unknown, write
`_Information not available — to be enriched by the team._` rather than guessing.

Valid lifecycle states are `proposed`, `accepted`, `rejected`, `deprecated`, and
`superseded`. Accepted ADRs are immutable: record a changed decision in a new ADR and
link the two records through `supersedes` and `superseded_by`.

Interview humans for the WHY. Code and git history establish observable facts and the
WHAT, but do not prove intent. Do not write an ADR until the user has reviewed the
proposed sections and explicitly approved the draft.

### Mining ADR candidates from git

When a brownfield repository lacks ADR coverage, inspect commits, renames, additions,
dependency changes, and hotspots. Keep only decisions that:

1. made a structural or business-logic change;
2. remain observable in the current repository; and
3. are non-obvious without external knowledge.

Group candidates by theme, show commit or file evidence, identify uncertainty, and let
the user select candidates. A candidate list is evidence, not a decision. Preserve
existing ADR links and never remove an accepted ADR without an explicit superseding or
deprecation decision.

For incremental ADR work, an optional `.regeneration-window` marker in the ADR directory
means the collection is open for enrichment. When it is absent, accepted ADRs remain
immutable and further changes require a superseding ADR. Report proposed drafts with
missing sections before closing an open window.

## Project Glossary

A glossary records only project-specific terms whose ambiguity could change
implementation, review, testing, requirements, ownership, or communication. It is not
an acronym list, dictionary, or replacement for domain documentation.

Use this structure when a glossary is needed:

```text
.agents/glossary/
├── index.md
└── common.md
```

`index.md` should be a short navigation page. `common.md` should contain a heading and
one concise definition paragraph per term, ordered alphabetically. Do not add a
`Definition:` label, speculative synonyms, evidence sections, or mini-articles.

Before writing a definition, inspect source, tests, configuration, documentation, and
existing ADRs. Resolve competing meanings with the user. Never infer a canonical
meaning from one isolated occurrence. If no term qualifies, keep an empty glossary
header and report that outcome.

## Memory Bank

A memory bank is a token-efficient map of architecture, workflow, and tacit knowledge,
not a copy of the codebase:

```text
.agents/memory-bank/
├── INDEX.md
└── <cluster>/<topic>.md
```

Keep `AGENTS.md` as the entry point, `INDEX.md` as the navigation hub, and Level 2
topic files focused on one concern. Use four to eight concern clusters only when the
project needs that breadth. Prefer pointers for facts recoverable from the codebase in
three or fewer reads; reserve prose for human experience, external knowledge, and
non-obvious procedures.

Every `INDEX.md` topic needs a task-specific load trigger, for example “when debugging
board setup,” not “during any development.” Keep topic files roughly 50–300 lines and
split them when they exceed one concern or become too large. Do not put a constitution,
README, or maintenance templates at the memory-bank root.

For creation, ask the user for facts the repository cannot reveal before writing. For
updates, edit the relevant topic in place and update the index and `AGENTS.md` cluster
pointers when paths change. For maintenance-only requests, report stale pointers,
changed targets, orphan topics, ghost index entries, obsolete tacit knowledge, and
missing load triggers without modifying the bank.

## Safe Repair Procedure

1. Inventory the target files and read the repository's own guidance first.
2. Separate mechanically verifiable drift from policy, rationale, definitions, and
   tacit knowledge.
3. Repair broken paths, filenames, and command documentation only when the intended
   target is unambiguous.
4. Ask before changing accepted decisions, project rules, canonical definitions, or
   uncertain tacit knowledge.
5. Preserve existing formats and lifecycle metadata.
6. Re-scan every changed pointer, link, frontmatter block, command, and status field.
7. Record findings, changes, reasons, validation, skipped work, and blockers in the
   final report.

## When to Load This Document

Load this document when `harness-gardening` encounters `AGENTS.md`,
`CONSTITUTION.md`, `.agents/guidelines/`, `.github/guidelines/`,
`.agents/instructions/`, `.github/instructions/`, `.agents/adr/`, `.github/adr/`,
`.agents/glossary/`, `.agents/memory-bank/`, architecture pointers, ADR candidates
in git history, or a request to create, refresh, validate, or reconcile any of those
artifacts.
