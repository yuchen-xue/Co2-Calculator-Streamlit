""" Test calculator functionality """


def test_basic(init_calculator):
    c = init_calculator("medium-diesel-car", 15, "km")
    result, result_unit = c.calculate_emission()
    assert result == 2.6 and result_unit == "kg"


def test_default_distance_unit(init_calculator):
    c = init_calculator("large-petrol-car", 1800.5)
    result, result_unit = c.calculate_emission()
    assert result == 507.7 and result_unit == "kg"


def test_show_result_in_g(init_calculator):
    c = init_calculator("train", 14500, "m")
    result, result_unit = c.calculate_emission()
    assert result == 87 and result_unit == "g"


def test_show_result_in_kg(init_calculator):
    c = init_calculator("train", 14500, "m", "kg")
    result, result_unit = c.calculate_emission()
    assert result == 0.1 and result_unit == "kg"
