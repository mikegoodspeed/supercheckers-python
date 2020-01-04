import invoke

PACKAGE = "supercheckers"
REQUIRED_COVERAGE = 50


@invoke.task
def clean(ctx, all_=False, n=False):
    """Clean unused files."""
    args = []
    if not all_:
        args.append(f"-e {PACKAGE}.egg-info")
    if n:
        args.append("-n")
    ctx.run("git clean -xfd -e .idea " + " ".join(args))


@invoke.task
def check(ctx):
    """Check for style and static typing errors."""
    ctx.run(f"flake8 {PACKAGE} tests *.py", echo=True)
    ctx.run(f"isort --check --diff -rc {PACKAGE} tests *.py", echo=True)
    ctx.run(f"black --check --diff -t py37 {PACKAGE} tests *.py", echo=True)
    ctx.run(f"mypy {PACKAGE} tests *.py", echo=True)


@invoke.task(name="format", aliases=["fmt"])
def format_(ctx):
    """Format code to adhere to best style guidelines."""
    af_args = (
        "--in-place --recursive "
        "--remove-all-unused-imports "
        "--ignore-init-module-imports "
        "--remove-duplicate-keys"
    )
    ctx.run(f"autoflake {af_args} {PACKAGE} tests *.py", echo=True)
    ctx.run(f"isort -rc --apply {PACKAGE} tests *.py", echo=True)
    ctx.run(f"black -t py37 {PACKAGE} tests *.py", echo=True)


@invoke.task
def test(ctx):
    """Run tests."""
    ctx.run(f"pytest --cov={PACKAGE} --cov-fail-under={REQUIRED_COVERAGE}", echo=True)


@invoke.task
def run(ctx):
    """Run the program."""
    ctx.run("supercheckers", pty=True, echo=True)


@invoke.task
def build(ctx):
    """Build a package."""
    ctx.run("python setup.py sdist bdist_wheel")
