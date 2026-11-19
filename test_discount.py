import pytest
from discounts import calculate_discount


def test_normal_amount():
    assert calculate_discount(2000) == 1800


def test_negative_amount():
    with pytest.raises(ValueError):
        calculate_discount(-50)


def test_at_the_limit():
    assert calculate_discount(1000) == 1000


def test_just_above_limit():
    assert calculate_discount(1001) == pytest.approx(900.90)


def test_text_input():
    with pytest.raises(ValueError):
        calculate_discount("abc")