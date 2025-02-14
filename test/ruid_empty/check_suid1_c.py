from src import blick


def check_suid11_a():
    """No RUID"""
    yield blick.BlickResult(status=True, msg="No RUID")


def check_suid12_a():
    """No RUID"""
    yield blick.BlickResult(status=True, msg="No RUID")
