"""DocString for check_simple1"""
from src import blick


def check_hello():
    """DocString for check_hello"""
    yield blick.BlickResult(status=True, msg="Result check_hello")
