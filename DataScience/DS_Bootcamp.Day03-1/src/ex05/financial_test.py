import sys
import os
sys.path.append(os.path.abspath("../ex03"))

from financial import get_data
import pytest
def test_get_data_valid():
    result = get_data("AAPL", "Total Revenue")
    assert isinstance(result, tuple)

def test_get_data_invalid_ticker():
    with pytest.raises(ValueError):
        get_data("INVALID_TICKER", "Total Revenue")

def test_get_data_invalid_field():
    with pytest.raises(ValueError):
        get_data("MSFT", "Invalid_field")
