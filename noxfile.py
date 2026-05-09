"""Nox configuration for django-improved-user."""

import nox
from nox import Session, options
from nox_uv import session

# Use uv as the default venv backend
options.default_venv_backend = "uv"

# Python versions supported by each Django version
DJANGO_PYTHON_VERSIONS = {
    "4.2": ["3.10", "3.11", "3.12"],
    "5.2": ["3.10", "3.11", "3.12", "3.13", "3.14"],
    "6.0": ["3.12", "3.13", "3.14"],
}

DJANGO_CONSTRAINTS = {
    "4.2": "Django>=4.2,<4.3",
    "5.2": "Django>=5.2,<6.0",
    "6.0": "Django>=6.0,<6.1",
}

# Build the full unit test matrix
UNIT_TEST_MATRIX = [
    (python, django)
    for django, pythons in DJANGO_PYTHON_VERSIONS.items()
    for python in pythons
]

# Example project test configurations
EXAMPLE_PROJECT_MATRIX = [
    ("3.12", "4.2"),
    ("3.14", "5.2"),
    ("3.14", "6.0"),
]


@session(python="3.12", uv_groups=["dev"])
def pkgcheck(session: Session) -> None:
    """Run check-sdist to verify package contents."""
    session.run("check-sdist")


@session(python="3.12", uv_groups=["docs"], uv_extras=["factory"])
def docs(session: Session) -> None:
    """Build documentation and check links."""
    with session.chdir("docs"):
        session.run(
            "sphinx-build",
            "-W",
            "-b",
            "html",
            "-d",
            f"{session.create_tmp()}/doctrees",
            ".",
            f"{session.create_tmp()}/html",
        )
        session.run(
            "python",
            "-msphinx",
            "-b",
            "linkcheck",
            ".",
            "build/linkcheck",
        )


@session(uv_groups=["dev"], uv_extras=["factory"])
@nox.parametrize("python,django", UNIT_TEST_MATRIX)
def unit(session: Session, django: str) -> None:
    """Run unit tests with coverage."""
    session.env["PYTHONDONTWRITEBYTECODE"] = "1"
    session.env["PYTHONWARNINGS"] = "once"
    session.install(DJANGO_CONSTRAINTS[django])
    session.run("coverage", "erase")
    session.run("coverage", "run", "runtests.py", *session.posargs)
    session.run("coverage", "combine", "--append")
    session.run("coverage", "report")


@session(uv_groups=["dev", "examples"], uv_extras=["factory"])
@nox.parametrize("python,django", EXAMPLE_PROJECT_MATRIX)
def extension(session: Session, django: str) -> None:
    """Run extension example project tests with coverage."""
    _run_example_project(session, "example_extension_project", django)


@session(uv_groups=["dev", "examples"], uv_extras=["factory"])
@nox.parametrize("python,django", EXAMPLE_PROJECT_MATRIX)
def replacement(session: Session, django: str) -> None:
    """Run replacement example project tests with coverage."""
    _run_example_project(session, "example_replacement_project", django)


def _run_example_project(
    session: Session,
    project: str,
    django: str,
) -> None:
    """Run example project tests with coverage."""
    session.env["PYTHONDONTWRITEBYTECODE"] = "1"
    session.env["PYTHONWARNINGS"] = "once"
    session.install(DJANGO_CONSTRAINTS[django])
    with session.chdir(project):
        session.run("coverage", "erase")
        session.run("coverage", "run", "manage.py", "test", *session.posargs)
        session.run("coverage", "combine", "--append")
        session.run("coverage", "report")
