# Copyright (C) 2025 Ford Motor Company
# SPDX-License-Identifier: LicenseRef-Qt-Commercial OR GPL-3.0-only WITH Qt-GPL-exception-1.0
from __future__ import annotations

import gc
import sys
from functools import wraps


def _cleanup_local_variables(self, extra, debug):
    """
    Function to clean up local variables after a unit test.

    This method will set any local variables defined in the test run to None.  It also
    sets variables of self to None, if they are provided in the extra list.

    The self argument is passed by the decorator, so we can access the instance variables.
    """
    local_vars = self._locals
    if debug:
        print(f"  Cleaning up locals: {local_vars.keys()} and member of self: {extra}",
              file=sys.stderr)
    exclude_vars = {'__builtins__', 'self', 'args', 'kwargs'}
    for var in list(local_vars.keys()):
        if var not in exclude_vars:
            local_vars[var] = None
            if debug:
                print(f"  Set {var} to None", file=sys.stderr)
    # Remove variables added to 'self' during our test
    for var in list(vars(self).keys()):
        if var in extra:
            setattr(self, var, None)
            if debug:
                print(f"  Set self.{var} to None", file=sys.stderr)
    gc.collect()


# This leverages the tip from # https://stackoverflow.com/a/9187022/169296
# for capturing local variables using sys.setprofile and a tracer function
def wrap_tests_for_cleanup(extra: str | list[str] = None, debug: bool = False):
    """
    Method that returns a decorator for setting variables used in a test to
    None, thus allowing the garbage collection to clean up properly and ensure
    destruction behavior is correct.  Using a method to return the decorator
    allows us to pass extra arguments to the decorator, in this case for extra
    data members on `self` to set to None or whether to output additional debug
    logging.

    It simply returns the class decorator to be used.
    """
    def decorator(cls):
        """
        This is a class decorator that finds and wraps all test methods in a
        class.

        The provided extra is used to define a set() of variables that are set
        to None on `self` after the test method has run.  This is useful for
        making sure the local and self variables can be garbage collected.
        """
        _extra = set()
        if extra:
            if isinstance(extra, str):
                _extra.add(extra)
            else:
                _extra.update(extra)
        for name, attr in cls.__dict__.items():
            if name.startswith("test") and callable(attr):
                """
                Only wrap methods that start with 'test' and are callable.
                """
                def make_wrapper(method):
                    """
                    This is the actual wrapper that will be used to wrap the
                    test methods.  It will set a tracer function to capture the
                    local variables and then calls our cleanup function to set
                    the variables to None.
                    """
                    @wraps(method)
                    def wrapper(self, *args, **kwargs):
                        if debug:
                            print(f"wrap_tests_for_cleanup - calling {method.__name__}",
                                  file=sys.stderr)

                        def tracer(frame, event, arg):
                            if event == 'return':
                                self._locals = frame.f_locals.copy()

                        # tracer is activated on next call, return or exception
                        sys.setprofile(tracer)
                        try:
                            # trace the function call
                            return method(self, *args, **kwargs)
                        finally:
                            # disable tracer and replace with old one
                            sys.setprofile(None)
                            # call our cleanup function
                            _cleanup_local_variables(self, _extra, debug)
                            if debug:
                                print(f"wrap_tests_for_cleanup - done calling {method.__name__}",
                                      file=sys.stderr)
                    return wrapper
                setattr(cls, name, make_wrapper(attr))
        return cls
    return decorator


if __name__ == "__main__":
    # Set up example test class
    @wrap_tests_for_cleanup(extra="name", debug=True)
    class test:
        def __init__(self):
            self.name = "test"

        def testStuff(self):
            value = 42
            raise ValueError("Test")
            temp = 11  # noqa: F841
            return value

    t = test()
    try:
        t.testStuff()
    except ValueError:
        pass
    # Should print that `value` and `self.name` are set to None, even with the
    # exception being raised.
