"""
A funny way to have classes that act like singletons. Like `None`, they can
have only one instance.
"""

from __future__ import annotations

import os
import typing


_ALREADY_EXISTS = "cannot instantiate singleton class {!r}: the instance already exists"


class SingletonMeta(type):
    """
    Metaclass of which classes can only be instantiated once.

    The exception is raised at runtime ; it cannot be caught statically.
    """

    # Tracks whether an instance of SingletonMeta's classes exists or not
    _has_instance: dict[typing.Self, bool] = {}

    def _remove_destroyed_instance(self) -> None:
        self.__class__._has_instance[self] = False

    @staticmethod
    def _del_substitute(cls_inst: typing.Any) -> None:
        cls_inst.__class__._remove_destroyed_instance()

    def __new__(cls, *args: typing.Any, **kwargs: typing.Any) -> typing.Self:
        instance: typing.Self = typing.cast(
            typing.Self,
            super().__new__(cls, *args, **kwargs),
        )
        # adds the newly-created class in our tracking dict
        cls._has_instance[instance] = False
        setattr(instance, "__del__", cls._del_substitute)

        return instance

    #   __call__(self: SingletonMeta[Cls], *args, **kwargs) -> Cls
    def __call__(self, *args: typing.Any, **kwargs: typing.Any):
        if self.__class__._has_instance[self]:
            # instance already exists! we don't allow that :)
            raise TypeError(_ALREADY_EXISTS.format(self.__name__))

        # we create the instance BEFORE registering it: we have to be sure
        # that no exception was raised during the process
        instance = super().__call__(*args, **kwargs)

        self.__class__._has_instance[self] = True

        # send it back to the normal (sane) circuitry lol
        return instance


class MyClass(metaclass=SingletonMeta):
    def __init__(self, value: int) -> None:
        self.value = value

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(value: {self.value})"


def main() -> int:
    print(MyClass(-1))  # ok

    # the instance gets deleted (not guaranteed, though)

    inst1 = MyClass(3)  # ok (usually)
    print(inst1)

    inst2 = MyClass(5)  # error: TypeError: cannot instantiate singleton cl...
    print(inst2)

    return os.EX_OK


if __name__ == "__main__":
    raise SystemExit(main())
