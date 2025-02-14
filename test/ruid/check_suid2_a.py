from src import blick


@blick.attributes(ruid="suid21")
def check_suid11_x():
    """Check RUID"""
    yield blick.BlickResult(status=True, msg="RUID 21")


@blick.attributes(ruid="suid22")
def check_suid12_x():
    """Check RUID"""
    yield blick.BlickResult(status=True, msg="RUID 22")
