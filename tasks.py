import invoke

PACKAGE = "supercheckers"


@invoke.task
def clean(ctx, all_=False):
    """Clean all unused files."""
    ctx.run("rm -rf .mypy_cache")
    ctx.run("rm -rf .pytest_cache")
    ctx.run("rm -rf build")
    ctx.run("rm -rf dist")
    if all_:
        ctx.run(f"rm -rf {PACKAGE}.egg-info")


@invoke.task
def check(ctx):
    """Check for style and static typing errors."""
    autoflake = "autoflake -r -c --remove-all-unused-imports --ignore-init-module-imports --remove-duplicate-keys"
    ctx.run(f"{autoflake} {PACKAGE} tests *.py", echo=True)
    ctx.run(f"flake8 {PACKAGE} tests *.py", echo=True)
    ctx.run(f"isort --check --diff -rc {PACKAGE} tests *.py", echo=True)
    ctx.run(f"black --check --diff -l 120 -t py37 {PACKAGE} tests *.py", echo=True)
    ctx.run(f"mypy {PACKAGE} tests *.py", echo=True)


@invoke.task(name="format")
def format_(ctx):
    """Format code to adhere to best style guidelines."""
    autoflake = "autoflake -r -i --remove-all-unused-imports --ignore-init-module-imports --remove-duplicate-keys"
    ctx.run(f"{autoflake} {PACKAGE} tests *.py", echo=True)
    ctx.run(f"isort -rc --apply {PACKAGE} tests *.py", echo=True)
    ctx.run(f"black -l 120 -t py37 {PACKAGE} tests *.py", echo=True)


@invoke.task
def test(ctx):
    """Run tests."""
    ctx.run("pytest", echo=True)


@invoke.task
def run(ctx):
    """Run the program."""
    ctx.run("supercheckers", pty=True, echo=True)


@invoke.task
def build(ctx):
    """Build a package."""
    ctx.run("python setup.py sdist bdist_wheel")
