# gitlab-ci-optim.md — Prescriptive Guide for GitLab CI Pipeline Optimization

> This reference is part of the `harness-gardening` skill.
> Apply these rules when auditing or restructuring GitLab CI pipelines.

---

## Rule 1: One Target Per Job

**Every job `script:` block must call exactly one `just ci-*` target (1–2 lines max).**
Business logic belongs in the task runner, not in YAML.

Bad:
```yaml
build:
  script:
    - uv sync
    - uv build
    - uv run python scripts/verify.py
    - cyclonedx-py environment .venv -o sbom.json
```

Good:
```yaml
build:
  script:
    - just ci-build
```

**Why**: Jobs that contain inline shell logic cannot be reproduced locally without
reading the YAML. When a job fails, developers must be able to run `just ci-build`
locally to diagnose and fix the issue.

## Rule 2: Parallelization by Natural Dependency

**Split jobs along their natural dependency boundary. Jobs with no shared artifacts or
prerequisites must run in parallel in the same stage, not be sequenced.**

Use `needs:` to express the actual dependency graph. Avoid relying on stage ordering as
the only sequencing mechanism — `needs:` provides finer control and enables faster pipelines.

**DAG pattern**:
```
[check stage]
  check:python (parallel)
  build:frontend (parallel)

[test stage]
  test:e2e  → needs: [build:frontend]
  build:app → needs: [build:frontend]

[publish stage]
  pages → needs: [check:python, build:app, test:e2e]
```

## Rule 3: Artifact-Driven Flow

**Jobs that consume upstream output declare `needs:` to download artifacts; they never
re-run the same work.**

A job that rebuilds from scratch what another job already produced is:
- Wasting compute time
- Introducing non-determinism (different dependency versions)

Pattern: upstream jobs produce artifacts declared in `artifacts: paths:`. Downstream jobs
declare `needs: [upstream-job]` to automatically download them.

## Rule 4: Dual-Face Pages Pattern

**Any project with GitLab Pages needs two variants of the deploy job.**

```yaml
.pages-base:
  stage: publish
  needs: [check:python, build:app, test:e2e]
  script: just ci-pages

pages:dry-run:
  extends: .pages-base
  rules:
    - if: $CI_PIPELINE_SOURCE == "merge_request_event"
    - if: $CI_COMMIT_BRANCH && $CI_COMMIT_BRANCH != $CI_DEFAULT_BRANCH

pages:
  extends: .pages-base
  rules:
    - if: $CI_COMMIT_BRANCH == $CI_DEFAULT_BRANCH
    - if: $CI_COMMIT_TAG
```

- `pages` is the GitLab magic job name that triggers Pages deployment.
- `pages:dry-run` runs the same script but GitLab does not treat it as a deployment.
- Both use native `rules:` — no external framework dependency required.
- The shared `.pages-base` template prevents drift between the two variants.

## Rule 5: Allow-Failure Discipline

**Only flaky, proxy-dependent, or non-critical jobs use `allow_failure: true`.**
Blocking jobs (quality gates): `allow_failure: false` (default).
Non-blocking jobs (flaky tests, experimental checks): `allow_failure: true`.

**Never mark a hard quality gate `allow_failure: true`** — it nullifies the gate.
**Never mark all jobs `allow_failure: true`** — it means the pipeline gives no signal.

A job should be `allow_failure: true` if and only if:
1. It depends on external infrastructure that may be unavailable, or
2. It is in a trial/experimental period with known failure modes being addressed.

## Rule 6: No Monolith Jobs

**Any job exceeding 15 minutes is a monolith. Any job exceeding 12 minutes is a warning.**

Monolith symptoms:
- A single job that "does everything": lint + test + build + publish
- A job whose failure provides no signal about which concern failed
- A job that must be re-run entirely when only one step fails

Split strategy:
1. Identify natural dependency boundaries.
2. Extract the piece that can run independently into its own job.
3. Use `needs:` to express the actual dependency.
4. Aim for every job ≤ 12 minutes on a standard runner.

Target pipeline wall-clock time ≤ 20 minutes for a mid-size project.

## Anti-patterns

| Anti-pattern | Problem | Fix |
|---|---|---|
| Job with a long `script:` block | Cannot reproduce locally; hard to debug | Wrap in `just ci-*` target |
| All jobs run sequentially in one stage | Wall-clock equals the sum of all jobs | Add `needs:` to unlock parallelism |
| `allow_failure: true` on quality gates | CI becomes a rubber stamp | Remove it and fix the flakiness root cause |
| Re-running work from upstream jobs | Non-determinism and wasted compute | Use `needs:` plus artifact download |
| Single `pages` job with `only: [master]` | No dry-run validation on merge requests | Add `pages:dry-run` with merge-request rules |
| Monolith job > 15 min | Slow feedback; hard to split failures | Apply Rule 6 split strategy |
