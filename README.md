# effectual

[![Python](https://img.shields.io/badge/Python-3776AB?logo=python&logoColor=fff)](#) [![MIT License](https://img.shields.io/badge/MIT%20License-FFFFFF)](#) [![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)

*/ɪˈfek.tʃu.əl/ meaning effective and successful*

## Why?

Sometimes you want a single portable Python executable file without having to make a platform specific executable (with tools such as [pyinstaller](https://pyinstaller.org/en/stable/) or [nuitka](https://nuitka.net/)) or a .pyz file without dependencies

## When not to use this

- The python package requires access to specific files like [CustomTkinter](https://github.com/TomSchimansky/CustomTkinter/wiki/Packaging#windows-pyinstaller-auto-py-to-exe) and [Pillow](https://python-pillow.org/)
- Incredibly version specific code, for example something that won't run on a slightly different python version or operating system
- The output bundle needs to include packages that aren't mostly written in python (such as packages written with [maturin](https://github.com/pyo3/maturin))

## Is this production ready

No

# Setup

## Template

If you want minimal setup then you can use the [effectual-template](https://github.com/effectualpy/effectual-template)

## DIY

First make sure you have [uv installed](https://docs.astral.sh/uv/getting-started/installation/#installation-methods) and [updated](https://docs.astral.sh/uv/getting-started/installation/#upgrading-uv):

    uv self update

Furthermore if you haven't already created a project run:

    uv init

Then to install effectual run:

    uv add effectual --dev

Finally add the following lines to your pyproject.toml

```TOML
[tool.effectual]

sourceDirectory = "./src/"
outputDirectory =  "./dist/"
outputFileName = "bundle.pyz"
minification = true
compressionLevel = 5
```

Note you must have a \_\_main\_\_.py entrypoint in the source directory for this to work

# Bundling

## Development

To bundle in dev mode use:

    uv run efec dev

This is like what [esBuild](https://esbuild.github.io/) does for Vite

## Production

To build a distributable .pyz file run:

    uv run efec dist

This is like what what [Rollup](https://rollupjs.org/) does for Vite

# Building from source

### Requirements

To build the project from source you need two tools:

1) [uv](https://docs.astral.sh/uv/#getting-started)
2) [justfile](https://just.systems/man/en/installation.html)

### Process

1) CD to the project directory and run:

        just setup


2) Then to build a distributable tar.gz and wheel:

        just build

You can also now use the included rust-just by prepending `uv run` e.g.

```
uv run just <command>
```

# Contributions

All contributions are welcome, if you utilise LLMs in your pull requests please specify and include its involvement
