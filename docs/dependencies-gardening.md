# `dependencies-gardening`: Validated Dependency Modernization

The `dependencies-gardening` skill helps GitHub Copilot modernize dependencies
across repositories while preserving project constraints and validating
compatibility. It is designed for repositories with multiple package managers,
nested applications, or dependency-owned configuration migrations.

## What it does

The skill reads the target project's `AGENTS.md`, conventions, task runners, CI,
and dependency tooling before changing anything. It discovers authoritative
manifests and lockfiles across the repository, including nested projects such as
frontends and extensions. It updates direct declarations, regenerates locks with
project-approved commands, and validates each update unit.

Small, mechanical compatibility changes and dependency-required configuration
migrations may be applied when focused checks prove they are safe. Declared lower
bounds are raised to the newest validated floor unless older support is
intentionally retained with evidence. Major releases are actively attempted in
isolation, including release-note review, lock regeneration, focused checks,
bounded compatibility edits, and the broad project gate. A major release is
retained when validated. Only a genuinely hard, unsafe, or untestable migration
is reverted in favor of the latest validated non-breaking release and returned
as actionable manual work. The skill leaves routine and non-breaking changes
uncommitted for review.

## Audit trail mode

Audit trail mode tracks validated dependency work in local Git commits so each
breaking migration can be reviewed or reverted independently. It is enabled when
the user explicitly requests commits or an audit trail, or when a breaking
dependency or dependency-required configuration migration needs source or
configuration changes.

The skill captures the starting commit, commits the validated safe baseline, and
keeps each breaking migration in its own local commit. It never pushes
automatically. The final report includes a proposed, not executed, local squash
command when the audit commit range can be verified safely.

## When to use it

Use it for explicit manual requests such as:

- “Update all dependencies safely, including nested projects.”
- “Find every authoritative dependency declaration in this monorepo, attempt
  major upgrades where allowed, and fall back only when migration is genuinely
  hard.”
- “Upgrade dependency X, make small compatibility fixes, and only report a
  substantial migration after attempting and validating the major release.”

## Boundaries

The skill updates package manifests, lockfiles, and project-declared runtime or
toolchain constraints. It preserves existing upper bounds and environment
markers. It does not add dependencies, remove supported runtimes, perform
unrelated refactors, edit generated or vendored files, commit by default, push,
schedule, or create merge requests.

It actively considers and attempts major releases when the project allows them.
Potential breaking changes trigger investigation and validation, not refusal. If
the migration is genuinely hard, it restores the attempt and tries the latest
validated non-breaking release. If no reliable validation gate exists, a clean
resolution is marked **unverified** rather than presented as proven
compatibility. When audit trail mode is enabled, it commits a validated safe
baseline and then places each breaking migration in its own isolated commit; it
never pushes automatically.

## Expected result

The final report identifies:

- every directly declared dependency, grouped by authoritative dependency
  surface, with declaration constraints, resolved versions, and an explicit
  status;
- authoritative dependency files and update units;
- retained updates with old/new declarations and resolved versions;
- source adaptations and validation evidence;
- major migrations attempted, retained, or reverted to a non-breaking fallback;
- skipped, reverted, blocked, and unverified updates; and
- official replacement dependencies and dependency-required configuration
  migrations;
- concrete next steps for migrations that are too risky to automate; and
- when audit trail mode is enabled, why it was enabled, a proposed (not
  executed) local squash command, and one user-impact-focused commit message
  covering retained and skipped work.
