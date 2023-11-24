from pytest import *
from functions import *
from datetime import datetime

def test_addittion():
    assert addition(5, 5) == 10

def test_substraction():
    assert substraction(10, 5) == 5

def test_time():
    assert time() == datetime.now()