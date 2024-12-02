import click


@click.group()
def main() -> None:
    pass


@click.command("dist")
def dist() -> None:
    """Bundles your source directory."""
    from . import build

    build.main()


@click.command("dev")
def dev() -> None:
    """Bundles your source directory."""
    from . import developer

    developer.main()


main.add_command(dist)
main.add_command(dev)

if __name__ == "__main__":
    main()
