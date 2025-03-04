
from src import blick


def test_yielder_do_something():
    @blick.attributes(tag="tag", phase="phase", level=1, weight=100, skip=False)
    def func1():
        y = blick.BlickYield()
        for i in [1, 2, 3]:
            yield from y.results(blick.BlickResult(status=False, msg=f"Msg {i}"))
        if not y.yielded:
            yield from y.results(blick.BlickResult(status=True, msg="Nothing was to be done"))

    s_func = blick.BlickFunction(func1)

    ch = blick.BlickChecker(check_functions=[s_func], auto_setup=True)
    results = ch.run_all()

    assert len(results) == 3
    assert results[0].status is False
    assert results[0].msg == "Msg 1"
    assert results[1].status is False
    assert results[1].msg == "Msg 2"
    assert results[2].status is False
    assert results[2].msg == "Msg 3"


def test_result_yielder_counts():
    """
    This is tricky meta code.  The yield object is used to track how many passes
    and fails have been yielded because it is a common pattern to perform reporting
    based on all passes or all fails.  This test function runs through a simple
    scenario where it tests the counters in the yield object...and yields those
    results.

    """

    @blick.attributes(tag="tag", phase="phase", level=1, weight=100, skip=False)
    def func1():
        y = blick.BlickYield()
        yield from y.results(blick.BlickResult(status=False, msg="Here's a fail"))
        yield from y.results(blick.BlickResult(status=True, msg="Here's a pass"))
        yield from y.results(blick.BlickResult(y.fail_count == 1 and y.pass_count == 1 and y.count == 2,
                                                msg=f"Should be 1/1 counted {y.pass_count} pass and {y.fail_count} fail."))
        yield from y.results(blick.BlickResult(y.fail_count == 1 and y.pass_count == 2 and y.count == 3,
                                                msg=f"Should be 2/1 counted {y.pass_count} pass and {y.fail_count} fail."))
        yield from y.results(blick.BlickResult(status=False, msg="Here's another fail"))
        yield from y.results(blick.BlickResult(y.fail_count == 2 and y.pass_count == 3 and y.count == 5,
                                                msg=f"Should be 2/1 counted {y.pass_count} pass and {y.fail_count} fail."))
        p, f, t = y.counts
        yield from y.results(
            blick.BlickResult(status=all((f == 2, p == 4, t == 6)), msg=f"Counts check {p}==1 and {f}==1 and {t}==5"))

    s_func = blick.BlickFunction(func1)
    results = list(s_func())
    assert len(results) == 7
    assert results[0].status is False  # Hardcoded false
    assert results[1].status is True  # Hardcoded pass
    assert results[2].status is True  # verify counters
    assert results[3].status is True  # verify counters
    assert results[4].status is False  # verify y.counts
    assert results[5].status is True  # verify y.counts
    assert results[6].status is True  # verify y.counts

def test__call__yielder_counts():
    """
    This is tricky meta code again, only this test uses the __call__ method in
    the yielder class to clean up the syntax of yielding results

    """

    @blick.attributes(tag="tag", phase="phase", level=1, weight=100, skip=False)
    def func1():
        y = blick.BlickYield()
        yield from y(status=False, msg="Here's a fail")
        yield from y(status=True, msg="Here's a pass")
        yield from y(y.fail_count == 1 and y.pass_count == 1 and y.count == 2,
                                         msg=f"Should be 1/1 counted {y.pass_count} pass and {y.fail_count} fail.")
        yield from y(y.fail_count == 1 and y.pass_count == 2 and y.count == 3,
                                         msg=f"Should be 2/1 counted {y.pass_count} pass and {y.fail_count} fail.")
        yield from y(status=False, msg="Here's another fail")
        yield from y(y.fail_count == 2 and y.pass_count == 3 and y.count == 5,
                                         msg=f"Should be 2/1 counted {y.pass_count} pass and {y.fail_count} fail.")
        p, f, t = y.counts
        yield from y(status=all((f == 2, p == 4, t == 6)), msg=f"Counts check {p}==1 and {f}==1 and {t}==5")

    s_func = blick.BlickFunction(func1)
    results = list(s_func())
    assert len(results) == 7
    assert results[0].status is False  # Hardcoded false
    assert results[1].status is True  # Hardcoded pass
    assert results[2].status is True  # verify counters
    assert results[3].status is True  # verify counters
    assert results[4].status is False  # verify y.counts
    assert results[5].status is True  # verify y.counts
    assert results[6].status is True  # verify y.counts

def test_yielder_do_nothing():
    """Verify that you can check if anything has happened"""

    def false():
        return False

    @blick.attributes(tag="tag", phase="phase", level=1, weight=100, skip=False)
    def func():
        y = blick.BlickYield()
        if false():
            yield from y.results(blick.BlickResult(status=False, msg="Done"))
        if not y.yielded:
            yield from y.results(blick.BlickResult(status=True, msg="Nothing needed to be done."))

    s_func = blick.BlickFunction(func)

    ch = blick.BlickChecker(check_functions=[s_func], auto_setup=True)
    results = ch.run_all()

    assert len(results) == 1
    assert results[0].status is True
    assert results[0].msg == "Nothing needed to be done."

def test_yielder_exc():
    @blick.attributes(tag="tag", phase="phase", level=1, weight=100, skip=False)
    def should_pass_a_result_not_a_string():
        y = blick.BlickYield()
        yield from y.results("foo")

    s_func = blick.BlickFunction(should_pass_a_result_not_a_string)

    results = s_func()
    for result in results:
        assert result.status is False
        assert result.traceback
    
    
def test_yielder_result():
    @blick.attributes(tag="tag", phase="phase", level=1, weight=100, skip=False)
    def yield_a_result():
        y = blick.BlickYield()
        yield from y(blick.BR(status=True, msg="Yield result the 'normal' way."))

    s_func = blick.BlickFunction(yield_a_result)

    results = s_func()
    for result in results:
        assert result.status is True
        assert result.msg.startswith("Yield result the 'normal' way")
    
def test_yielder_summary():
    """
    This is tricky meta code again, only this test uses the __call__ method in
    the yielder class to clean up the syntax of yielding results
    
    Because the summary only flag is set, even though func1 has many tests that
    are verified and "yielded" this function only yields the summary result 
    rather than the 6 results.

    """

    @blick.attributes(tag="tag", phase="phase", level=1, weight=100, skip=False)
    def func1():
        y = blick.BlickYield(summary_only=True, summary_name="Func1 Summary")
        yield from y(status=False, msg="Here's a fail")
        yield from y(status=True, msg="Here's a pass")
        yield from y(y.fail_count == 1 and y.pass_count == 1 and y.count == 2,
                                         msg=f"Should be 1/1 counted {y.pass_count} pass and {y.fail_count} fail.")
        yield from y(y.fail_count == 1 and y.pass_count == 2 and y.count == 3,
                                         msg=f"Should be 2/1 counted {y.pass_count} pass and {y.fail_count} fail.")
        yield from y(status=False, msg="Here's another fail")
        yield from y(y.fail_count == 2 and y.pass_count == 3 and y.count == 5,
                                         msg=f"Should be 2/1 counted {y.pass_count} pass and {y.fail_count} fail.")
        p, f, t = y.counts
        yield from y(status=all((f == 2, p == 4, t == 6)), msg=f"Counts check {p}==1 and {f}==1 and {t}==5")
        yield from y.yield_summary()

    s_func = blick.BlickFunction(func1)
    results = list(s_func())
    assert len(results) == 1
    assert results[0].status is False
    assert results[0].msg == "Func1 Summary had 5 pass and 2 fail."
    assert results[0].summary_result is True
