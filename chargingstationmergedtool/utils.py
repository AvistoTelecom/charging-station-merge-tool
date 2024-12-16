"""
Module: Utilities

This module provides utility functions for handling geographic data, 
hashing files, and exporting graphs.

Imports:
    - re
    - geopandas as gpd
    - pandas as pd
    - os
    - hashlib

Constants:
    - PATH_LAST_EXECUTION: Path to the last execution record.

License:
    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU Lesser General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
    GNU Lesser General Public License for more details.

    You should have received a copy of the GNU Lesser General Public License
    along with this program. If not, see <https://www.gnu.org/licenses/>.
"""

import re
import geopandas as gpd
import pandas as pd
import os
import hashlib

PATH_LAST_EXECUTION = "results/last_execution"

def is_power_rated_data(value) -> bool:
    """
    Checks if the given value is a valid power rated data format.

    Parameters:
        value (str): The value to check.

    Returns:
        bool: True if the value matches the power rated format, False otherwise.
    """
    return re.match("\\d+[\\.,]?\\d*\\s?[kKwW]+", value) is not None

def is_int_data(value) -> bool:
    """
    Checks if the given value is a valid integer format.

    Parameters:
        value (str): The value to check.

    Returns:
        bool: True if the value is an integer, False otherwise.
    """
    return re.match("^\\d+$", value) is not None

def extract_power_rated(value: str) -> float:
    """
    Extracts the numeric power rating from a given string.

    Parameters:
        value (str): The string containing the power rating.

    Returns:
        float: The extracted power rating as a float, or None if not found.
    """
    regex_numbers = "\\d+[\\.,]?\\d*"
    match = re.findall(regex_numbers, value)

    if match is not None and len(match) > 0:
        return float(match[0].replace(',', '.'))
    else:
        return None
    
def export_graph_to_svg(charging_station_geo_dataframe: gpd.GeoDataFrame, socket_geo_dataframe: gpd.GeoDataFrame, filename: str):
    """
    Exports a graph of charging stations and sockets to an SVG file.

    Parameters:
        charging_station_geo_dataframe (gpd.GeoDataFrame): GeoDataFrame of charging stations.
        socket_geo_dataframe (gpd.GeoDataFrame): GeoDataFrame of sockets.
        filename (str): The name of the file to save the SVG as (without extension).
    """
    import matplotlib.pyplot as plt
    from shapely.geometry import box

    fig, ax = plt.subplots()
    fig.set_size_inches(11.69, 8.27)

    min_longitude = -5.14
    max_longitude = 9.53
    min_latitude = 41.26
    max_latitude = 51.09

    # Create a bounding box
    bbox = box(min_longitude, min_latitude, max_longitude, max_latitude)

    metropole_charging_station = charging_station_geo_dataframe[charging_station_geo_dataframe.geometry.within(bbox)]
    metropole_sockets = socket_geo_dataframe[socket_geo_dataframe.geometry.within(bbox)]

    metropole_sockets.plot(ax=ax, marker='o', color='red', markersize=0.1)
    metropole_charging_station.plot(ax=ax, marker='o', color='blue', markersize=0.1)

    plt.savefig(f"{filename}.svg")

def to_geo_dataframe(data: pd.DataFrame) -> gpd.GeoDataFrame:
    """
    Converts a DataFrame to a GeoDataFrame.

    Parameters:
        data (pd.DataFrame): The DataFrame to convert.

    Returns:
        gpd.GeoDataFrame: The converted GeoDataFrame.
    """
    return gpd.GeoDataFrame(data, geometry='geometry', crs="EPSG:4326")

def compare_hash(path_hash_file: str, path_file: str) -> bool:
    """
    Compares the hash of a file with a previously stored hash.

    Parameters:
        path_hash_file (str): The path to the hash file.
        path_file (str): The path to the file to compare.

    Returns:
        bool: True if the hashes match, False otherwise.
    """
    if not os.path.exists(path_hash_file):
        return False
    else:
        with open(path_hash_file, 'r') as f:
            old_hash = f.read()

        sha256 = hashlib.sha512()
        BUF_SIZE = 65536  # lets read stuff in 64kb chunks!

        if os.path.exists(path_file):
            with open(path_file, 'rb') as f:
                while True:
                    data = f.read(BUF_SIZE)
                    if not data:
                        break
                    sha256.update(data)

            return old_hash == sha256.hexdigest()
        return False

def write_hash_file(path_hash_file: str, path_file: str):
    """
    Writes the SHA-512 hash of a file to a specified hash file.

    Parameters:
        path_hash_file (str): The path to the hash file where the hash will be written.
        path_file (str): The path to the file for which the hash will be calculated.

    Raises:
        FileNotFoundError: If the specified file does not exist.
    """
    sha256 = hashlib.sha512()
    BUF_SIZE = 65536  # Read in 64kb chunks

    if not os.path.exists(path_file):
        raise FileNotFoundError(path_file)

    with open(path_file, 'rb') as f:
        while True:
            data = f.read(BUF_SIZE)
            if not data:
                break
            sha256.update(data)

    # Clean old hash file
    if os.path.exists(path_hash_file):
        os.remove(path_hash_file)

    with open(path_hash_file, 'w') as f:
        f.write(sha256.hexdigest())

def extract_path_last_execution() -> str:
    """
    Extracts the path of the last execution from a file.

    Returns:
        str: The path of the last execution if it exists, None otherwise.
    """
    if not os.path.exists("results") or not os.path.exists(PATH_LAST_EXECUTION):
        return None
    else:
        with open(PATH_LAST_EXECUTION, "r") as f:
            return f.read()

def write_path_last_execution(path):
    """
    Writes the specified path to the last execution file.

    Parameters:
        path (str): The path to write to the last execution file.
    """
    if os.path.exists(PATH_LAST_EXECUTION):
        os.remove(PATH_LAST_EXECUTION)

    with open(PATH_LAST_EXECUTION, "w") as f:
        f.write(path)