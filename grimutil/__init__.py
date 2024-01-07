import importlib.util
import sys

_ERR_MESSAGE = """\
Error: This snippet depends on an external package called `{0}`.
Please install it by typing the following command:

    pip install {0}
"""


def requires_package(name: str, *, _no_exit: bool = False) -> None:
    if importlib.util.find_spec(name) is None:
        sys.stderr.write("\x1b[31m")
        print(_ERR_MESSAGE.format(name), file=sys.stderr)
        sys.stderr.write("\x1b[39m")

    if not _no_exit:
        raise SystemExit(1)


def requires_packages(*names: str) -> None:
    for name in names:
        requires_package(name, _no_exit=True)

    raise SystemExit(1)
