import click

@click.group()
def main():
    """Effectual CLI - A simple command-line interface."""
    pass

@click.command("dist")
def dist():
    """Bundles your source directory."""
    from . import build
    build.main()

@click.command("dev")
def dev():
    """Bundles your source directory."""
    from . import dev
    dev.main()

main.add_command(dist)

if __name__ == "__main__":
    main()