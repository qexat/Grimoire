"""
I don't know what I cooked here. But it doesn't taste very good.
"""

from __future__ import annotations

import collections.abc
import typing

T = typing.TypeVar("T")


class ListMeta(type):
    def __lshift__(self, other: typing.Any, /) -> typing.Any:
        return self(other)


class List(typing.Generic[T], metaclass=ListMeta):
    def __init__(self, *values: T) -> None:
        self.__data = list(values)

    def __repr__(self) -> str:
        return repr(self.data)

    def __iter__(self) -> collections.abc.Iterator[T]:
        return iter(self.data)

    def __next__(self) -> collections.abc.Iterator[T]:
        yield from self.data

    def __lshift__(self, value: T, /) -> typing.Self:
        res = typing.cast(typing.Self, List.copy(self))
        List.push(res, value)

        return res

    @property
    def data(self) -> list[T]:
        return self.__data.copy()

    @staticmethod
    def copy(list: List[T]) -> List[T]:
        return list.__class__(*list.__data)

    @staticmethod
    def push(list: List[T], value: T, /) -> None:
        list.__data.append(value)

    @staticmethod
    def pop(list: List[T]) -> T:
        return list.__data.pop()


lst = List << 3 << 5 << 2
List.push(lst, -1)

for i in lst:
    print(i)
