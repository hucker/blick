"""Basic exception classes for blick."""


class BlickTypeError(TypeError):
    """Type errors associated with setting up Blick

    When bad types are sent to blick, this exception will be raised and should
    not be confused the TypeError that (should) indicate an unexpected lower
    level error.

    """


class BlickValueError(ValueError):
    """ Value Error associated with setting up Blick

    These exceptions will occur when setting up parameters on blick attributes and
    basic setup.  For example a negative weight.

    """


class BlickException(Exception):
    """Specialized exception for blick."""
