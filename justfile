set minimum-version := '1.55.0'
set script-interpreter := ['uv', 'run', '--script']

[windows]
set shell := ["powershell.exe", "-NoLogo", "-Command"]

# Installs dependencies and creates venv
setup:
    uv python install 3.11
    uv venv --python 3.11 --clear
    uv lock
    uv sync
    just --list

# Bumps the versions of installed Python pacakges#
bump:
    uv lock --upgrade
    uv sync

# Formats Python source files
alias fmt := format
format:
    uv run ruff format --config pyproject.toml

[script]
pyproject:
    from pyproject_fmt import run
    exitCode = run(["./pyproject.toml"])

# Lints Python source files
lint:
    uv run ruff check --config pyproject.toml

# Type checks Python source files
alias ty := type
type:
    uv run ty check

# Type checks, Lints and Formats Python source files
check:
    just type
    just lint
    just format

# Runs tox which hence runs pytests
alias tox := test
test:
    uv run tox

# Builds distributable tar.gz and wheels after performing checks
build:
    just pyproject
    just check
    just test
    uv build

# Builds and then publishes artifacts to pypi
dist:
    just build
