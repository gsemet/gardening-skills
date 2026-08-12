# Discovery and classification

Dependency gardening is only as reliable as its inventory. Build the inventory
from project evidence, not from a hardcoded list of languages or filenames.

## Evidence hierarchy

Use evidence in this order when deciding whether a candidate file is
authoritative:

1. Explicit project guidance in `AGENTS.md`, `CONSTITUTION.md`, accepted ADRs,
   contribution docs, and dependency-tool configuration.
2. Build, install, test, packaging, and release commands that consume the file.
3. Workspace, module, package, or project relationships declared by tooling.
4. Version-control and ownership conventions, including directory-level guides.
5. The file's syntax and naming, which are useful discovery signals but not
   proof of authority.

If evidence conflicts, preserve the file and report the conflict rather than
silently choosing a manifest. Accepted ADRs and explicit project rules override
inferred conventions.

## Candidate inventory

Search the whole repository for:

- package manifests and dependency declarations;
- lockfiles and resolver state;
- workspace or monorepo definitions;
- runtime, interpreter, compiler, SDK, and package-manager constraints;
- dependency configuration files and registry settings; and
- deprecated direct dependencies and their officially documented successor
   recommendations; and
- documented update, install, build, test, and preflight commands.

Also search nested application directories. A repository may contain a backend,
frontend, extension, plugin, examples, or tooling project with independent
manifests. Classify examples and fixtures as non-authoritative unless project
guidance says they are shipped or tested products.

For every candidate, record:

| Field | Meaning |
|---|---|
| Path | Repository-relative file path. |
| Owner | Root project, nested subproject, workspace, or shared owner. |
| Role | Declaration, lock, derived artifact, toolchain constraint, or unrelated config. |
| Dependency scope | Runtime, development, optional, documentation, test, or mixed. |
| Declared constraints | Lower and upper bounds, markers, exclusions, source, registry, and runtime/toolchain floors. |
| Relationships | Workspace, shared lock, generated-from, or consumed-by links. |
| Evidence | Guidance section, command, or build reference proving authority. |
| Update unit | The smallest group that must be changed and validated together. |
| Exclusions | Reason the file or dependency is not in scope. |

Do not edit until every in-scope update unit has an owner and evidence.

For each direct dependency, record the declared lower bound separately from
the resolved version. The lower bound is an explicit modernization candidate,
not merely a constraint to preserve. After validation, either raise it to the
newest supported floor or record why the project intentionally retains the
older floor. This prevents a lock-only update from being mistaken for a
complete dependency review.

## Authority signals

Treat a declaration as authoritative when project commands install, package,
build, or test from it, or when project guidance names it as the source of truth.
Treat a lockfile as authoritative when reproducible installation consumes it or
the project explicitly requires it to be committed. Treat a file as derived when
a documented generator recreates it from another source.

A dependency-owned configuration file is an authoritative migration surface when
the candidate release requires changes there. Examples include a linter
configuration format migration such as ESLint 9 flat config. Record the file,
the dependency version that requires it, and the focused command that validates
the migration.

When a direct dependency is deprecated, record the official successor, the
authoritative recommendation that supports the replacement, and whether the
old dependency can be removed in the same update unit. Do not classify an
official successor as unrelated dependency growth.

## Shared ownership

Create one update unit for declarations or locks shared by multiple components.
Examples include workspaces, a root lockfile resolving nested packages, generated
pinned extras, or a single manifest consumed by multiple build targets. Keep
independent subprojects separate only when their conventions permit independent
versions and validation.

## When to Load This Document

Load when identifying manifests, lockfiles, nested projects, workspace
relationships, generated files, or authoritative dependency declarations; when
`AGENTS.md` or project conventions determine dependency scope; or when the
repository uses more than one dependency surface.
