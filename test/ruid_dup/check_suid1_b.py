from src import blick


@blick.attributes(ruid="suid11")
def check_suid11_d():
    """Check RUID"""
    yield blick.BlickResult(status=True, msg="RUID 11")


@blick.attributes(ruid="suid12")
def check_suid12_d():
    """Check RUID"""
    yield blick.BlickResult(status=True, msg="RUID 12")


#### DUPLICATE RUID IN THIS MODULE
@blick.attributes(ruid="suid12")
def check_suid13_d():
    """Check RUID"""
    yield blick.BlickResult(status=True, msg="RUID 12")


#### DUPLICATE RUID IN OTHER MODULE
def check_suid14_d():
    """Check RUID"""
    yield blick.BlickResult(status=True, msg="RUID 12")
