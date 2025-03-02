""" Common fixtures for test tasks """
import pytest
from calculator import Calculator


@pytest.fixture(scope="module")
def init_calculator():
    def _init_calculator(*args):
        return Calculator(*args)

    return _init_calculator
