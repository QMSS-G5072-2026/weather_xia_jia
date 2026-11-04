import pandas as pd
import pytest
from pandas.testing import assert_frame_equal

from weather_jx2708 import (
    celsius_to_fahrenheit,
    clean_readings,
    summarize_temperatures,
)

# =============================================================================
# PART 1: UNIT TESTS
# =============================================================================


# TODO: add @pytest.mark.parametrize with at least 5 (celsius, expected) cases,
# including absolute zero itself.
@pytest.mark.parametrize("celsius, expected", [
    (0, 32),
    (100, 212),
    (-40, -40),
    (37, 98.6),
    (-273.15, -459.67),
])
def test_celsius_to_fahrenheit(celsius, expected):
    """Make sure that Celsius temperature conversions are done right."""
    result = celsius_to_fahrenheit(celsius)
    assert result == pytest.approx(expected)


# TODO: add @pytest.mark.parametrize with at least 4 (bad_input, expected_error) cases.
@pytest.mark.parametrize("bad_input, expected_error", [
    ("hello", TypeError),
    (None, TypeError),
    (True, TypeError),
    (-273.16, ValueError),
])
def test_celsius_to_fahrenheit_invalid(bad_input, expected_error):
    """Check whether the correct errors are raised when invalid input is given."""
    with pytest.raises(expected_error):
        celsius_to_fahrenheit(bad_input)


def test_summarize_temperatures():
    """Make sure that the summary does not include missing temperature values."""

    # Arrange
    temps = [5.0, 15.0, float("nan"), 25.0]
    # Act
    result = summarize_temperatures(temps)
    # Assert
    assert result["mean"] == pytest.approx(15.0)
    assert result["min"] == pytest.approx(5.0)
    assert result["max"] == pytest.approx(25.0)
    assert result["n_missing"] == 1


# =============================================================================
# PART 2: FIXTURES
# =============================================================================


@pytest.fixture
def raw_readings():
    return pd.DataFrame({
        "station": ["JFK", "CPK", "JFK", "CPK", "LGA"],
        "date": ["2026-07-02", "2026-07-01", "2026-07-01", "2026-07-02", "2026-07-01"],
        "temp_c": [30.0, 25.0, float("nan"), 999.0, 28.0],
    })


def test_raw_readings_fixture(raw_readings):
    """Make sure that the sample data has the correct columns, number of rows, and missing values."""
    assert list(raw_readings.columns) == ["station", "date", "temp_c"]
    assert len(raw_readings) == 5
    assert raw_readings["temp_c"].isna().sum() == 1


# =============================================================================
# PART 3: TESTING DATAFRAMES
# =============================================================================


def test_clean_readings(raw_readings):
    """Make sure that the weather data is cleaned correctly."""
    result = clean_readings(raw_readings)

    expected = pd.DataFrame({
        "station": ["CPK", "JFK", "LGA"],
        "date": ["2026-07-01", "2026-07-02", "2026-07-01"],
        "temp_c": [25.0, 30.0, 28.0],
        "temp_f": [77.0, 86.0, 82.4],
    })
    assert_frame_equal(result, expected)
