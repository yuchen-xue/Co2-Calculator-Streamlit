""" Check if a wrong input query would trigger a ValueError """
import pytest


def test_with_wrong_transportation(init_calculator):
    with pytest.raises(ValueError, match="Invalid transportation method!"):
        init_calculator("unsuppported-vehicle", 15, "km", "g")


def test_with_wrong_distance_unit(init_calculator):
    with pytest.raises(ValueError, match="Invalid unit of distance!"):
        init_calculator("train", 15, "cm", "g")


def test_with_wrong_output_unit(init_calculator):
    with pytest.raises(ValueError, match="Invalid unit of output!"):
        init_calculator("train", 15, "m", "ton")
