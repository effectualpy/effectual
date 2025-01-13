# effectual

*/ɪˈfek.tʃu.əl/ meaning effective and successful*

## Why?

Sometimes you want a single portable python file without having to make a platform specific executable or a dependency-less .pyz! Basically me trying to make [Vite](https://vite.dev/) for python (badly) :(

## When not to use this

- The python package requires access to specific files like [CustomTkinter](https://github.com/TomSchimansky/CustomTkinter/wiki/Packaging#windows-pyinstaller-auto-py-to-exe) and [Pillow](https://python-pillow.org/)
- Incredibly version specific code, for example something that won't run on a slightly different python version or operating system

# Setup

First make sure you have [uv installed](https://docs.astral.sh/uv/getting-started/installation/#installation-methods) and updated:

    uv self update

Furthermore if you haven't already created a project run:

    uv init

Then to install effectual run:

    uv add effectual --dev

Finally add the following lines to your pyproject.toml and configure to your hearts desire

```TOML
[tool.effectual]

sourceDirectory = "./src/"
outputDirectory =  "./dist/"
outputFileName = "bundle.pyz"
minification = true
compressionLevel = 5
```

Note you must have a \_\_main\_\_.py entrypoint for this to work

## Template

If you want a simple minimal setup process then just use the [effectual-template](https://github.com/effectualpy/effectual-template)

# Bundling

## Development

To bundle in dev mode use:

    uv run efec dev

This is like what [esBuild](https://esbuild.github.io/) does for vite

## Production

To build a distributable .pyz file run:

    uv run efec dist

This is like what what [Rollup](https://rollupjs.org/) does for vite

# To be added

- [Treeshaking](https://webpack.js.org/guides/tree-shaking/)
- Rewriting some time critical parts in Rust 🚀🦀
- Cross platform compatibility (multiple output bundles)
- Bundle python version shebang and bytecode compilation
- Plugin and loader system (like rollup and webpack)

# Contributions

All contributions are welcome, I'm not the best in the world at project management but if you think you can add or improve anything please send over a pull request

## Building the project from source

### Requirements

To build the project from source you need two tools:

1) [uv](https://docs.astral.sh/uv/#getting-started)
2) [TaskFile](https://taskfile.dev/installation/)

### Process

1) CD to your effectual directory and run:

    task setup

2) Then to build an distributable tar.gz and wheel:

    task build