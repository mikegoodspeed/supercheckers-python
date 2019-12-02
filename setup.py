from pathlib import Path
from typing import Any, Dict

from setuptools import find_packages, setup

PACKAGE = "supercheckers"
HERE = Path(__file__).parent


def read(path: Path) -> str:
    with open(HERE / path) as f:
        return f.read()


meta: Dict[str, Any] = {}
exec(read(Path(PACKAGE) / "__meta__.py"), {}, meta)

setup(
    name=PACKAGE,
    description=meta["__description__"],
    long_description=read(Path("README.md")),
    long_description_content_type="text/markdown",
    author=meta["__author__"],
    version=meta["__version__"],
    packages=find_packages(exclude=["tests"]),
    package_data={"": ["LICENSE"]},
    entry_points={"console_scripts": [f"{PACKAGE} = {PACKAGE}.__main__:main"]},
    license=meta["__license__"],
)
