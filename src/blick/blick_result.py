""" This module contains the BlickResult class and some common result transformers. """

import itertools
import traceback
from collections import Counter
from dataclasses import asdict, dataclass, field
from functools import wraps
from operator import attrgetter
from typing import Any, Generator, Sequence

from .blick_exception import BlickException
from .blick_format import BlickMarkup


@dataclass
class BlickResult:
    """
    Return value of a BlickFunction.

    This dataclass tracks the status of a BlickFunction. It includes data relating to the function
    call, such as the status, module name, function name, message, additional info, warning message,
    docstring, runtime, exceptions, traceback, skip flag, tag, level, and count.

    This data can be used for reporting purposes.

    Attributes:
        status (bool): Check status. Default is False.
        module_name (str): Module name. Default is "".
        func_name (str): Function name. Default is "".
        msg (str): Message to the user. Default is "".
        info_msg (str): Additional function call info. Default is "".
        warn_msg (str): Warning message. Default is "".
        doc (str): Function docstring. Default is "".
        runtime_sec (float): Function runtime in seconds. Default is 0.0.
        except_ (Exception): Raised exception, if any. Default is None.
        traceback (str): Exception traceback, if any. Default is "".
        skipped (bool): Function skip flag. Default is False.
        tag (str): Function tag. Default is "".
        level (int): Function level. Default is 1.
        count (int): Return value count from a BlickFunction.
        """

    status: bool | None = False

    # Name hierarchy
    func_name: str = ""
    pkg_name: str = ""
    module_name: str = ""

    # Msg Hierarchy
    msg: str = ""
    info_msg: str = ""
    warn_msg: str = ""

    msg_rendered = ""

    # Function Info
    doc: str = ""

    # Timing Info
    runtime_sec: float = 0.0

    # Error Info
    except_: Exception | None = None
    traceback: str = ""
    skipped: bool = False

    weight: float = 100.0

    # Attribute Info - This needs to be factored out?
    tag: str = ""
    level: int = 1
    phase: str = ""
    count: int = 0
    ruid: str = ""
    ttl_minutes: float = 0.0

    # Mitigations
    mit_msg: str = ""
    owner_list: list[str] = field(default_factory=list)

    # Bad parameters
    skip_on_none: bool = False
    fail_on_none: bool = False

    # Indicate summary results, so they can be filtered
    summary_result: bool = False

    mu = BlickMarkup()

    def __post_init__(self):
        # Automatically grab the traceback for better debugging.
        if self.except_ is not None and not self.traceback:
            self.traceback = traceback.format_exc()

    def as_dict(self):
        """Convert the BlickResult instance to a dictionary."""
        d = asdict(self)
        d['except_'] = str(d['except_'])
        return d


# Shorthand
BR = BlickResult


class BlickYield:
    """
    This allows syntactic sugar to know how many times a generator
    has been fired and how many passes and fails have occurred.

    These internal counts allow top level code to NOT manage that
    state at the rule level.  Instead, you just report your passes

    and fails and ask at the end how it played out.

    gen = BrickYield()

    if cond:
        yield from gen(BR(True,"Info...")
    if not gen.yielded:
        yield from gen(BR(False,"Nothing to do"))
    if show_summary:
        yield SR(status=self.fail_count==0,msg=f"{self.pass_count} passes and {self.fail_count} fails")

    """

    def __init__(self, summary_only=False, summary_name=""):
        """
        The blick yield class allows you to use the yield mechanism while also tracking
        pass fail status of the generator.  Using this class allows for a separation of
        concerns so your top level code doesn't end up counting passes and fails.
        
        When your test is complete you can query the yield object and report that
        statistics without a bunch of overhead.
        
        If you set summary_only to true, no messages will be yielded, but you 
        can yield the summary message manually when you are done with the test.
        
        If you provide a name to this init then a generic summary message can be
        generated like this:
        
        y = BlickYield("Generic Test")
        y(status=True,msg="Test1")
        y(status=True,msg="Test2")
        y(status=False,msg="Test3")
        y.yield_summary()
        
        BR(status=False,msg="Generic Test had 2 pass and 1 fail results for 66.7%.")
        
        Args:
            summary_only(bool): Defaults to False
            summary_name: Defaults to ""
        """
        self._count = 0
        self._fail_count = 0
        self.summary_only = summary_only
        self.summary_name = summary_name

    @property
    def yielded(self):
        """ Have we yielded once?"""
        return self._count > 0

    @property
    def count(self):
        """How many times have we yielded?"""
        return self._count

    @property
    def fail_count(self):
        """How many fails have there been"""
        return self._fail_count

    @property
    def pass_count(self):
        """How many passes have there been"""
        return self.count - self._fail_count

    @property
    def counts(self):
        """Return pass/fail/total yield counts"""
        return self.pass_count, self.fail_count, self.count

    def increment_counter(self, result: BlickResult) -> None:
        self._count += 1
        if not result.status:
            self._fail_count += 1

    def results(self, results: BlickResult | list[BlickResult]) -> Generator[BlickResult, None, None]:
        """
        This lets you pass a result or results to be yielded and mimics the way blick results
        work in other places where traditional result collection is used, for example code
        that returns a list of BlickResults
        Args:
            results: one or list of blick results
        Returns:

        """
        if isinstance(results, BlickResult):
            results = [results]
               
        if isinstance(results,Generator) or (isinstance(results, list) and isinstance(results[0], BlickResult)):
            # At this point we are iterating over a list or a generator.
            for result in results:
                if isinstance(result, BlickResult):
                    self.increment_counter(result)
                    if not self.summary_only:
                        yield result
                else:
                    raise BlickException(f"Unknown result type {type(results)}")                        
        else:
            raise BlickException(f"Unknown result type {type(results)}")

    def __call__(self, *args_, **kwargs_) -> Generator[BlickResult, None, None]:
        """
        Syntactic sugar to make yielding look just like creating the SR object at each
        invocation of yield.  The code mimics creating a BlickResult manually
        since the *args/**kwargs are passed through via a functools.wrapper. 
        
        y.results(SR(status=True,msg="Did it work?"))
        
        The __call_ override allows the following code to work correctly without having to manually
        instantiate a BlickResult. 
        
        y(status=True,msg="Did it work?")
        
        Under the covers all the parameters to this function are forward to the creation of
        the underlying BlickResult inside the wrapper.
        
                
        Args:
            *args_: For BlickResult 
            **kwargs_: For BlickResult
        """

        @wraps(BlickResult.__init__)
        def sr_wrapper(*args, **kwargs):
            """
            Make the __call__ method have the same parameter list as the blickResult.__init__
            method.
            
            You can say:
            y(status=True,msg="Did it work?")
            
            or you can do
            
            y(SR(status=True,msg="Did it work?")
            
            Args:
                *args:   Handle any function args
                **kwargs: Handle any function kwargs

            Returns:

            """
            return BlickResult(*args, **kwargs)
        
        # If they just hand you a result then just pass it on
        if len(args_) == 1 and len(kwargs_) == 0 and isinstance(args_[0], BlickResult):
            results = [args_[0]]
            
        # This is when we get a generator
        elif len(args_) == 1 and len(kwargs_) == 0 and isinstance(args_[0], Generator):
                results = args_[0]
        else:
            # package up the result information
            results = [sr_wrapper(*args_, **kwargs_)]
        for result in results:
            self.increment_counter(result)
            if not self.summary_only:
                yield result

    def yield_summary(self, name="", msg="") -> Generator[BlickResult, None, None]:
        """
        The yield summary should be the name of the summary followed information message
        about the summary.  The message should give a pass and fail count.  If no name
        or message is provided the function name is used and a generic message is
        created. Generally the name should be provided since the function name is only
        good enough for very simple cases.  In general the message is good enough since
        it is nice to have all summaries look the same with the pass and fail count.
        
        Since this is yielding a summary the summary_result flag is set to enable filtering.
        Args:
            name: 
            msg: 

        Returns:

        """
        name = name or self.summary_name or self.__call__.__name__
        msg = msg or f"{name} had {self.pass_count} pass and {self.fail_count} fail."

        yield BlickResult(status=self.fail_count == 0, msg=msg, summary_result=True)


# Result transformers do one of three things, nothing and pass the result on, modify the result
# or return None to indicate that the result should be dropped.  What follows are some
# common result transformers.

def passes_only(sr: BlickResult):
    """ Return only results that have pass status"""
    return sr if sr.status else None


def fails_only(sr: BlickResult):
    """Filters out successful results.

    Args:
        sr (BlickResult): The result to check.

    Returns:
        BlickResult: The result if it has failed, otherwise None.
    """
    return None if sr.status else sr


def remove_info(sr: BlickResult):
    """Filter out messages tagged as informational

    Args:
        sr (BlickResult): The result to check.

    Returns:
        BlickResult: The result if it has failed, otherwise None.
    """
    return None if sr.info_msg else sr


def warn_as_fail(sr: BlickResult):
    """Treats results with a warning message as failures.

    Args:
        sr (BlickResult): The result to check.

    Returns:
        BlickResult: The result with its status set to False if there's a warning message.
    """
    if sr.warn_msg:
        sr.status = False
    return sr


def results_as_dict(results: list[BlickResult]):
    """Converts a list of BlickResult to a list of dictionaries.

    Args:
        results (list[BlickResult]): The list of results to convert.

    Returns:
        list[Dict]: The list of dictionaries.
    """
    return [result.as_dict() for result in results]


def group_by(results: Sequence[BlickResult], keys: Sequence[str]) -> dict[str, Any]:
    """
    Groups a list of BlickResult by a list of keys.

    This function allows for arbitrary grouping of BlickResult using the keys of the
    BlickResult as the grouping criteria.  You can group in any order or depth with
    any number of keys.

    Args:
        results (Sequence[BlickResult]): The list of results to group.
        keys (Sequence[str]): The list of keys to group by.S

    """

    if not keys:
        raise BlickException("Empty key list for grouping results.")

    key = keys[0]
    key_func = attrgetter(key)

    # I do not believe this is an actual test case as it would require a bug in
    # the code.  I'm leaving it here for now.
    # if not all(hasattr(x, key) for x in results):
    #    raise blick.BlickValueError(f"All objects must have an attribute '{key}'")

    # Sort and group by the first key
    results = sorted(results, key=key_func)
    group_results: list[tuple[str, Any]] = [(k, list(g)) for k, g in itertools.groupby(results, key=key_func)]

    # Recursively group by the remaining keys
    if len(keys) > 1:
        for i, (k, group) in enumerate(group_results):
            group_results[i] = (k, group_by(group, keys[1:]))

    return dict(group_results)


def overview(results: list[BlickResult]) -> str:
    """
    Returns an overview of the results.

    Args:
        results (list[BlickResult]): The list of results to summarize.

    Returns:
        str: A summary of the results.
    """

    result_counter = Counter(
        'skip' if result.skipped else
        'error' if result.except_ else
        'fail' if not result.status else
        'warn' if result.warn_msg else
        'pass'
        for result in results
    )

    total = len(results)
    passed = result_counter['pass']
    failed = result_counter['fail']
    errors = result_counter['error']
    skipped = result_counter['skip']
    warned = result_counter['warn']

    return f"Total: {total}, Passed: {passed}, Failed: {failed}, " \
           f"Errors: {errors}, Skipped: {skipped}, Warned: {warned}"
