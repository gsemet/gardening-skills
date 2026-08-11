# Evidence and Uncertainty Model

Use this model to keep repository facts, interpretations, and proposed wording
separate. The model applies across languages, formats, and analysis strategies.

## Evidence record

Each material observation should be represented by an evidence record containing:

- `evidence_id` — stable identifier within the audit;
- `path` — repository-relative source path;
- `location` — line, range, heading, key, symbol, or other locator;
- `type` — such as export, command, route, schema field, test, link, version,
  docstring, example, or prose claim;
- `value` — exact or normalized observed value;
- `authority` — `authoritative`, `supporting`, or `uncertain`;
- `extraction_method` — parser, tool, targeted text inspection, or heuristic;
- `confidence` — `high`, `medium`, or `low`;
- `limitations` — unresolved aliases, generated code, truncation, or ambiguity.

Never replace the exact observed value with an interpretation. Store both when
normalization is necessary.

## Evidence quality

Use the following confidence guidance:

- **High** — directly observed in an executable definition, schema, test,
  authoritative configuration, or unambiguous generated artifact with provenance.
- **Medium** — supported by multiple consistent references or a reliable parser,
  but affected by scope, aliasing, or incomplete context.
- **Low** — inferred from naming, proximity, regex, partial content, or a file
  whose authority is unknown.

Low-confidence evidence can guide further inspection, but should not independently
produce a high-severity finding.

## Authority and current state

The audit applies to the selected checkout and the active configuration and runtime
assumptions discovered for that checkout. Record the revision or branch when it is
available, along with configuration paths and assumptions that can change behavior.

For claims about implemented behavior, current executable code is the final source
of truth. Tests, schemas, configuration, generated artifacts, repository guidance,
and other documents are supporting evidence or explicit constraints. They may
explain a conflict, but must not silently override what the current implementation
does. When code paths disagree, preserve the conflict as an implementation
limitation instead of selecting an authority by convenience.

## Evidence status

Use explicit statuses for scopes, tasks, and documents:

- `complete` — the relevant evidence was inspected;
- `partial` — some evidence was inspected, but limitations may affect conclusions;
- `unmatched` — no reliable relationship between claim and evidence was found;
- `not_applicable` — the strategy does not fit the discovered scope;
- `unsupported` — the format or behavior could not be interpreted;
- `failed` — the worker or read operation failed;
- `ignored` — excluded by an explicit or evidence-backed exclusion rule.

Every discovered documentation-like artifact must have one of these handling
states: `analyze`, `not_applicable`, `unsupported`, or `explicitly_excluded`.
An explicit exclusion requires a reason. Generated documentation is not excluded
solely because it is generated; when it is user-facing, audit it through its
discovered provenance and report missing provenance.

## Claim classes

Classify material claims separately so that the alignment verdict does not pretend
that code can prove every kind of statement:

- `code_verifiable` — the current implementation can establish the behavior;
- `repository_supported_non_code` — the claim is supported by repository evidence
  but is not directly implemented behavior;
- `intentional_policy_or_design` — the claim expresses policy, design intent, or
  history rather than an executable fact;
- `unresolved` — the available evidence cannot establish the claim.

Only `code_verifiable` claims receive a direct code-alignment judgment. Keep the
other classes visible and qualified in the report.

## Absence is not removal

Classify a documented item as removed only when all of the following hold:

1. The item was matched to an applicable evidence scope.
2. The relevant source roots and generated-source rules were inspected.
3. The search completed without truncation or read failures.
4. Aliases, re-exports, dynamic registration, and alternate names were considered.
5. The item was not found in the repository-wide evidence index.

Otherwise use `unmatched`, `partial`, or `needs_manual_review`. Never convert an
empty or local-only snapshot into a removal finding.

## Finding severity

Assign severity based on user impact, not extraction convenience:

- **High** — following the documentation is likely to break execution, violate
  a required contract, select the wrong endpoint, or cause unsafe operation.
- **Medium** — the documentation is materially misleading or omits information
  needed for a common successful workflow, but immediate failure is unlikely.
- **Low** — wording, terminology, formatting, or minor precision issue with no
  meaningful change to the workflow.

Record confidence separately from severity. A high-impact claim supported only by
low-confidence evidence is a manual-review item, not a confirmed high finding.

## Scope and expected coverage

Use document intent to determine whether missing coverage is meaningful:

- API references can require broad public-surface coverage.
- Tutorials and READMEs should be checked for the symbols and workflows they use.
- Changelogs and migration guides should be checked for version and lifecycle
  claims.
- Runbooks should be checked against operational configuration and commands.
- Conceptual documents should be checked for claims and references, not every
  exported symbol.

## Repository-wide index

Build one index across all completed evidence scopes. Index normalized names,
aliases, paths, operations, commands, configuration keys, versions, and links.
Keep the original path and scope attached. Use scope-specific subsets for local
analysis, but use the global index when resolving cross-directory references or
testing whether a documented item was actually removed.

## Deduplication

Deduplicate by document location plus normalized claim, not by symbol name alone.
Two documents may legitimately contain different claims about the same symbol.
When merging observations, retain all distinct evidence paths and limitations.

## Alignment verdict

The alignment verdict is distinct from execution status and must be derived from
coverage as well as findings:

- `aligned` — every discovered documentation artifact is accounted for, all
  in-scope code-verifiable claims were assessed, no confirmed drift remains, and
  no unresolved high-impact code claim remains;
- `drift_found` — one or more confirmed code-verifiable documentation conflicts
  remain, whether or not the audit itself completed fully;
- `partially_assessed` — no confirmed drift was established, but documentation
  accounting, code evidence, or claim assessment is incomplete or materially
  uncertain;
- `not_assessable` — the audit could not establish enough implementation evidence
  or documentation scope to make a meaningful alignment judgment.

Do not infer `aligned` from an empty findings list. A report-only audit must not
claim `aligned` while confirmed drift remains unapplied. If an explicit approved
implementation phase later applies changes, the repository must be re-scanned
before the verdict can change.

## When to Load This Document

Load this document when reconciling worker results, deciding whether an absence is
meaningful, assigning confidence or severity, resolving cross-scope references,
or preparing the final report.
