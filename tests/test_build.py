import subprocess

from effectual import bundleFiles


def test_bundle() -> None:
    """Checks bundle runs and outputs correct code"""
    assert bundleFiles("./tests/src", "./tests/out", "bundle.pyz", 5, True, False) is None
    runCommand = subprocess.run(
        "uv run ./tests/out/bundle.pyz", capture_output=True, text=True
    )
    assert runCommand.stdout.strip() == "Hello World\nHello from file2!"

if __name__ == "__main__":
    test_bundle()
