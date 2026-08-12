# Dependency gardening report template

Use this structure for the final chat report or adapt it to a project-required
report file. Keep the report factual: distinguish updated, unverified, reverted,
and blocked work.

## Summary

- **Repository:** `<path>`
- **Requested scope:** `<user request>`
- **Result:** `<complete | partial | no safe updates>`
- **Commit status:** `<left uncommitted | audit commits created; squash proposal printed>`

State the number of update units discovered, attempted, retained, reverted, and
blocked. Mention whether a broad project gate passed, failed, or was unavailable.
Count major candidates separately and state how many were retained, reverted to a
non-breaking fallback, or left unverified.

If Git audit trail mode was enabled, identify whether it was explicitly requested
or automatically activated, then identify the safe-baseline commit and each
isolated breaking-migration commit or rollback. Confirm that unrelated pre-existing
changes were excluded and that nothing was pushed.

## Discovery inventory

| Update unit | Authoritative files | Dependency scope | Evidence | Shared state |
|---|---|---|---|---|
| `<unit>` | `<paths>` | `<runtime/dev/etc.>` | `<guidance or command>` | `<lock/workspace>` |

List candidates excluded from scope when the exclusion could surprise the user.

## Retained updates

| Dependency | Declaration before | Declaration after | Resolved version | Validation |
|---|---|---|---|---|
| `<name>` | `<old>` | `<new>` | `<version>` | `<checks>` |

Include source adaptations separately:

- `<file or symbol>`: `<mechanical change>` — validated by `<check>`.

Include official replacement dependencies separately when applicable:

- `<deprecated dependency>` → `<official successor>`: `<authoritative
\trecommendation>` — `<old declaration removed and replacement validated>`.

Include dependency-required configuration migrations separately when applicable:

- `<configuration file>`: `<migration required by dependency version>` —
  validated by `<focused check>`.

## Major migration attempts

List every attempted major candidate, including successful migrations and those
that fell back to a non-breaking release.

| Dependency | Attempted major | Evidence reviewed | Adaptations | Outcome | Validation |
|---|---|---|---|---|---|
| `<name>` | `<version>` | `<release notes and project usage>` | `<none or local edits>` | `<retained | fallback: version | unresolved>` | `<checks>` |

Do not classify a major candidate as refused solely because it may be breaking.
If it was reverted, state the concrete hard-migration signal or validation
evidence that exhausted the bounded attempt, then name the retained fallback.

## Unchanged or skipped updates

Record dependencies that were already current, had no compatible release, were
outside preserved constraints, or were excluded by project policy.

## Reverted or blocked migrations

| Dependency | Attempted version | Classification | Evidence | Rollback | Manual next step |
|---|---|---|---|---|---|
| `<name>` | `<version>` | `<type>` | `<failure or uncertainty>` | `<restored/not restored>` | `<action>` |

For a substantial breaking change, explain the affected API or behavior only as
far as the evidence supports. Do not invent migration details. If the next step
requires project-owner knowledge, say so explicitly. A potential breaking change
without failed validation or a hard-migration signal is not sufficient reason to
place an update here.

## Validation

List commands, working directories, and results:

- `<focused command>` — `<pass/fail/blocked>`
- `<broad gate>` — `<pass/fail/unavailable>`

Explain environment failures, flaky checks, baseline failures, and unknown causes
separately from dependency regressions.

## Audit-trail squash proposal

Include this section only when Git audit trail mode was enabled. State why it was
enabled, the `audit_start_sha` captured before the first audit commit, and confirm
that the range through `HEAD` contains only the linear commits created by this
execution. If it does, print a ready-to-paste proposal using:

```text
git reset --soft <audit-start-sha>
git commit -F- <<'EOF'
<conventional subject under the project limit>

Retained: <user-impact summary of completed work>
Skipped or deferred: <skipped, blocked, reverted, or unverified work>
Validation: <actual quality-gate outcome and remaining uncertainty>

Assisted-by: <PROVIDER>:<MODEL>
EOF
```

Replace all placeholders with facts from this run, keep exactly one `Assisted-by`
trailer from current session metadata, and label the proposal **not executed**.
If the range contains unrelated commits, a merge, or an uncertain boundary, omit
the command and explain why the commits remain isolated.

## Remaining uncertainty

State missing gates, unresolved shared-version interactions, unavailable registries,
unverified updates, and any recommended follow-up. A clean resolver result without
runtime checks must be labelled **unverified**.

## When to Load This Document

Load when composing the final dependency-update report; when an update is skipped,
reverted, blocked, or unverified; or when documenting manual migration steps and
evidence.
