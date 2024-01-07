# pyright: reportUnusedExpression = false

"""
This `debug` feature was imagined by @waffle-annie and I brought it to life.
"""

from impl import debug


debug("The answer is {x}!") @ 12  # debug at line 12
x = int(input("3 + 3 = "))
x = 6
