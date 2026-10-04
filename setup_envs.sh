#!/usr/bin/env bash
# Creates the six pinned environments with uv. Fails loudly if any step fails.
set -euo pipefail
mkdir -p envs
mk() {
  uv venv -q --python 3.12 "envs/$1"
  uv pip install -q --python "envs/$1/bin/python" "$2"
  "envs/$1/bin/python" -c "import importlib.metadata as m, sys; print('$1 ->', m.version(sys.argv[1]))" "${2%%==*}"
}
mk pandas_old "pandas==2.3.3"
mk pandas_new "pandas==3.0.6"
mk pytest_old "pytest==8.4.2"
mk pytest_new "pytest==9.0.3"
mk django_old "django==5.2.17"
mk django_new "django==6.0.6"
