from src import blick


@blick.attributes(ruid="suid21")
def check_suid21_d():
    """Check RUID"""
    yield blick.BlickResult(status=True, msg="RUID 21")


@blick.attributes(ruid="suid22")
def check_suid122_d():
    """Check RUID"""
    yield blick.BlickResult(status=True, msg="RUID 22")


@blick.attributes(ruid="suid22")
def check_suid23_d():
    """Check RUID"""
    yield blick.BlickResult(status=True, msg="RUID 23")
