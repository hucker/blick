"""Sample blick module with check functions"""

import time

from blick import BR
from src import blick


@blick.attributes(tag="tag1", ruid="m2_f1", level=1, phase="proto")
def check_module2_func1():
    "Another always passing function"
    time.sleep(.5)
    yield BR(status=True, msg="Always passes")


@blick.attributes(tag="tag2", ruid='m2_f2', level=2, phase="production")
def check_module2_func2():
    "THis thing always fails"
    time.sleep(.5)
    yield BR(status=False, msg="Always fails")


@blick.attributes(tag="tag2", ruid='m2_f3', level=2, phase="production")
def check_module2_func3():
    "This thing always warns"
    time.sleep(.5)
    yield BR(status=True, warn_msg="Always warns and passes")


@blick.attributes(tag="tag2", ruid='m2_f4', level=2, phase="production")
def check_module2_func4():
    "This thing always warns"
    time.sleep(.5)
    yield BR(status=False, warn_msg="Always warns and fails")
