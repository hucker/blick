import pytest

from src import blick


@pytest.fixture
def func1():
    @blick.attributes(tag="t1", level=1, phase='p1', ruid="ruid_1")
    def func1():
        yield blick.BlickResult(status=True, msg="It works1")

    return blick.BlickFunction(func1)


@pytest.fixture
def func2():
    @blick.attributes(tag="t2", level=2, phase='p2', ruid="ruid_2")
    def func2():
        yield blick.BlickResult(status=True, msg="It works2")

    return blick.BlickFunction(func2)


@pytest.fixture
def func3():
    @blick.attributes(tag="t3", level=3, phase='p3', ruid="ruid_3")
    def func3():
        yield blick.BlickResult(status=True, msg="It works3")

    return blick.BlickFunction(func3)


def test_nothing_rc_file(func1, func2, func3):
    ch = blick.BlickChecker(check_functions=[func1, func2, func3], auto_setup=True)
    assert ch.phases == ['p1', 'p2', 'p3']
    assert ch.tags == ['t1', 't2', 't3']
    assert ch.ruids == ['ruid_1', 'ruid_2', 'ruid_3']
    assert ch.levels == [1, 2, 3]

    # Same assertions since we are giving an RC file with nothing in it
    rc = blick.BlickRC()
    ch = blick.BlickChecker(check_functions=[func1, func2, func3], auto_setup=True, rc=rc)
    assert ch.phases == ['p1', 'p2', 'p3']
    assert ch.tags == ['t1', 't2', 't3']
    assert ch.ruids == ['ruid_1', 'ruid_2', 'ruid_3']
    assert ch.levels == [1, 2, 3]


def test_check_with_rc(func1, func2, func3):
    rc = blick.BlickRC(rc_d={'tags': 't1'})
    ch = blick.BlickChecker(check_functions=[func1, func2, func3], auto_setup=True, rc=rc)
    assert ch.tags == ['t1']

    rc = blick.BlickRC(rc_d={'phases': ['p1']})
    ch = blick.BlickChecker(check_functions=[func1, func2, func3], auto_setup=True, rc=rc)
    assert ch.phases == ['p1']

    rc = blick.BlickRC(rc_d={'ruids': ['ruid_1']})
    ch = blick.BlickChecker(check_functions=[func1, func2, func3], auto_setup=True, rc=rc)
    assert ch.ruids == ['ruid_1']

    # TODO Fix this.  Levels should be ints not string 
    #  of ints.
    # rc = splint.BlickRC(display_name='rc',levels=[1])
    # ch = splint.BlickChecker(check_functions=[func1, func2, func3], auto_setup=True,rc=rc)
    # assert ch.levels == ['1']


@pytest.mark.parametrize("rc_d, expected", [
    ({'ruids': ['r.*']}, 3),
    ({'ruids': ['.*1|.*2']}, 2),
    ({'phases': ['.*1|.*2']}, 2),
    ({'phases': ['p.*']}, 3),
    ({'tags': ['t.*']}, 3),
    ({'tags': ['.*1|.*2']}, 2),
    ({'levels': ['1|2|3']}, 3),
    ({'levels': ['1|3']}, 2),
    ({'levels': ['1'], 'tags': 't2', 'phases': 'p3'}, 0),
])
def test_simple_check_regex1(func1, func2, func3, rc_d, expected):
    """
    Verify that using a BlickRC 'file' is correctly applied using various regular
    expressions.
    """
    rc = blick.BlickRC(rc_d=rc_d)
    ch = blick.BlickChecker(check_functions=[func1, func2, func3], auto_setup=True, rc=rc)
    assert ch.function_count == expected
