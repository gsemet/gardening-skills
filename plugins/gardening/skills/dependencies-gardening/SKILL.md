---
name: dependencies-gardening
description: This skill should be used when a developer explicitly asks to update, upgrade, refresh, garden, or modernize dependencies across a repository, including nested subprojects, by attempting major upgrades, official successor replacements, dependency-required configuration migrations, and validated compatibility changes.
metadata:
  keywords: [dependencies, dependency-update, dependency-gardening, manifests, lockfiles, compatibility, rollback, migration-report, maintenance]
  recommended-models: [GPT-5.6 Luna (copilot)]
---

# Dependencies Gardening

## Modernization target

Optimize for the maximum practical dependency modernization, not merely for a
successful lockfile refresh or a patch/minor-only update. For every
authoritative dependency surface:

- target the newest release that can be validated in the project;
- raise each declared lower bound to the newest validated floor when older
  versions are no longer intentionally supported;
- replace a deprecated direct dependency with its officially recommended
  successor when the replacement is validated, even though that adds a new
  package declaration as part of removing the old one;
- migrate dependency-owned project configuration when the candidate requires
  it and the migration is reasonably local and testable, including a config
  migration such as ESLint 9's flat configuration; and
- actively attempt major-version migrations, including the small, local,
  mechanical source or configuration edits needed to complete a reasonable
  migration; and
- retain the modernized declaration and lock state when the focused and broad
  project checks pass.

Do not optimize for a zero-source-diff result. A major version, a migration
guide that lists breaking changes, or the first compiler/test/build failure is
not sufficient reason to fall back. Diagnose the failure and try the bounded,
evidence-backed compatibility edits before classifying the migration as hard.
Fall back only when the migration requires broad redesign, uncertain semantic
changes, or another condition in
`references/safety-thresholds.md` that makes it unreasonable to automate safely.

## Purpose and boundary

Perform one bounded, user-requested dependency-maintenance session using the
repository's own guidance, tooling, and quality gates. Discover the dependency
model before changing anything; do not assume a language, package manager,
manifest location, lockfile format, or task-runner command.

This skill complements automated update tools such as renovate and Dependabot.
Use those tools for scheduled, obvious, or merge-request-driven
updates. Use this skill when compatibility judgment, nested-project discovery,
or small source adaptations are needed.

Keep the work limited to:

- authoritative package-manager manifests and lockfiles;
- direct runtime, development, optional, and documentation dependencies;
- declared runtime and toolchain constraints that govern compatibility; and
- narrowly mechanical source changes required by an otherwise safe update.

Do not add unrelated dependencies, remove or widen supported runtime, platform,
upper bound, exclusion, source, or policy constraints, edit generated, vendor,
cache, or artifact files, perform unrelated refactors, redesign APIs, change
behavior or product policy, schedule work, commit by default, push, or create a
merge request. Audit trail mode is the explicit exception for validated local
commits.
An officially recommended replacement dependency is not an unrelated addition:
add it only as part of removing or migrating away from the deprecated direct
dependency, and retain the old package only when the project still uses it.
Dependency-owned configuration files are in scope when the migration requires
them; do not treat a configuration migration as an unrelated refactor.
Historical lower bounds are not automatically preserved: raise them when the
validated result establishes that the project no longer intends to support the
older floor.

## Operating contract

- Run once from discovery through validation and reporting, then stop.
- Do not pause for approval during execution. Attempt safe work autonomously.
- Revert an uncertain or risky update and record it in the final report while
  continuing independent safe updates.
- Treat an available major release as a migration to attempt, not a reason to
  skip. A potential breaking change requires investigation and validation; it
  is not by itself evidence that the migration is too difficult.
- Treat a small, local, mechanical, testable migration as part of the normal
  gardening scope, even when it changes source or configuration files. The
  objective is not to avoid code changes; it is to avoid broad or speculative
  migration work.
- When a direct dependency is deprecated in favor of an official successor,
  treat the successor replacement as an in-scope migration, not as forbidden
  dependency growth. Confirm the recommendation from authoritative dependency
  documentation and validate removal of the deprecated package.
- Preserve pre-existing user changes; never use a reset or cleanup operation
  that discards unrelated work.
- Leave validated routine and non-breaking changes uncommitted by default.
  Enable Git audit trail mode when the user explicitly requests commits or an
  audit trail, or automatically when a breaking dependency or
  dependency-required configuration migration needs source/configuration
  changes. A major version by itself does not activate the mode when no
  source or configuration change is needed. In audit trail mode, commit the
  validated safe baseline first, then commit each breaking dependency or
  configuration migration separately so every unit can be reverted
  independently. Never push automatically.
- When Git audit trail mode is enabled, capture the pre-run `HEAD` before the
  first audit commit. Use that SHA only to propose a final local squash of the
  commits created by this execution; never execute the squash automatically.
- Treat a clean package-manager resolution as evidence of solvability, not
  proof of runtime compatibility.

## Workflow

### 1. Read project authority

Start at the target repository root and identify the project harness: `AGENTS.md`,
`CONSTITUTION.md`, contribution guidance, accepted ADR frontmatter and relevant
bodies, memory-bank pointers, task-runner files, CI configuration, package
metadata, and dependency-tool documentation. Follow more-specific guidance in
nested subprojects. Record rules that affect dependency scope, supported
runtimes, lockfiles, validation, generated files, and commits.

Load `references/discovery-and-classification.md` before completing inventory.

### 2. Discover and classify dependency surfaces

Search the whole repository for candidate manifests, lockfiles, workspace files,
runtime/toolchain pins, package-manager configuration, and documented update or
validation targets. Use repository evidence to classify each candidate as:

- authoritative declaration;
- authoritative lock or resolver state;
- derived artifact to regenerate;
- generated, cached, vendored, or external material; or
- unrelated configuration that must remain untouched.

Do not infer authority from filename alone. Check ownership, build scripts,
workspace relationships, guidance, and whether the file is consumed by a build
or installation path. Detect nested applications such as frontends, extensions,
examples, or tools, but exclude them when project rules say they are samples or
generated outputs.

Build an inventory before editing. Include path, owner, dependency type,
relationship to other manifests or locks, project evidence, and intended update
unit. Coordinate shared declarations and shared locks as one unit unless the
project explicitly permits independent versions.

### 3. Determine candidate updates

Identify direct declarations and their current constraints. Record each
dependency's declared lower bound, upper bound, markers, exclusions, source
constraints, and resolved version separately. Preserve:

- upper bounds and exclusion clauses;
- environment, platform, and interpreter markers;
- supported runtime and toolchain versions;
- source, registry, repository, or digest constraints; and
- project-specific pins or accepted ADR decisions.

Target the newest available release compatible with those preserved constraints,
including the newest major release when the declared runtime and package
constraints allow it. Do not treat an existing lower bound as a permanent
constraint: compare it with the candidate and validated floor, then raise the
declarative lower bound when older versions are no longer intentionally
supported. If the older floor is intentionally retained, record the reason
instead of silently leaving the declaration unexplained. Never widen or remove
a genuine constraint just to make resolution succeed.

For every direct dependency, produce an explicit disposition: declaration and
lock updated, lock-only update with a documented reason, already current,
preserved by a genuine constraint, or attempted and reverted/blocked. A
successful resolver run does not satisfy this review by itself.

When a direct dependency is deprecated, inspect its official migration or
replacement guidance. Add the officially recommended successor and remove the
deprecated dependency in the same update unit when the project no longer needs
the old package. Validate the replacement as a dependency migration; do not
reject it merely because the package list contains a new name.

Do not retain a major candidate merely because resolution succeeds, and do not
reject it merely because documentation lists breaking changes. Continue through
the major migration loop: update, regenerate locks, run focused checks, apply
small mechanical compatibility edits when clearly justified, and run the broad
project gate. Retain the major release when that evidence passes. Fall back to
the latest validated non-breaking release only when the migration is genuinely
hard, unsafe, untestable, or otherwise outside the bounded adaptation rules in
`references/safety-thresholds.md`.

Never add an unrelated third-party dependency. A package that is only transitive
is updated through the normal resolver, not edited as a direct declaration.

The preceding rule does not prohibit an official successor replacement: that
case is explicitly governed by the replacement policy above.

### Git audit trail mode

Enable this mode in either of these cases:

- the user requests commits or an audit trail; or
- a breaking dependency or dependency-required configuration migration is
  being worked on and requires source/configuration changes.

Do not enable it merely because a candidate release is major if the migration
needs no source or configuration change. When the second case activates the
mode, do so before making the breaking source/configuration edit, without
pausing for approval, and state in the final report that the mode was enabled
automatically to preserve a reversible history.

Before the first edit belonging to an audited unit, capture the worktree and
identify unrelated pre-existing changes that must not enter the commits.
Record `audit_start_sha=$(git rev-parse HEAD)` before creating the first audit
commit. Inspect recent history and project guidance for the commit subject
format, body conventions, and required checks.

1. Validate the coherent non-breaking baseline, including safe lower-bound
   raises and official successor replacements that do not require a breaking
   migration.
2. Stage only the files belonging to that baseline and commit them with the
   project convention. Include authoritative manifests, regenerated locks, and
   validated local compatibility/configuration edits; exclude unrelated user
   changes and generated artifacts not owned by the update unit.
3. Starting from that baseline, attempt one breaking dependency or
   dependency-required configuration migration at a time. Keep each migration,
   its lockfile changes, source/config edits, and validation evidence in one
   isolated commit.
4. If a migration fails or reaches the hard boundary, restore that migration to
   the preceding commit without disturbing unrelated work, report the evidence,
   and continue with the next independent candidate.

Do not create a commit merely to hide an unresolved failure. If the worktree
cannot be isolated safely, leave the affected changes uncommitted and explain
the audit-trail limitation. Never amend, reset, force-push, or push during the
execution. At closeout, provide the squash proposal described in the reporting
section, but do not execute it unless the user explicitly requests that
separate operation.

### 4. Update one unit at a time

Before each update unit, capture the relevant declaration and lock state. Use
the project's prescribed package-manager and task-runner commands. Update
manifests through their native or project-approved mechanism and regenerate
lockfiles and other derived dependency artifacts only when project conventions
require it. Never hand-edit generated lock or report output.

For a major candidate, preserve a known-good baseline and work through the
candidate as an explicit migration attempt. Do not stop at the first compiler,
type-checker, test, or build error: classify it, apply a local mechanical fix
when eligible, and repeat the focused check. Bound the attempt by the safety
thresholds rather than by an arbitrary major-version rule.

When the candidate passes validation, update both the authoritative lock state
and the declaration floor. When only the lock can move because an older
declared floor remains intentionally supported, state that decision and its
evidence in the report.

Load `references/validation-and-artifacts.md` when choosing commands or handling
lockfiles and generated outputs.

Run the narrowest relevant check after a risky change. Then continue to the next
independent unit unless the change is blocked. Shared resolution or shared
artifacts make the affected components one unit.

### 5. Diagnose and isolate failures

Classify every failure as dependency-caused, project-caused,
environment-caused, or unknown. Do not call an unknown failure a regression.

Load `references/safety-thresholds.md` before applying compatibility edits or
isolating a failure. Use dichotomic isolation for reproducible groups of
updates. Fall back to one-package or one-change isolation when upgrades
interact, shared resolution obscures causality, or checks are flaky. Revert any
change whose compatibility remains unverified, then continue independent units.

If no reliable validation gate exists, a clean manifest/lock resolution may be
attempted with an explicit **unverified** status. This applies to major
candidates as well: do not claim runtime compatibility without project
evidence, and do not perform unsupported source adaptations. If the major
candidate cannot be meaningfully validated, restore it and try the latest
validated non-breaking candidate instead.

### 6. Adapt source code conservatively

Apply one or more source changes during a major migration only when every
change meets all of these conditions:

1. The dependency update is the clear cause of the compatibility issue.
2. The edit is local and mechanical, such as a verified import or API-name
   adjustment.
3. The blast radius is small and understood from the code and tests.
4. A focused project check can validate the edit.
5. The edit does not change product behavior or require design intent.

Do not automate broad API migrations, data migrations, rewrites, behavioral
changes, or compatibility work that requires guessing. For those cases, restore
the major candidate, try the latest validated non-breaking version, and report
the major attempt and the concrete blocker instead of pausing for approval.

### 7. Run the project quality gates

Infer the focused and broad validation commands from the project's guidance,
task runners, CI, package metadata, existing scripts, and recent conventions.
Run affected checks after each unit, then the broadest documented repository
gate before closeout. Avoid inventing a generic command when the project has no
reliable gate.

Classify network, registry, proxy, missing-tool, and flaky-test failures before
deciding whether to retain a change. Revert changes that remain unverified.

For a failed major attempt, distinguish a temporary environment or project
failure from a genuinely hard migration. Retry or isolate when project
conventions allow it. Only after the dependency-caused incompatibility is
established and the bounded adaptation path is exhausted may the major update
be reverted in favor of the latest validated non-breaking candidate.

### 8. Report and close out

Load `references/report-template.md` before composing the final report. Always
summarize in chat. Write a repository report only when requested or required by
project convention.

Include discovery evidence, authoritative files and update units, updated and
unchanged dependencies, reverted or blocked migrations, declaration and lock
versions, source adaptations, validation commands and results, uncertainty,
and concrete manual next steps. For every direct dependency, report whether its
declaration floor changed or stayed unchanged and why. For every major
candidate, report whether it was retained, reverted to a non-breaking fallback,
or left unverified, including the evidence that determined the outcome. Leave
validated changes uncommitted unless Git audit trail mode was enabled; this
includes both explicit and automatic activation. In audit trail mode, report
the activation reason, baseline commit, and each isolated migration commit or
rollback.

#### Audit-trail squash proposal

When Git audit trail mode was enabled, finish the report with a ready-to-paste
local squash proposal. Scope it to `audit_start_sha`, the SHA captured before
the first commit created by this execution, so pre-existing history and
unrelated work remain outside the operation. Verify that the commits from
`audit_start_sha..HEAD` are the linear audit commits from this execution before
printing the proposal. If the range contains an unrelated commit, a merge, or
cannot be verified safely, do not invent a command; report the boundary issue
and leave the commits isolated.

Print the following two-part proposal, replacing every placeholder with facts
from the final report:

```text
git reset --soft <audit-start-sha>
git commit -F- <<'EOF'
chore(deps): modernize validated dependencies

Retained: <user-impact summary of validated updates and migrations>
Skipped or deferred: <summary of skipped, blocked, reverted, or unverified work>
Validation: <actual broad-gate outcome and any remaining uncertainty>

Assisted-by: <PROVIDER>:<MODEL>
EOF
```

Keep the subject within the repository's Conventional Commit limit and keep
body lines within its wrapping limit. Summarize what users gain rather than
listing files or test counts. Include every skipped, blocked, reverted, or
unverified candidate in the second body line or a concise continuation. Use
exactly one `Assisted-by` trailer, resolved from the current session's provider
and model metadata, never from historical commits. Label the block clearly as
**proposed, not executed** and remind the user that `git reset --soft` rewrites
local branch history without pushing anything.

## Progressive disclosure references

Load the following documents when their trigger applies. The trigger text is
copied from each reference's mandatory `When to Load This Document` section.

- [`references/discovery-and-classification.md`](references/discovery-and-classification.md)
  — Load when identifying manifests, lockfiles, nested projects, workspace
  relationships, generated files, or authoritative dependency declarations;
  when `AGENTS.md` or project conventions determine dependency scope; or when
  the repository uses more than one dependency surface.
- [`references/safety-thresholds.md`](references/safety-thresholds.md)
  — Load when judging whether a dependency update or source adaptation is safe;
  when a compatibility check fails; when classifying a failure; when using
  dichotomic isolation; or when deciding whether to revert and report a
  migration.
- [`references/validation-and-artifacts.md`](references/validation-and-artifacts.md)
  — Load when discovering focused or broad quality gates; choosing project
  commands; regenerating lockfiles; handling generated dependency artifacts; or
  distinguishing environment failures from compatibility failures.
- [`references/report-template.md`](references/report-template.md)
  — Load when composing the final dependency-update report; when an update is
  skipped, reverted, blocked, or unverified; or when documenting manual
  migration steps and evidence.

No bundled executable script is required. Add one only after repeated,
validated use demonstrates deterministic work that is genuinely reusable across
projects.
