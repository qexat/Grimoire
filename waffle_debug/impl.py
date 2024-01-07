import inspect
import sys
from string import Formatter
from types import FrameType
from typing import Any


class debug:
    def __init__(self, value: str) -> None:
        self.__value = value

        if (cur_frame := inspect.currentframe()) is None or (
            prev_frame := cur_frame.f_back
        ) is None:
            raise RuntimeError

        self.__debugframe = prev_frame
        self.__line_number = -1

    def __matmul__(self, line_number: int) -> None:
        if line_number <= 0:
            raise ValueError("line number must be positive")

        self.__line_number = line_number

        def trace_func(frame: FrameType, event: str, arg: Any) -> None:
            formatter = Formatter()

            if frame.f_lineno == self.__line_number and event == "return":
                args_required = [
                    arg[1]
                    for arg in formatter.parse(self.__value)
                    if arg[1] is not None
                ]
                args_given = {
                    key: value
                    for key, value in frame.f_locals.items()
                    if key in args_required
                }
                if len(args_required) != len(args_given):
                    raise NameError("some variables are not defined")

                print(formatter.vformat(self.__value, [], args_given))

        self.__debugframe.f_trace = trace_func

        sys.settrace(trace_func)
