# Update all plugin manifests to a semantic version.
version VERSION:
    uv run python3 scripts/set_version.py "{{VERSION}}"

# Validate the standalone plugin without installing dependencies.
validate:
    uv run python3 scripts/validate_plugin.py

# Run the complete local quality gate.
preflight: validate
