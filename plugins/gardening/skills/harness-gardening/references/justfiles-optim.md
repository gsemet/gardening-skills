# justfiles-optim.md — Prescriptive Guide for Task-Runner Organization

> This reference is part of the `harness-gardening` skill.
> Apply these rules when auditing or restructuring justfiles, Makefiles,
> Taskfiles, or any similar task runner used in an agentic project harness.

---

## Rule 1: One-Liner CI Targets

**Every CI job script must call exactly one `ci-*` target.** Logic belongs in the
justfile; YAML is declaration only.

Bad:
```yaml
script:
  - uv sync
  - pytest src --cov --junitxml=reports/unit-tests.xml
  - black --check src
  - flake8 src
```

Good:
```yaml
script:
  - just ci-check
```

**Why**: When a job fails, developers can reproduce it locally with `just ci-check`.
When it needs updating, the change lives in one place, not scattered across
pipeline YAML files.

## Rule 2: CI/Dev Separation

**CI targets (`ci-*`) call developer-facing targets. Developer targets never call CI targets.**

```
ci-check → checks → lint, sast, tests
ci-build → build, docs, sbom
```

**Never**:
```
tests → ci-check
build → ci-build
```

**Why**: CI targets are superset orchestrations. Developer targets are atomic units.
Reversing the dependency direction creates circular complexity and makes local
reproduction impossible.

## Rule 3: Group Annotations for Discoverability

**Annotate every target with `[group("name")]`.** Use consistent group names:
`base`, `dev`, `ci`, `style`, `check`, `test`, `demo`, `doc`.

Running `just --list` should immediately show developers all available targets
organized by purpose. New contributors and coding agents must be able to discover
the full surface area of the harness without reading documentation.

## Rule 4: Progressive Disclosure

**Each target must have a one-line description comment above it.**

```just
# Run all quality gates: lint, SAST, unit tests, performance
[group("ci")]
ci-check:
    just lint
    just sast
    just tests
    just test-performance
```

The description appears in `just --list` output. Targets without descriptions
are invisible to `just --list` and therefore invisible to agents and newcomers.

## Rule 5: Composability — Local Reproducibility Mandate

**Every `ci-*` target must be runnable on a developer workstation.**

A target that requires secrets, infrastructure, or network access not available
locally is not a CI target — it is a deployment script. Move deployment scripts
to a separate `deploy` or `release` group.

Test: if `just ci-X` cannot run on a fresh checkout (with environment set up),
it violates this rule.

## Rule 6: Remove Dead Targets

**Any target not called from CI or referenced in developer documentation must be deleted
or moved to `[group("experimental")]`.**

Dead targets create maintenance burden and mislead agents that discover them via
`just --list`. Before removing, check:
1. Is the target called from any CI job? (`grep -r "just <name>" .gitlab-ci.yml`)
2. Is the target referenced in `README.md`, `AGENTS.md`, or `CONTRIBUTING.md`?
3. Is the target called from another justfile target?

If none: delete it.

## Anti-patterns

| Anti-pattern | Problem | Fix |
|---|---|---|
| Monolith `ci-all` taking 30+ min | Untestable locally, long feedback loop | Split by concern into `ci-check`, `ci-build`, `ci-test-e2e`, etc. |
| Shell logic in YAML `script:` | Cannot reproduce locally | Move to a `ci-*` target |
| Targets with no description | Invisible to `just --list` | Add one-line comment |
| Developer targets calling `ci-*` | Circular dependency | Reverse — `ci-*` calls developer targets |
| Long chains of `&&` in YAML | Hard to debug which step failed | Use `just ci-*` target instead |
