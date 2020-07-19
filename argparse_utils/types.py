# -*- coding: utf-8 -*-
from argparse import ArgumentTypeError
from functools import partial


# mypy still doesn't have support for a partial type of some sorts so ignoring locally leaving type
# hint for ease of code reading and understanding
def int_ge_two() -> int:
    return partial(int_ge_than_x, x=2)  # type: ignore


def int_ge_zero() -> int:
    return partial(int_ge_than_x, x=0)  # type: ignore


def int_ge_than_x(string: str, x: int) -> int:
    """ return int of string if greater equal to x """
    try:
        number = int(string)
        if number <= x:
            raise ValueError
        return number
    except ValueError:
        raise ArgumentTypeError(f"Not an int >= 0: '{string}'")

