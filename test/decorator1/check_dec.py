"""DocString for check_dec"""
from src import blick


@blick.attributes(tag='tag1', level=1)
def check_dec():
    """DocString for check_dec"""
    yield blick.BlickResult(status=True, msg="Result check_dec")
