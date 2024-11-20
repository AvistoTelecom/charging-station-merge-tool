import re
import geopandas as gpd
import pandas as pd

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
