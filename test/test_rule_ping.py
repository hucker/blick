import pytest

import blick


# urls fixture that returns list of urls to check
@pytest.fixture
def urls():
    return ["www.google.com", "www.yahoo.com", "www.bing.com"]


@pytest.fixture
def bad_urls():
    return ["asdfaasf", "123", "", None, "bad.url.foo"]


def test_empty_rule_ping(urls):
    """ Verify url is tested fail"""

    @blick.attributes(tag="tag")
    def check_rule_ping_fail():
        yield from blick.rule_ping_check("", pass_on_none=False)
        yield from blick.rule_ping_check([], pass_on_none=False)

    for result in check_rule_ping_fail():
        assert not result.status


def test_empty_rule_ping_pass(urls):
    """ Verify empty url is tested pass """

    @blick.attributes(tag="tag")
    def check_rule_ping_pass():
        yield from blick.rule_ping_check("", pass_on_none=True)
        yield from blick.rule_ping_check([], pass_on_none=True)

    for result in check_rule_ping_pass():
        assert result.status


def test_skip_ping_true():
    @blick.attributes(tag="tag")
    def check_rule_ping_skip():
        yield from blick.rule_ping_check("", skip_on_none=True)        
        yield from blick.rule_ping_check([], skip_on_none=True)

    for result in check_rule_ping_skip():
        assert result.skipped


def test_skip_ping_false():
    @blick.attributes(tag="tag")
    def check_rule_ping_not_skipped():
        yield from blick.rule_ping_check("", skip_on_none=False)
        yield from blick.rule_ping_check([], skip_on_none=False)

    for result in check_rule_ping_not_skipped():
        assert not result.skipped


def test_rule_ping(urls):
    """ Verify single url is tested """

    @blick.attributes(tag="tag")
    def check_rule_ping():
        yield from blick.rule_ping_check(urls[0])

    for result in check_rule_ping():
        assert result.status


def test_rule_pings(urls):
    """ Verify list of urls is tested """

    @blick.attributes(tag="tag")
    def check_rule_pings():
        yield from blick.rule_ping_check(urls)

    for count, result in enumerate(check_rule_pings()):
        assert result.status

    # Make sure we ran all the tests
    assert count == len(urls) - 1


def test_nonexistent_host(bad_urls):
    """ Verify that a nonexistent URL fails appropriately """

    @blick.attributes(tag="tag")
    def check_nonexistent_url():
        yield from blick.rule_ping_check(bad_urls)

    for result in check_nonexistent_url():
        assert not result.status
