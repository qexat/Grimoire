class arrowint(int):
    def __neg__(self):
        for key, value in globals().items():
            if self is value:
                globals()[key] = type(self)(self - 1)
        return self


x = arrowint(5)


while 0 <-- x:  # fmt: off
    print(x)
