import re
import geopandas as gpd
import pandas as pd
import os
import hashlib

PATH_LAST_EXECUTION = "results/last_execution"

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
    
def export_graph_to_svg(charging_station_geo_dataframe: gpd.GeoDataFrame, socket_geo_dataframe: gpd.GeoDataFrame, filename: str):
    import matplotlib.pyplot as plt
    from shapely.geometry import box

    fig, ax = plt.subplots()

    fig.set_size_inches(11.69, 8.27)

    min_longitude = -5.14
    max_longitude = 9.53
    min_latitude = 41.26
    max_latitude = 51.09

    # Créer une boîte englobante (bounding box)
    bbox = box(min_longitude, min_latitude, max_longitude, max_latitude)

    metropole_charging_station = charging_station_geo_dataframe[charging_station_geo_dataframe.geometry.within(bbox)]
    metropole_sockets = socket_geo_dataframe[socket_geo_dataframe.geometry.within(bbox)]

    metropole_sockets.plot(ax=ax, marker='o', color='red', markersize=0.1)
    metropole_charging_station.plot(ax=ax, marker='o', color='blue', markersize=0.1)

    plt.savefig(f"{filename}.svg")

def to_geo_dataframe(data: pd.DataFrame) -> gpd.GeoDataFrame:
    return gpd.GeoDataFrame(data, geometry='geometry', crs="EPSG:4326")

def compare_hash(path_hash_file: str, path_file: str) -> bool:
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
    sha256 = hashlib.sha512()
    BUF_SIZE = 65536  # lets read stuff in 64kb chunks!

    if not os.path.exists(path_file):
        raise FileNotFoundError(path_file)

    with open(path_file, 'rb') as f:
        while True:
            data = f.read(BUF_SIZE)
            if not data:
                break
            sha256.update(data)

    # clean old hash file
    if os.path.exists(path_hash_file):
        os.remove(path_hash_file)

    with open(path_hash_file, 'w') as f:
        f.write(sha256.hexdigest())

def extract_path_last_execution():
    if not os.path.exists("results") or not os.path.exists(PATH_LAST_EXECUTION):
        return None
    else:
        with open(PATH_LAST_EXECUTION, "r") as f:
            return f.read()

def write_path_last_execution(path):
    if os.path.exists(PATH_LAST_EXECUTION):
        os.remove(PATH_LAST_EXECUTION)

    with open(PATH_LAST_EXECUTION, "w") as f:
        f.write(path)