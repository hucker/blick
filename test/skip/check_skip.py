"""DocString for check_dec"""
from src import blick

"""
Test that functions are skipped with the skip flag.
"""


@blick.attributes(skip=True)
def check_skip():
    """DocString for skip"""
    yield blick.BlickResult(status=True, msg="Result check_dec1")


@blick.attributes(skip=False)
def check_no_skip():
    """DocString for skip"""
    yield blick.BlickResult(status=True, msg="Result check_dec2")
