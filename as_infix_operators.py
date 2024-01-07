"""
"In Python, I wish I could use a function as an infix operator" — said nobody ever.

Anyway, you can do it now.
"""


from __future__ import annotations

import collections.abc
import dataclasses
import typing

T = typing.TypeVar("T")
U = typing.TypeVar("U")
Ret = typing.TypeVar("Ret")
HasLeft = typing.TypeVar(
    "HasLeft",
    typing.Literal[False],
    typing.Literal[True],
    covariant=True,
)
HasRight = typing.TypeVar(
    "HasRight",
    typing.Literal[False],
    typing.Literal[True],
    covariant=True,
)
BoolT = typing.TypeVar(
    "BoolT",
    typing.Literal[False],
    typing.Literal[True],
)


@dataclasses.dataclass(slots=True, frozen=True)
class _BinOp(typing.Generic[T, U, Ret, HasLeft, HasRight]):
    _function: collections.abc.Callable[
        [T], collections.abc.Callable[[U], Ret]
    ] | collections.abc.Callable[[U], Ret]
    _has_left: HasLeft = dataclasses.field(default=False)  # type: ignore
    _has_right: HasRight = dataclasses.field(default=False)  # type: ignore

    @property
    @typing.overload
    def function(  # type: ignore
        self: _BinOp[T, U, Ret, typing.Literal[False], typing.Literal[False]],
    ) -> collections.abc.Callable[[T], collections.abc.Callable[[U], Ret]]:
        pass

    @property
    @typing.overload
    def function(  # type: ignore
        self: _BinOp[T, U, Ret, typing.Literal[True], typing.Literal[False]],
    ) -> collections.abc.Callable[[U], Ret]:
        pass

    @property
    def function(
        self,
    ) -> (
        collections.abc.Callable[[T], collections.abc.Callable[[U], Ret]]
        | collections.abc.Callable[[U], Ret]
    ):
        return self._function

    @staticmethod
    def has_left(
        binop: _BinOp[T, U, Ret, HasLeft, BoolT],
    ) -> typing.TypeGuard[_BinOp[T, U, Ret, typing.Literal[True], BoolT]]:
        return binop._has_left

    @staticmethod
    def has_right(
        binop: _BinOp[T, U, Ret, BoolT, HasRight],
    ) -> typing.TypeGuard[_BinOp[T, U, Ret, BoolT, typing.Literal[True]]]:
        return binop._has_right

    @typing.overload
    def __rmatmul__(
        self: _BinOp[T, U, Ret, typing.Literal[False], typing.Literal[False]],
        left: T,
        /,
    ) -> _BinOp[T, U, Ret, typing.Literal[True], typing.Literal[False]]:
        pass

    @typing.overload
    def __rmatmul__(
        self: _BinOp[T, U, Ret, typing.Literal[False], typing.Literal[True]],
        left: T,
        /,
    ) -> Ret:
        pass

    def __rmatmul__(  # type: ignore
        self: _BinOp[T, U, Ret, typing.Literal[False], HasRight],
        left: T,
        /,
    ) -> Ret | _BinOp[T, U, Ret, typing.Literal[True], HasRight]:
        if _BinOp.has_right(self):
            return self.function(left)  # type: ignore

        def inner(right: U) -> Ret:
            return self.function(left)(right)  # type: ignore

        return _BinOp(inner, _has_left=True)

    @typing.overload
    def __matmul__(
        self: _BinOp[T, U, Ret, typing.Literal[False], typing.Literal[False]],
        right: U,
        /,
    ) -> _BinOp[T, U, Ret, typing.Literal[False], typing.Literal[True]]:
        pass

    @typing.overload
    def __matmul__(
        self: _BinOp[T, U, Ret, typing.Literal[True], typing.Literal[False]],
        right: U,
    ) -> Ret:
        pass

    def __matmul__(  # type: ignore
        self: _BinOp[T, U, Ret, HasLeft, typing.Literal[False]],
        right: U,
        /,
    ) -> Ret | _BinOp[T, U, Ret, HasLeft, typing.Literal[True]]:
        if _BinOp.has_left(self):
            return self.function(right)  # type: ignore

        def inner(left: U) -> Ret:
            return self.function(left)(right)  # type: ignore

        return _BinOp(inner, _has_right=True)


def binop(
    function: collections.abc.Callable[[T, U], Ret],
    /,
) -> _BinOp[T, U, Ret, typing.Literal[False], typing.Literal[False]]:
    return _BinOp(lambda left: (lambda right: function(left, right)))


@binop
def add(x: int, y: int) -> int:
    return x + y


x = 3 @ add @ 5
typing.reveal_type(x)  # Type of "x" is "int"
print(x)  # 8
