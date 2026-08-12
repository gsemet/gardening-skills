# Safety thresholds and rollback

Use this reference to decide whether to retain a dependency update, actively
attempt a major migration, apply small compatibility edits, or revert to the
latest validated non-breaking release.

## Safe update criteria

Retain an update when:

- the declaration remains within its original policy constraints;
- the resolver or package manager produces a reproducible result;
- focused checks covering the affected surface pass;
- the broad project gate passes, or the project has no such gate and the result
  is explicitly marked unverified; and
- no unexplained behavioral, API, packaging, or runtime change is observed.

## Major-version attempt policy

Treat the newest major release as a first-class migration candidate whenever it
is available within the preserved runtime, platform, source, and project-policy
constraints. Potential breaking changes, a major version number, or a migration
guide that lists possible work are reasons to investigate and test, not reasons
to refuse the attempt.

For each major candidate:

1. Capture the known-good declaration, lock state, and focused baseline.
2. Read available release notes, changelogs, migration guides, compatibility
   matrices, and the project's usage of the dependency.
3. Apply the candidate in isolation and regenerate the authoritative lock state.
4. Run focused checks before the broad project gate.
5. Resolve failures with small, mechanical, evidence-backed source or
   configuration edits, rerunning focused checks after each edit.
6. Run the broadest reliable project gate and retain the major release when the
   evidence passes.

When the candidate is retained, raise the declaration's lower bound to the newest
validated floor unless the project has evidence that older versions are still
intentionally supported. A lockfile-only result is incomplete when the manifest
floor can be tightened safely.

If authoritative dependency documentation recommends a successor for a deprecated
direct dependency, adding that successor and removing the old dependency is an
allowed replacement migration. Validate the replacement as a single unit; do not
reject it under the general prohibition on unrelated new dependencies.

Do not interpret the first compile, type, test, or build error as proof that a
major migration is too hard. Diagnose it first. Use isolation when several
updates interact and distinguish dependency regressions from baseline,
environment, and flaky failures.

### Genuinely hard migration boundary

Declare the major migration genuinely hard only when the evidence shows one or
more of the following:

- a broad architectural redesign or product-behavior decision is required;
- a data, schema, persistence, security-policy, or deployment migration is
  required;
- incompatible APIs affect many modules and replacements are unclear or
  semantically different;
- the candidate requires removing or widening a supported runtime or other
  preserved project constraint;
- required tooling, documentation, or compatibility evidence is unavailable and
  the project has no meaningful validation gate; or
- the candidate creates an unacceptable security, data-loss, packaging, or
  runtime risk that project checks cannot establish as safe.

The version being major is not itself a hard-migration signal. A small number of
mechanical call-site, import, option-name, or configuration adjustments remains
within scope when the replacement contract is clear and focused checks validate
the result. This includes dependency-required configuration migrations such as
converting an ESLint 8 configuration to the official ESLint 9 flat-config format,
provided the resulting lint gate passes.

### Fallback after an exhausted major attempt

Only after the hard-migration boundary is reached or compatibility remains
unverified after diagnosis:

1. Restore the major candidate's declaration, lock state, and source edits.
2. Select the newest available non-breaking release that preserves the original
   runtime, platform, upper-bound, marker, source, and policy constraints.
3. Validate that fallback with the same focused and broad gates.
4. Retain the fallback only when it is validated, or mark it **unverified** when
   the project has no reliable gate.
5. Report the attempted major version, evidence for abandonment, restoration
   status, fallback version, and remaining manual work.

Do not silently downgrade to an arbitrary older version. If no validated
non-breaking fallback exists, leave the unit reverted and report the unresolved
migration.

## Safe source adaptations

A source edit is eligible only when it is:

- directly caused by the retained dependency version;
- local, mechanical, and easy to review;
- limited in blast radius;
- covered by a focused check; and
- free of product or architectural decisions.

Examples include a verified import-path change, a renamed public symbol with a
clear replacement, or a mechanical option-name adjustment where the new contract
is established by project code or authoritative dependency documentation.

Do not automate a change when it requires redesigning control flow, changing
behavior, migrating persisted data, changing security policy, guessing a new API
contract, or touching many unrelated modules. During a major attempt, these
conditions exhaust the bounded adaptation path: revert the major update, try the
latest validated non-breaking fallback, and describe the required manual
migration.

## Failure classification

Classify failures before rollback:

- **Dependency-caused**: the failure appears only with the candidate and maps to
  a changed API, behavior, resolver constraint, or packaging contract.
- **Project-caused**: the candidate is not responsible; the baseline fails in the
  same way or the project already violates its own gate.
- **Environment-caused**: registry, network, proxy, credentials, missing tool,
  platform, or resource failure prevents a meaningful check.
- **Unknown**: evidence is insufficient or checks are flaky and causality cannot
  be established.

Retain an update only when compatibility is established despite a project or
environment issue. Revert changes with unknown compatibility. Do not claim that
a dependency caused a failure merely because it was the most recent change.

## Dichotomic isolation

Use bisection when a group of updates is reproducible, independently selectable,
and validated by a stable check:

1. Capture the known-good baseline and the full candidate group.
2. Split the candidate group into two coherent subsets.
3. Apply one subset while holding the other at baseline.
4. Run the smallest stable check that exposes the failure.
5. Keep the failing subset and restore the passing subset.
6. Repeat until the responsible package or interaction is isolated.

Fall back to one-package or one-change isolation when updates interact, a shared
lock resolves them together, the check is flaky, or the split changes the
conditions being tested. Do not use bisection to manufacture confidence.

## No-gate behavior

If no reliable validation gate exists, a clean declaration and lock update may be
attempted. Mark it **unverified**, avoid source adaptations, and state exactly
which evidence is missing. If a later check fails or cannot establish
compatibility, revert the affected unit and report it.

## Rollback contract

Rollback the smallest affected unit and restore both declarations and generated
lock state. Do not reset unrelated user work. Record:

- the attempted dependency and version;
- the update unit and files touched;
- the check and observed failure;
- the failure classification;
- the restoration status; and
- the manual migration path, if known.

Continue independent units after rollback. For a major candidate, rollback is not
complete until either the latest validated non-breaking fallback is retained or
the unit is restored to baseline and reported unresolved. Stop only when no safe
unit remains, the repository cannot be restored safely, or a project rule
explicitly requires manual intervention.

When audit trail mode is enabled, whether because the user explicitly requested
it or because a breaking dependency/configuration migration requires
source/configuration changes, commit validated safe changes before breaking
migrations, then commit each breaking dependency or configuration migration in
its own commit. Stage only the files in that update unit, record the activation
reason and commit identifiers in the report, and never push automatically.

## When to Load This Document

Load when judging whether a dependency update or source adaptation is safe; when
a compatibility check fails; when classifying a failure; when using dichotomic
isolation; or when deciding whether to revert and report a migration.
