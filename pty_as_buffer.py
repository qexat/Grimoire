"""
Why using `io.StringIO()` when you can open a whole ass pseudo-terminal and read from/write to it?
"""


import os
import pty


def main() -> int:
    mpty, stty = pty.openpty()
    os.write(stty, b"Hello World!\n")
    value = os.read(mpty, 14).replace(b"\r\n", b"\n")
    print(value)

    return os.EX_OK


if __name__ == "__main__":
    raise SystemExit(main())
