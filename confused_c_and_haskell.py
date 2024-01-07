"""
I have no f*cking clue how we got from pointers (in Python??) to functional programming style stuff.

It is so unhinged that I decided to left it as is.
"""

from __future__ import annotations

import ctypes
from dataclasses import dataclass
from collections.abc import Callable, Iterable, Iterator, Sequence
import sys
from types import NoneType
from typing import (
    Any,
    Final,
    Generic,
    Literal,
    NewType,
    Self,
    TypeAlias,
    TypeVar,
    TypeVarTuple,
)


T = TypeVar("T")
U = TypeVar("U")
V = TypeVar("V")
W = TypeVar("W")
Ts = TypeVarTuple("Ts")
AddressT = TypeVar("AddressT", Literal[0], int)

NonEmptyTuple: TypeAlias = tuple[*tuple[*Ts]]


@dataclass(slots=True, repr=False)
class Pointer(Generic[T]):
    address: int | Literal[0]
    type: type[T]

    @classmethod
    def new(cls, value: T, /) -> Self:
        return cls(id(value), type(value))

    def __eq__(self, other: Any, /) -> bool:
        if isinstance(other, int):
            return self.address == other
        elif isinstance(other, Pointer):
            return self.address == other.address
        else:
            return False

    def __iter__(self) -> Iterator[T]:
        yield self.deref()

    def __ptr_repr__(self) -> str:
        return "·"

    def __repr__(self) -> str:
        type_name = self.type.__name__

        return f"({self.__ptr_repr__()} => <{type_name}> at {self.address:#016x})"

    def _get_pyobject(self) -> ctypes.py_object[T]:
        return ctypes.cast(self.address, ctypes.py_object)  # type: ignore

    def deref(self) -> T:
        if not self.address:
            raise ValueError("cannot dereference NULL pointer")

        return self._get_pyobject().value

    def mutate(self, new_value: T) -> None:
        self.address = id(new_value)

        ctypes.memmove(
            ctypes.pointer(self._get_pyobject()),
            ctypes.pointer(
                ctypes.cast(
                    id(new_value),
                    ctypes.py_object,  # type: ignore
                )
            ),
            1,
        )


@dataclass(slots=True, repr=False)
class FatPointer(Pointer[T]):
    capacity: int

    @classmethod
    def new(cls, *values: *NonEmptyTuple[*tuple[T, ...]]) -> Self:
        return cls(id(values[0]), type(values[0]), len(values))

    def __add__(self, offset: int) -> Self:
        if not 0 <= offset < self.capacity:
            raise ValueError(f"offset must be between 0 and {self.capacity}")

        return self.__class__(
            self.address + sys.getsizeof(self.deref()),
            self.type,
            self.capacity - 1,
        )

    def __ptr_repr__(self) -> str:
        return f"* [{self.capacity}]"


nullptr_t = NewType("nullptr_t", Pointer[None])
nullptr: Final = nullptr_t(Pointer(0, NoneType))

"""






"""


def bind(func1: Callable[[T], U], func2: Callable[[U], V]) -> Callable[[T], V]:
    return lambda arg: func2(func1(arg))


@dataclass
class bindable(Generic[T, U]):
    function: Callable[[T], U]

    def __rshift__(self, other: Callable[[U], V], /) -> bindable[T, V]:
        return bindable(bind(self, other))

    def __call__(self, __c: T | Any) -> U:
        return self.function(__c)


@bindable
def partmap(func: Callable[[T], U]) -> bindable[Iterable[T], map[U]]:
    return bindable(lambda p: map(func, p))


def bracket(
    func1: Callable[[T], U],
    func2: Callable[[V], W],
    arg1: T,
    arg2: V,
) -> tuple[U, W]:
    return func1(arg1), func2(arg2)


def expand(func: Callable[[*Ts], U], args: tuple[*Ts]) -> U:
    return func(*args)


def seq(subtype: type[T]) -> type[Sequence[T]]:
    return list[subtype]


print(
    expand(
        str.join,
        bracket(str, partmap(chr) >> seq(str), "", partmap(ord)("hello")),
    )
)
