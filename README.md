# effectual

*/ɪˈfek.tʃu.əl/ meaning effective and successful*

## Why?

Sometimes you want a single portable python file without having to make a platform specific executable or a dependency-less .pyz! Basically me trying to make [Vite](https://vite.dev/) for python (badly) :(

## When not to use this

- The python package requires access to specific files like [CustomTkinter](https://github.com/TomSchimansky/CustomTkinter/wiki/Packaging#windows-pyinstaller-auto-py-to-exe) and [Pillow](https://python-pillow.org/)
- Incredibly version specific code, for example something that won't run on a slightly different python version or operating system

# Setup

If you haven't already, run:

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
compressionLevel=5
```

Note you must have a \_\_main\_\_.py entrypoint for this to work

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
- Cross platform compatibility
- Plugin and loader system

# Contributions

All contributions are welcome, I'm not the best in the world at project management but if you think you can add or improve anything please send over a pull request
