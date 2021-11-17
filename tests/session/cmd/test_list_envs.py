from __future__ import annotations

import pytest

from tox.pytest import ToxProject, ToxProjectCreator


@pytest.fixture()
def project(tox_project: ToxProjectCreator) -> ToxProject:
    ini = """
    [tox]
    env_list=py32,py31,py
    [testenv]
    package = wheel
    wheel_build_env = pkg
    description = with {basepython}
    deps = pypy:
    [testenv:py]
    basepython=py32,py31
    [testenv:fix]
    description = fix it
    [testenv:pkg]
    """
    return tox_project({"tox.ini": ini})


def test_list_env(project: ToxProject) -> None:
    outcome = project.run("l")

    outcome.assert_success()
    expected = """
    default environments:
    py32 -> with py32
    py31 -> with py31
    py   -> with py32 py31

    additional environments:
    fix  -> fix it
    """
    outcome.assert_out_err(expected, "")


def test_list_env_default(project: ToxProject) -> None:
    outcome = project.run("l", "-d")

    outcome.assert_success()
    expected = """
    default environments:
    py32 -> with py32
    py31 -> with py31
    py   -> with py32 py31
    """
    outcome.assert_out_err(expected, "")


def test_list_env_quiet(project: ToxProject) -> None:
    outcome = project.run("l", "--no-desc")

    outcome.assert_success()
    expected = """
    py32
    py31
    py
    fix
    """
    outcome.assert_out_err(expected, "")


def test_list_env_quiet_default(project: ToxProject) -> None:
    outcome = project.run("l", "--no-desc", "-d")

    outcome.assert_success()
    expected = """
    py32
    py31
    py
    """
    outcome.assert_out_err(expected, "")
