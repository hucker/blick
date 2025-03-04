import time

import pytest

import blick


@pytest.fixture(scope="module")
def check_func():
    def func(value):
        return value == 1

    return blick.BlickFunction(func)


def test__str__(check_func):
    str_value = str(check_func)
    assert check_func.function_name == 'func'
    assert str_value == "BlickFunction(self.function_name='func')"


@pytest.mark.parametrize("weight", [True, False, None])
def test_weight_none(weight):
    # Note this will fail if you say BlickException since weights
    with pytest.raises(blick.BlickException):
        @blick.attributes(weight=weight)
        def func():
            yield blick.BR(status=True, msg="Hello")


def test_weight_exception():
    @blick.attributes(tag="tag")
    def func():
        yield blick.BR(status=True, msg="Hello")

    func.weight = 0
    # Note this will fail if you say BlickException
    with pytest.raises(blick.BlickException):
        blick.BlickFunction(func)


def test_function_str():
    @blick.attributes(tag="tag")
    def func():
        yield blick.BR(status=True, msg="Hello")

    blick_func = blick.BlickFunction(func)
    assert blick_func.function_name == "func"


def test_func_doc_string_extract():
    @blick.attributes(tag="tag")
    def func():
        """This is a test function

        Mitigation:
        - Do something

        Owner:
        chuck@foobar.com

        Info:
        This is a
        long info string
        that needs

        help

        """
        return True

    s_func = blick.BlickFunction(func)
    for result in s_func():
        assert result.func_name == "func"
        assert result.status is True

        # NOTE: The inspect module, when used to get doc strings, will strip the leading
        #       white space from the doc string.  This is why the doc string is not
        #       indented and why you should use INSPECT.getdoc() to get the doc string.

        assert s_func._get_section("Mitigation") == "- Do something"
        assert s_func._get_section("Owner") == "chuck@foobar.com"
        assert s_func._get_section("DoesntExist") == ""

        assert (
                s_func._get_section("Info")
                == "This is a\nlong info string\nthat needs\n\nhelp"
        )
        assert s_func._get_section() == "This is a test function"


def test_function_bad_weight():
    def dummy_func():
        pass

    try:
        attribute_decorator = blick.attributes(tag="tag", phase="phase", level=1, weight=0, skip=False)
        attribute_decorator(dummy_func)
    except blick.BlickException:
        assert True

    except Exception:
        # The above cases don't work, even though the debugger says the exception is a BlickValueError
        # if I compare type(e) to BlickValueError it says False?
        assert False


def test_function_attributes():
    """Test arbitrary attributes"""

    @blick.attributes(tag="tag", phase="phase", level=1, weight=100, skip=False)
    def func():
        pass

    assert func.tag == "tag"
    assert func.phase == "phase"
    assert func.level == 1
    assert func.weight == 100
    assert func.skip is False


def test_def_function_attributes():
    """Check default tags"""

    @blick.attributes(tag="")
    def func():
        pass

    assert func.tag == ""
    assert func.phase == ""
    assert func.level == 1
    assert func.weight == 100
    assert func.skip is False


def test_basic_func_call():
    @blick.attributes(tag="Test")
    def func():
        """Test Function"""
        yield blick.BR(status=True, msg="It works")

    sfunc = blick.BlickFunction(func)

    for result in sfunc():
        assert result.func_name == "func"
        assert result.status is True
        assert result.msg == "It works"
        assert result.doc == "Test Function"
        assert result.skipped is False
        assert result.except_ is None
        assert result.warn_msg == ""
        assert result.info_msg == ""
        assert result.tag == "Test"


def test_basic_func_call_timing():
    @blick.attributes(tag="Timing")
    def func():
        """Test Timing Function"""
        time.sleep(1.1)
        yield blick.BR(status=True, msg="Timing works")

    sfunc1 = blick.BlickFunction(func)

    @blick.attributes(tag="Timing")
    def fast_func():
        """Test Timing Function"""
        time.sleep(0.1)
        yield blick.BR(status=True, msg="Timing works")

    sfunc2 = blick.BlickFunction(fast_func)

    result: blick.BlickResult = next(sfunc1())
    assert result.status is True
    assert result.skipped is False
    assert result.except_ is None
    assert result.runtime_sec > 1.0

    result: blick.BlickResult = next(sfunc2())
    assert result.status is True
    assert result.skipped is False
    assert result.except_ is None
    assert result.runtime_sec < 0.2


def test_info_warning_func_call():
    """Verify that warning message gets to result"""

    @blick.attributes(tag="InfoWarning")
    def func():
        """Test Complex Function"""
        yield blick.BR(status=True, msg="It still works", warn_msg="Warning")

    sfunc = blick.BlickFunction(func)

    result: blick.BlickResult = next(sfunc())
    assert result.func_name == "func"
    assert result.status is True
    assert result.skipped is False
    assert result.except_ is None
    assert result.warn_msg == "Warning"


def test_divide_by_zero():
    """Test exception handling data passes through to result and automatic tracebacks """

    @blick.attributes(tag="DivideByZero")
    def func():
        """Test Exception Function"""
        return 1 / 0

    sfunc = blick.BlickFunction(func)

    result: blick.BlickResult = next(sfunc())
    assert result.status is False
    assert result.msg == "Exception 'division by zero' occurred while running .func"
    assert result.doc == "Test Exception Function"
    assert result.skipped is False
    assert str(result.except_) == "division by zero"
    assert 'return 1 / 0' in result.traceback  # Might be python rev dependent, trying to be better not None
    assert result.tag == "DivideByZero"


def test_simplest_case_ever():
    """
    Test case where the users are the laziest possible people and use nothing in
    the system.
    """

    def return_only():
        return True

    def yield_only():
        yield True

    # The above function requires all default cases to work correctly
    s_func1 = blick.BlickFunction(return_only)
    s_func2 = blick.BlickFunction(yield_only)
    for s_func, name in ((s_func1, "return_only"), (s_func2, "yield_only")):
        for result in s_func():
            assert result.status is True
            assert result.func_name == name
            assert result.weight == 100
            assert result.count == 1
            assert result.ttl_minutes == 0
            assert result.level == 1
            assert result.module_name == ''
            assert result.pkg_name == ''
            assert result.owner_list == []
            assert result.skipped is False
            assert result.msg == f'Ran {name}.001 level=1'
