"""Nox configuration for django-improved-user."""

import nox

# Python versions supported by each Django version
DJANGO_PYTHON_VERSIONS = {
    "4.2": ["3.10", "3.11", "3.12"],
    "5.2": ["3.10", "3.11", "3.12", "3.13", "3.14"],
}

DJANGO_CONSTRAINTS = {
    "4.2": "Django>=4.2,<4.3",
    "5.2": "Django>=5.2,<6.0",
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
]


@nox.session(python="3.12")
def pkgcheck(session: nox.Session) -> None:
    """Run check-manifest to verify package contents."""
    session.install("-r", "requirements.txt")
    session.run("check-manifest", ".")


@nox.session(python="3.12")
def docs(session: nox.Session) -> None:
    """Build documentation and check links."""
    session.install("-r", "doc-requirements.txt")
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


@nox.session
@nox.parametrize("python,django", UNIT_TEST_MATRIX)
def unit(session: nox.Session, django: str) -> None:
    """Run unit tests with coverage."""
    session.env["PYTHONDONTWRITEBYTECODE"] = "1"
    session.env["PYTHONWARNINGS"] = "once"
    session.install("-r", "requirements.txt")
    session.install(DJANGO_CONSTRAINTS[django])
    session.install("-e", ".[factory]")
    session.run("coverage", "erase")
    session.run("coverage", "run", "runtests.py", *session.posargs)
    session.run("coverage", "combine", "--append")
    session.run("coverage", "report")


@nox.session
@nox.parametrize("python,django", EXAMPLE_PROJECT_MATRIX)
def extension(session: nox.Session, django: str) -> None:
    """Run extension example project tests with coverage."""
    _run_example_project(session, "example_extension_project", django)


@nox.session
@nox.parametrize("python,django", EXAMPLE_PROJECT_MATRIX)
def replacement(session: nox.Session, django: str) -> None:
    """Run replacement example project tests with coverage."""
    _run_example_project(session, "example_replacement_project", django)


def _run_example_project(
    session: nox.Session,
    project: str,
    django: str,
) -> None:
    """Run example project tests with coverage."""
    session.env["PYTHONDONTWRITEBYTECODE"] = "1"
    session.env["PYTHONWARNINGS"] = "once"
    session.install("-r", "requirements.txt")
    session.install("-r", f"{project}/requirements.txt")
    session.install(DJANGO_CONSTRAINTS[django])
    session.install("-e", ".[factory]")
    with session.chdir(project):
        session.run("coverage", "erase")
        session.run("coverage", "run", "manage.py", "test", *session.posargs)
        session.run("coverage", "combine", "--append")
        session.run("coverage", "report")
