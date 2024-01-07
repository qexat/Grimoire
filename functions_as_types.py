# type: ignore
"""
Extremely rare untyped snippet of Python code produced by myself.

It does weird stuff that I don't know how to describe, hopefully the code
speaks for itself.

In summary, it's a way to piss off strict typing evangelists... ;) 
"""


def metaclass(func):
    class _FuncMeta(type):
        def __call__(self, *args):
            return func(self, *args)

    return _FuncMeta


@metaclass
def fib_type(self, n):
    if n < 0:
        raise ValueError("dude this is fibonacci")
    if n <= 1:
        return n
    return self(n - 2) + self(n - 1)


class fib(metaclass=fib_type):
    pass


def main() -> None:
    n = 10

    for i in range(n):
        print(fib(i))


if __name__ == "__main__":
    main()
