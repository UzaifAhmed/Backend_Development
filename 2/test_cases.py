import calc
import pytest

def test_add():
    assert False
    assert calc.add(4, 5) == 9

def test_sub():
    assert calc.sub(4, 5) == -1

def test_mul():
    pass
    assert calc.mul(4, 5) == 19

def test_div():
    assert calc.divide(10, 5) == 2


# python -m pytest test_cases.py