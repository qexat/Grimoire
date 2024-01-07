# ruff: noqa: E402

"""
Why using the wheel when you can make your own uglier, worse one?
"""

from __future__ import annotations

from grimutil import requires_package

requires_package("result")

import abc
import collections.abc
import typing

import result


P = typing.ParamSpec("P")
R = typing.TypeVar("R")
R_co = typing.TypeVar("R_co", covariant=True)


def safe_call(
    func: collections.abc.Callable[P, R],
    *args: P.args,
    **kwargs: P.kwargs,
) -> result.Result[R, Exception]:
    try:
        return result.Ok(func(*args, **kwargs))
    except Exception as e:
        return result.Err(e)


class TriFunction(typing.Protocol[P, R_co]):
    @abc.abstractmethod
    def __precall__(self, *args: P.args, **kwargs: P.kwargs) -> None:
        pass

    @abc.abstractmethod
    def __unsafe_call__(self, *args: P.args, **kwargs: P.kwargs) -> R_co:
        pass

    @abc.abstractmethod
    def __postcall__(self, exception: Exception | None) -> None:
        pass

    def __call__(self, *args: P.args, **kwargs: P.kwargs) -> R_co:
        def _call_wrap(_: None, /):
            return safe_call(self.__unsafe_call__, *args, **kwargs)

        e: Exception | None = None

        try:
            match safe_call(self.__precall__, *args, **kwargs).and_then(_call_wrap):
                case result.Ok(value):
                    return value
                case result.Err(e):
                    raise e
        finally:
            self.__postcall__(e)


def trifunc(
    precall: collections.abc.Callable[P, None],
    postcall: collections.abc.Callable[[Exception | None], None] | None = None,
) -> collections.abc.Callable[[collections.abc.Callable[P, R]], TriFunction[P, R]]:
    _postcall = postcall or (lambda e: None)

    def inner(func: collections.abc.Callable[P, R]) -> TriFunction[P, R]:
        # typing.Any because otherwise we get "R is already used in the outer scope"
        class _TriFunc(TriFunction[P, typing.Any]):
            def __precall__(self, *args: P.args, **kwargs: P.kwargs) -> None:
                precall(*args, **kwargs)

            def __unsafe_call__(self, *args: P.args, **kwargs: P.kwargs) -> R:
                return func(*args, **kwargs)

            def __postcall__(self, exception: Exception | None) -> None:
                _postcall(exception)

        return _TriFunc()

    return inner


def assert_uint(n: int) -> None:
    if n < 0:
        exc = TypeError("n must be greater or equal to 0")
        _offset = len(exc.__class__.__name__) + 2
        exc.add_note(" " * _offset + f"╰─ {n}")

        raise exc


@trifunc(assert_uint)
def fib(n: int) -> int:
    if n <= 1:
        return n
    return fib(n - 2) + fib(n - 1)


print(fib(-1))
