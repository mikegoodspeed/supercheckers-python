import invoke

PACKAGE = "supercheckers"


@invoke.task
def clean(ctx, all_=False):
    ctx.run("rm -rf .mypy_cache")
    ctx.run("rm -rf .pytest_cache")
    if all_:
        ctx.run(f"rm -rf {PACKAGE}.egg-info")


@invoke.task
def check(ctx):
    ctx.run(f"isort --check --diff -rc {PACKAGE} tests *.py", echo=True)
    ctx.run(f"black --check --diff -l 120 -t py37 {PACKAGE} tests *.py", echo=True)
    ctx.run(f"flake8 {PACKAGE} tests *.py", echo=True)
    ctx.run(f"mypy {PACKAGE} tests *.py", echo=True)


@invoke.task(name="format")
def format_(ctx):
    ctx.run(f"isort -rc --apply {PACKAGE} tests *.py", echo=True)
    ctx.run(f"black -l 120 -t py37 {PACKAGE} tests *.py", echo=True)


@invoke.task
def test(ctx):
    ctx.run("pytest")
