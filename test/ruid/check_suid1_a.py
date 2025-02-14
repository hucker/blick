from src import blick


@blick.attributes(ruid="suid11")
def check_suid11_x():
    """Check RUID"""
    yield blick.BlickResult(status=True, msg="RUID 11")


@blick.attributes(ruid="suid12")
def check_suid12_x():
    """Check RUID"""
    yield blick.BlickResult(status=True, msg="RUID 12")
