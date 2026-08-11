# Gardening Skills

`gardening` helps GitHub Copilot find documentation drift and agent-harness gaps
using evidence from a repository's files, commands, tests, and history.

The plugin is standalone and released under the MIT License.

## Installation

Install the `gardening` plugin from the GitHub Copilot plugin marketplace.

## Usage

Ask GitHub Copilot to audit a repository and include its path when it is not
obvious. For example:

- “Check whether the documentation in `docs/` is up to date with the source.”
- “Audit this repository’s agent harness and propose repairs.”
- “Find the most important documentation drift in this service.”

## Included Skills

| Skill | Purpose |
| --- | --- |
| `doc-gardening` | Shows where documentation no longer reflects the code, configuration, or public behavior, with evidence and proposed wording. |
| `harness-gardening` | Shows whether agent guidance, quality checks, decisions, vocabulary, and project memory still work together, then supports approved repairs. |

## Skill documentation

- [`doc-gardening`](docs/doc-gardening.md)
- [`harness-gardening`](docs/harness-gardening.md)

## Compatibility and Tool Boundaries

The skills use standard GitHub Copilot workspace capabilities. They are
model-neutral and do not require a specific task runner or external service.

## Mutation Safety

- `doc-gardening` is report-only and does not edit the audited repository.
- `harness-gardening` applies repairs only after the user approves their scope.
- Both skills record uncertainty instead of inventing evidence or rationale.

## Repository Layout

The installable plugin is under `plugins/gardening/`. Its two skills include
their own `SKILL.md` files and local references.

## Validation

The repository is dependency-free. Run:

- `just validate` — validate the plugin.
- `just preflight` — run the complete local quality gate.

GitHub Actions runs the same validator on pushes and pull requests.

## Release and Versioning

The plugin uses semantic versioning. Keep the version synchronized in the
marketplace and plugin manifests with `just version X.Y.Z`, then run
`just preflight` before publishing.

## Contributing

1. Keep skill names lowercase and hyphenated.
2. Keep frontmatter valid and free of private source metadata.
3. Keep mutation boundaries explicit and references local.
4. Run `just preflight` before opening a pull request.
