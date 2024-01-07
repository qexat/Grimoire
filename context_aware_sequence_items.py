"""
A sequence type where items are context-aware ; e.g. you can get the rest of
the sequence from a single element even if it was "isolated".
"""

from __future__ import annotations

import collections.abc
import functools
import typing


T = typing.TypeVar("T")


class SeqItem(typing.Generic[T]):
    def __init__(self, sequence: Seq[T], index: int, value: T, /) -> None:
        self.__sequence = sequence
        self.__index = index
        self.__value = value

    def __repr__(self) -> str:
        return repr(self.value)

    @functools.cached_property
    def value(self) -> T:
        return self.__value

    def previous(self) -> SeqItem[T]:
        return self.__sequence[self.__index - 1]

    def next(self) -> SeqItem[T]:
        return self.__sequence[self.__index + 1]

    def remaining(self) -> Seq[T]:
        return Seq(
            element.value
            for index, element in enumerate(self.__sequence)
            if index != self.__index
        )

    def __add__(self, other: typing.Any) -> typing.Any:
        if isinstance(other, SeqItem):
            return self.value + other.value  # type: ignore

        return self.value + other

    def __sub__(self, other: typing.Any) -> typing.Any:
        if isinstance(other, SeqItem):
            return self.value - other.value  # type: ignore

        return self.value - other

    def __mul__(self, other: typing.Any) -> typing.Any:
        if isinstance(other, SeqItem):
            return self.value * other.value  # type: ignore
        return self.value * other

    def __floordiv__(self, other: typing.Any) -> typing.Any:
        if isinstance(other, SeqItem):
            return self.value // other.value  # type: ignore
        return self.value // other

    def __truediv__(self, other: typing.Any) -> typing.Any:
        if isinstance(other, SeqItem):
            return self.value / other.value  # type: ignore
        return self.value / other

    def __mod__(self, other: typing.Any) -> typing.Any:
        if isinstance(other, SeqItem):
            return self.value % other.value  # type: ignore
        return self.value % other


class Seq(typing.Generic[T]):
    def __init__(self, __iterable: collections.abc.Iterable[T] | None = None) -> None:
        self._internal = [] if __iterable is None else list(__iterable)

    def __len__(self) -> int:
        return len(self._internal)

    def __iter__(self) -> collections.abc.Iterator[SeqItem[T]]:
        yield from (SeqItem(self, *pair) for pair in enumerate(self._internal))

    def __getitem__(self, index: int, /) -> SeqItem[T]:
        effective_index = index

        while abs(effective_index) >= len(self):
            effective_index += len(self) * -sign(effective_index)

        if effective_index < 0:
            effective_index = len(self) + effective_index

        return SeqItem(self, effective_index, self._internal[effective_index])

    def __repr__(self) -> str:
        return repr(self._internal)


def sign(value: int) -> typing.Literal[-1, 1]:
    if value < 0:
        return -1
    return 1


s = Seq(range(10))  # [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
v = s[3]  # 3
print(v.remaining())  # [0, 1, 2, 4, 5, 6, 7, 8, 9]
