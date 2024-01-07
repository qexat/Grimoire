"""
A very basic and unfinished ALU (Arithmetic and Logic Unit) accompanied by
a simple and stupid tester because I was too lazy to set up a venv + pytest. 
"""

import collections.abc
import dataclasses
import operator
import os
import shutil
import sys
import typing

from grimutil.types import MAX_I8, MIN_I8, i8, is_i8, u8


class ALU:
    __slots__ = ("a", "b", "y", "op", "negative", "carry", "overflow")

    def __init__(self) -> None:
        self.a: i8 = 0  # left operand
        self.b: i8 = 0  # right operand
        self.y: i8 = 0  # result
        self.op: u8 = 0  # opcode
        self.negative: bool = False
        self.carry: bool = False
        self.overflow: bool = False

    @property
    def zero(self) -> bool:
        return self.y == 0

    @staticmethod
    def does_carry(n: int) -> bool:
        return -0xFF <= n < MIN_I8 or MAX_I8 < n <= 0xFF

    @staticmethod
    def does_overflow(n: int) -> bool:
        return not ALU.does_carry(n) and not is_i8(n)

    def add(self) -> None:
        res = self.a + self.b

        self.negative = res < 0
        self.carry = self.does_carry(res)
        self.overflow = self.does_overflow(res)

        self.y = typing.cast(i8, (res & MAX_I8) - (0x80 * self.negative))


class CPU:
    pass


# *- The following code is ugly but it's not meant to be pretty -* #

BinaryComparison: typing.TypeAlias = collections.abc.Callable[[object, object], bool]


@dataclasses.dataclass(slots=True, frozen=True)
class AssertTest:
    lname: str
    rname: str
    lvalue: object
    rvalue: object
    comparison: BinaryComparison = dataclasses.field(default=operator.eq)

    def run(self) -> bool:
        return self.comparison(self.lvalue, self.rvalue)

    def __repr__(self) -> str:
        _comp_name = (
            "==" if self.comparison == operator.eq else self.comparison.__name__
        )

        return f"{self.lname} \x1b[34m{_comp_name}\x1b[39m {self.rname}"

    def repr_left(self) -> str:
        return f"{self.lname} = {self.lvalue}"

    def repr_right(self) -> str:
        return f"{self.rname} = {self.rvalue}"


def test_alu_add(
    name: str,
    a: i8,
    b: i8,
    y: i8,
    negative: bool,
    carry: bool,
    overflow: bool,
) -> int:
    alu = ALU()

    alu.a = a
    alu.b = b

    alu.add()

    return test_suite(
        name,
        AssertTest("alu.y", "y", alu.y, y),
        AssertTest("alu.negative", "negative", alu.negative, negative),
        AssertTest("alu.carry", "carry", alu.carry, carry),
        AssertTest("alu.overflow", "overflow", alu.overflow, overflow),
    )


def test_suite(name: str, *tests: AssertTest) -> int:
    code = 0

    # no trag1c, I'm not going to install dahlia just for this
    TEST_MESSAGE = "\x1b[1mTest\x1b[22m {!r}"
    PASSED = "\x1b[42m PASSED \x1b[49m"
    FAILED = "\x1b[41m FAILED \x1b[49m"
    ERROR_MESSAGE = (
        "\t \x1b[1;31mAssertion failed\x1b[39m:\x1b[22m {!r}\n\t   {}\n\t   {}"
    )

    width, _ = shutil.get_terminal_size()

    print(f" Test suite {name} ".center(width, "─"))

    for test in tests:
        _base_msg = TEST_MESSAGE.format(test)

        if test.run():
            print(PASSED, _base_msg)
        else:
            print(FAILED, _base_msg, file=sys.stderr)
            print(
                ERROR_MESSAGE.format(test, test.repr_left(), test.repr_right()),
                file=sys.stderr,
            )

            code += 1

    return code


def main() -> int:
    code = os.EX_OK

    code += test_alu_add("1", 9, 10, 19, False, False, False) > 0
    code += test_alu_add("2", 9, -10, -1, True, False, False) > 0
    code += test_alu_add("3", 127, 1, 0, False, True, False) > 0
    code += test_alu_add("4", -128, -1, -1, True, True, False) > 0
    code += test_alu_add("5", -128, -128, -128, True, False, True) > 0

    return code


if __name__ == "__main__":
    raise SystemExit(main())
