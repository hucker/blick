import pytest

import blick
from blick import blick_exception
from blick import blick_result


# Define the fixture for the results
@pytest.fixture(scope="module")
def results():
    pkg = blick.BlickPackage(folder="./pkg_result")
    chk = blick.BlickChecker(packages=pkg, auto_setup=True)
    return chk.run_all()


def test_total_results(results):
    """ Test to verify the total results """
    assert len(results) == 7

    

def test_fail_only_filter(results):
    """ Test to verify the fail_only filter function """
    fail_only = [r for r in results if blick_result.fails_only(r)]
    assert len(fail_only) == 2


def test_pass_only_filter(results):
    """ Test to verify the pass_only filter function """
    pass_only = [r for r in results if blick_result.passes_only(r)]
    assert len(pass_only) == 5


def test_no_info_filter(results):
    """ Test to verify the remove_info filter function """
    no_info = [r for r in results if blick_result.remove_info(r)]
    assert len(no_info) == 6


def test_warn_is_fail_filter(results):
    """ Test to verify the warn_as_fail filter function """
    warn_is_fail = [r for r in results if blick_result.warn_as_fail(r)]
    assert len(warn_is_fail) == 7


def test_warning_messages(results):
    """ Test to verify the warning messages """
    wc = sum(1 for r in results if r.warn_msg)
    assert wc == 1


def test_info_messages(results):
    """ Test to verify the info messages """
    wc = sum(1 for r in results if r.info_msg)
    assert wc == 1


def test_group_by_tags(results):
    """ Test the group_by function with the 'tags' as the group key """
    grouped_results = blick_result.group_by(results, ['tag'])
    assert len(grouped_results) == 3
    assert len(grouped_results['tag1']) == 3
    assert grouped_results['tag1'][0].ruid == "pass11"
    assert len(grouped_results['tag2']) == 3
    assert grouped_results['tag2'][0].ruid == "skip_flag"
    assert len(grouped_results['tag3']) == 1
    assert grouped_results['tag3'][0].ruid == "blank_msg"


def test_group_by_tags_ruid(results):
    """ This shows that the recursion works with multi level grouping """
    grouped_results = blick_result.group_by(results, ['tag', 'ruid'])
    assert len(grouped_results) == 3
    assert len(grouped_results['tag1']) == 3
    assert len(grouped_results['tag1']['pass11']) == 1
    assert len(grouped_results['tag1']['fail12']) == 1
    assert len(grouped_results['tag1']['skip_none']) == 1
    assert len(grouped_results['tag2']['skip_flag']) == 1
    assert len(grouped_results['tag2']['warning']) == 1
    assert len(grouped_results['tag2']['info']) == 1
    assert len(grouped_results['tag3']['blank_msg']) == 1


def test_group_by_empty_key(results):
    """ This shows that the recursion works with multi level grouping """
    with pytest.raises(blick_exception.BlickException):
        _ = blick_result.group_by(results, [])


def test_group_by_ruids(results):
    """ Test the group_by function with the 'ruids' as the group key """
    r_grouped_results = blick_result.group_by(results, ['ruid'])
    assert len(r_grouped_results) == 7
