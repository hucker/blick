import sys

import pytest

from src import blick


@pytest.fixture(scope="function")
def sys_path():
    """
    Prevent sys.path from being modified by tests.

    This is a case where you should @pytest.mark.usefixtures("sys_path")
    at the top of each function that can modify sys.path. This will ensure
    that sys.path is reset after each test and prevent warnings
    about sys_path not being used.
    """
    original_sys_path = sys.path.copy()
    yield
    sys.path = original_sys_path


@pytest.mark.usefixtures("sys_path")
def test_ruid1():
    """Normal case all RUIDS are unique"""
    pkg = blick.BlickPackage(folder="./ruid", name="ruid")

    ruids = pkg.ruids()

    assert ruids == ["suid11", "suid12", "suid21", "suid22"]
    assert blick.valid_ruids(ruids)
    assert blick.ruid_issues(ruids) == "No issues found."
    assert blick.package_ruids(pkg) == ["suid11", "suid12", "suid21", "suid22"]
    assert blick.module_ruids(pkg.modules[0]) == ["suid11", "suid12"]
    assert blick.module_ruids(pkg.modules[1]) == ["suid21", "suid22"]


def test_ruids1_module1():
    """Make sure we can load modules individually and extract the ruids"""
    module = blick.BlickModule(module_name="check_suid1_a", module_file='./ruid/check_suid1_a.py')
    assert module.module_name == "check_suid1_a"
    assert module.module_file == "./ruid/check_suid1_a.py"
    assert set(module.ruids()) == {"suid11", "suid12"}

    module = blick.BlickModule(module_name="check_suid2_a", module_file='./ruid/check_suid2_a.py')
    assert module.module_name == "check_suid2_a"
    assert module.module_file == "./ruid/check_suid2_a.py"
    assert set(module.ruids()) == {"suid21", "suid22"}


def test_ruids1_module2():
    """Make sure we can load modules individually and extract the ruids"""
    module = blick.BlickModule(module_name="check_suid1_a", module_file='./ruid/check_suid1_a.py')
    assert module.module_name == "check_suid1_a"
    assert module.module_file == "./ruid/check_suid1_a.py"
    assert set(module.ruids()) == {"suid11", "suid12"}

    module = blick.BlickModule(module_name="check_suid2_a", module_file='./ruid/check_suid2_a.py')
    assert module.module_name == "check_suid2_a"
    assert module.module_file == "./ruid/check_suid2_a.py"
    assert set(module.ruids()) == {"suid21", "suid22"}


@pytest.mark.usefixtures("sys_path")
def test_run_ruid_1():
    """Normal case all RUIDS are unique"""
    pkg = blick.BlickPackage(folder="./ruid", name="ruid")
    ch = blick.BlickChecker(packages=pkg, auto_setup=True)

    _ = ch.run_all()

    ruids = pkg.ruids()

    assert ruids == ["suid11", "suid12", "suid21", "suid22"]
    assert blick.valid_ruids(ruids)
    assert blick.ruid_issues(ruids) == "No issues found."


@pytest.mark.usefixtures("sys_path")
def test_run_package_in_list():
    """This is a check to verify that packages can be passed in a list"""
    pkg = blick.BlickPackage(folder="./ruid", name="ruid")
    ch = blick.BlickChecker(packages=[pkg], auto_setup=True)

    _ = ch.run_all()

    ruids = pkg.ruids()

    assert ruids == ["suid11", "suid12", "suid21", "suid22"]
    assert blick.valid_ruids(ruids)
    assert blick.ruid_issues(ruids) == "No issues found."


@pytest.mark.usefixtures("sys_path")
def test_ruid_dup():
    """Load up a package with duplicate RUIDS to verify exception"""
    with pytest.raises(blick.BlickException, match="Duplicate RUIDs found in module: suid12"):
        blick.BlickPackage(folder="./ruid_dup", name="ruid_dup")


@pytest.mark.usefixtures("sys_path")
def test_no_ruid():
    """Load a package that has no RUIDS"""
    pkg = blick.BlickPackage(folder="./ruid_empty", name="ruid_empty")

    ruids = pkg.ruids()

    # This package doesn't have RUIDS so all 4 should be empty
    assert ruids == ["", "", "", ""]

    # Now check
    assert pkg.name == 'ruid_empty'
    assert blick.empty_ruids(ruids) is True
    assert blick.valid_ruids(ruids) is False
    assert blick.ruid_issues(ruids) == "RUIDS are not used."


def test_missing_ruids():
    ruids = ["", "foo"]

    # Now check
    assert blick.empty_ruids(ruids) is False
    assert blick.valid_ruids(ruids) is False
    assert blick.ruid_issues(ruids) == "Blank RUIDs are present."
