# `doc-gardening`: Documentation Drift Analysis

The `doc-gardening` skill helps GitHub Copilot determine whether a repository's
documentation-like artifacts still match its current implementation. It produces
an evidence-based Markdown report with an explicit alignment verdict and proposed
wording for approved updates.

## What it provides

The skill is a **report-only documentation audit by default**. It accounts for
documentation-like artifacts discovered in the repository, including:

- READMEs, guides, and standalone documentation;
- inline comments, docstrings, and generated documentation;
- examples, notebooks, and runnable snippets;
- configuration and operational documentation; and
- other artifacts whose discovered intent is to communicate repository behavior.

The default read-only research subagent is the custom `Gardening Researcher`
agent, configured to run with `GPT 5.6 Luna (copilot)`.

The agent discovers the repository's formats, languages, tools, source roots,
documentation relationships, and suitable comparison strategies at runtime. It
compares documented claims with current executable code as the final authority,
while preserving non-code claims and conflicting supporting evidence as qualified
results rather than silently treating them as implementation facts.

## When to use it

Use it when you want to answer questions such as:

- “Is the documentation in this repository up to date?”
- “Find documentation drift between `docs/` and the source.”
- “Which public APIs are missing from the documentation?”
- “Propose updates, but do not edit the repository.”

It is most useful before a release, after a refactor, during documentation
maintenance, or when onboarding material and API references may have diverged.

## How it works

The skill is discovery-led rather than tied to a fixed language, directory layout,
or API model.

### 1. Discovery

A Discovery Agent first profiles the repository, reads applicable agent guidance,
records the selected checkout and active configuration, inventories source and
documentation-like artifacts, identifies code evidence and generated provenance,
and creates evidence scopes. A file can have multiple roles, such as source plus
inline documentation. Documentation is not limited to `docs/` directories, and
every discovered artifact is analyzed, classified, or explicitly excluded with a
reason.

### 2. Adaptive planning

Discovery recommends only the comparisons supported by the repository. Depending
on what it finds, the audit may compare public exports, docstrings, schemas,
OpenAPI operations, CLI commands, configuration, examples, links, versions, or
test-backed behavior. Unknown formats use a generic claim-and-reference fallback
and remain visible as limitations.

### 3. Evidence-led analysis

Analysis workers operate on evidence scopes rather than fixed directory zones.
They return structured observations, source locations, claim classes, confidence,
and limitations. A repository-wide evidence index resolves references across
directories and packages. Absence of local evidence is never treated as proof
that a symbol or feature was removed.

### 4. Aggregation

An Aggregator merges evidence and worker statuses into one report. It separates
confirmed findings, probable findings, unmatched claims, unsupported formats,
skipped paths, and failed or partial analysis, then returns an alignment verdict:
`aligned`, `drift_found`, `partially_assessed`, or `not_assessable`. The skill
never edits the audited repository during the audit phase.

## Report contents

A completed report can include:

- the selected revision, active configuration, and runtime assumptions;
- the alignment verdict and documentation coverage statement;
- a plain-English summary of documentation health;
- high-, medium-, and low-severity drift findings;
- the affected document and approximate location;
- the current documentation snippet;
- a suggested replacement or `[NEEDS MANUAL REVIEW]` marker;
- code-verifiable coverage gaps justified by document intent;
- generated-document provenance findings;
- non-code claims and internal implementation conflicts requiring qualification;
- skipped files and reasons when a file could not be read; and
- files that could not be verified because no matching symbol or API evidence was
  available.

The final report is only as reliable as the evidence available in the inspected
repository. Partial results are returned when one file, zone, or extractor fails.

## What it brings to the user

- **A focused maintenance queue:** drift is grouped by severity instead of being
  buried in a full repository diff.
- **Evidence for every proposed change:** the report preserves the documented
  snippet and explains what source evidence disagrees with it.
- **Coverage visibility:** justified coverage gaps and unresolved references
  reveal where documentation may have fallen behind repository evidence.
- **Safe reviewability:** proposed replacements are surfaced for a human to accept,
  reject, or rewrite.
- **Scalable analysis:** independent evidence scopes can be processed in parallel,
  while discovery avoids unnecessary work for small or documentation-only
  repositories.
- **Honest uncertainty:** unreadable, unverifiable, or failed areas are recorded
  rather than filled with guesses.

## Mutation boundary

`doc-gardening` does **not** edit the audited repository during its audit phase. It
discovers and verifies drift, then proposes aligned documentation changes in the
report. Applying those changes is a separate, explicitly approved implementation
phase followed by a re-scan. The report must not claim `aligned` while confirmed
drift remains unapplied.

## Error handling

The skill continues with partial evidence when possible:

| Situation | Result |
| --- | --- |
| A file cannot be read | Record it as unreadable and continue with partial status. |
| A worker returns no evidence | Preserve the task status; never fabricate a removal finding. |
| A document cannot be matched to evidence | Mark it unmatched or unverifiable with the reason. |
| An analysis worker times out | Record the failed task and continue with other tasks. |
| No documentation files exist | Return an explicit no-documentation result and do not claim `aligned` without stating the scope decision. |
| No validating implementation evidence exists | Run claim/reference checks and state that implementation drift could not be assessed. |

## In short

The `doc-gardening` skill is a read-only comparison between what a repository says
and what its evidence supports. It gives maintainers a prioritized, reviewable
staleness report without silently rewriting documentation or pretending that
uncertain findings are facts.
