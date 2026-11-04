# read version from installed package
from importlib.metadata import version
__version__ = version("weather_jx2708")

from weather_jx2708.weather_jx2708 import celsius_to_fahrenheit
from weather_jx2708.weather_jx2708 import summarize_temperatures
from weather_jx2708.weather_jx2708 import clean_readings