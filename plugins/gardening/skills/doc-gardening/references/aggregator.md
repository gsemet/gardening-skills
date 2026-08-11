# Aggregator Agent Contract

Produce one human-readable Markdown report from discovery, worker observations,
the evidence ledger, and execution statuses. Output only the report.

## Required inputs

- repository root and scan timestamp;
- selected current state, active configuration, and runtime assumptions;
- repository profile and governing guidance pointers;
- documentation accounting and generated-document provenance;
- evidence scopes and their intended coverage;
- worker observations and evidence records;
- worker, read, and scope statuses;
- unmatched paths, skipped paths, truncation, and limitations;
- mutation status, including whether any approved implementation phase was applied.

Do not treat a missing field as a clean result. If an input is absent, report the
aggregation limitation.

## Report structure

Use this structure, omitting empty detail sections but retaining meaningful
zero-result and limitation statements:

# Documentation Staleness Report

**Repository:** `{root}`  \
**Scanned:** `{timestamp}`  \
**Audit status:** `{complete | partial | failed}`  \
**Alignment verdict:** `{aligned | drift_found | partially_assessed | not_assessable}`  \
**Mutation status:** `{report_only | explicit_apply_phase_applied | not_applicable}`

## Summary

State what was inspected, the documentation coverage, the strongest evidence
discovered, the number of confirmed or probable findings, the alignment verdict,
and the main limitations in two to four concise sentences. Do not describe a
report-only audit as aligned when confirmed drift remains unapplied.

## Alignment verdict and coverage

Explain why the verdict was selected. Summarize:

- the number or set of documentation-like artifacts discovered;
- artifacts analyzed, not applicable, unsupported, or explicitly excluded;
- generated documentation whose provenance was verified or unavailable;
- code-verifiable claims assessed and any remaining unresolved claims;
- internal code conflicts that affect the judgment; and
- the current revision, configuration, and runtime assumptions.

## Repository profile

Summarize detected project types, documentation intents, evidence scopes, and
governing guidance. Link to repository-relative paths where useful.

## Confirmed findings

Group by severity, then document path and location. For each finding include:

- kind and confidence;
- documented claim or snippet;
- evidence path and location;
- explanation of the conflict;
- minimum proposed replacement, or `[NEEDS MANUAL REVIEW]`;
- limitations.

## Probable findings

List material concerns supported by incomplete or medium-confidence evidence.
Do not present these as confirmed drift.

## Coverage and unresolved references

Report expected coverage gaps only when document intent justifies them. List
unmatched claims, unresolved links, and references that could not be proven
removed separately.

## Skipped and incomplete analysis

Include unreadable, explicitly ignored, generated, vendor, unsupported,
truncated, timed-out, and failed areas with reasons. Distinguish deliberate
exclusions from execution failures. Do not hide an unaccounted documentation
artifact in this section; report it as a coverage limitation affecting the
alignment verdict.

## Recommended maintenance actions

Order actions by user impact and confidence. Do not edit files or imply that a
proposal was applied.

## Aggregation rules

- Report only observations supported by supplied evidence records.
- Preserve the distinction between confirmed, probable, unmatched, unsupported,
  and failed analysis.
- Sort confirmed findings by severity, document path, and location.
- Deduplicate by document location plus normalized claim, not symbol name alone.
- Merge duplicate observations while retaining distinct evidence and limitations.
- Do not manufacture file paths, symbols, signatures, versions, or replacements.
- Never convert an empty scope or failed worker into a ghost or removal finding.
- Never convert incomplete documentation accounting or incomplete code evidence
  into `aligned`.
- Treat current executable code as authoritative for implemented behavior;
  preserve internal code conflicts separately.
- Keep non-code claims qualified rather than silently marking them code-aligned.
- Include every discovered documentation artifact in the coverage statement or
  identify its explicit exclusion and reason.
- Generated documentation requires provenance or an explicit limitation.
- Escape or safely format repository-controlled text before placing it in the
  Markdown report.
- Include the overall status even when there are no findings.

## When to Load This Document

Load this document after discovery and analysis results are available, when
merging the evidence ledger, or when producing the final user-facing report.
