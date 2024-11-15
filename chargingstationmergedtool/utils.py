import re
import pandas as pd
import geopandas as gpd

def is_power_rated_data(value):
    return re.match("\\d+[\\.,]?\\d*\\s?[kKwW]+", value) is not None

def is_int_data(value):
    return re.match("^\\d+$", value) is not None

def extract_power_rated(value: str) -> float:
    regex_numbers = "\\d+[\\.,]?\\d*"

    match = re.findall(regex_numbers, value)

    if match is not None and len(match) > 0:
        return float(match[0].replace(',', '.'))
    else:
        return None