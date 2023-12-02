import calc
import pytest

def test_add():
    assert False
    assert calc.add(4, 5) == 9

def test_add():
    assert calc.sub(4, 5) == -1

def test_add():
    pass
    assert calc.mul(4, 5) == 19

def test_add():
    assert calc.divide(10, 5) == 2


# python -m pytest test_cases.py