"""
Module: Transform

This module provides the Transform class, which is responsible for transforming
and merging charging station and socket data.

Imports:
    - uuid
    - geopandas as gpd
    - pandas as pd
    - numpy as np
    - chargingstationmergedtool.utils.to_geo_dataframe

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

import uuid

import geopandas as gpd
import numpy as np
import pandas as pd

from src.utils import to_geo_dataframe


class Transform:
    """
    A class to transform and merge charging station and socket data.

    Attributes:
        __charging_stations (pd.DataFrame): DataFrame to store charging station records.
        __sockets (pd.DataFrame): DataFrame to store socket records.
    """

    def __init__(self):
        """
        Initializes the Transform instance with empty charging stations and sockets.
        """
        self._charging_stations = None
        self._sockets = None

    def get_charging_stations(self) -> pd.DataFrame:
        """
        Returns the DataFrame containing charging station records.

        Returns:
            pd.DataFrame: The DataFrame of charging stations.
        """
        return self._charging_stations

    def get_sockets(self) -> pd.DataFrame:
        """
        Returns the DataFrame containing socket records.

        Returns:
            pd.DataFrame: The DataFrame of sockets.
        """
        return self._sockets

    def merge_datasources(self, datasource1: gpd.GeoDataFrame, datasource2: gpd.GeoDataFrame) -> gpd.GeoDataFrame:
        """
        Merges two GeoDataFrames into one.

        Parameters:
            datasource1 (gpd.GeoDataFrame): The first GeoDataFrame to merge.
            datasource2 (gpd.GeoDataFrame): The second GeoDataFrame to merge.

        Returns:
            gpd.GeoDataFrame: The merged GeoDataFrame.
        """
        return gpd.GeoDataFrame(pd.concat([datasource1, datasource2]), geometry='geometry', crs="EPSG:4326")
    
    def group_neighbouring(self, datasource: gpd.GeoDataFrame, distance_to_merge: int) -> dict:
        """
        Groups neighboring geometries within a specified distance.

        Parameters:
            datasource (gpd.GeoDataFrame): The GeoDataFrame containing geometries to group.
            distance_to_merge (int): The distance threshold for merging.

        Returns:
            dict: A dictionary where keys are indices of charging stations and values are lists of indices of neighboring stations.
        """
        geometries = datasource['geometry'].to_list()
        gdf = gpd.GeoDataFrame({'geometry': geometries}, crs='EPSG:4326')
        gdf = gdf.to_crs('EPSG:5234')

        index = gdf.index.to_numpy()
        length = len(index)
        index_already_merged = set()
        merge_dict = {}

        for index1 in range(length):
            if index1 not in index_already_merged:
                index_already_merged.add(index1)
                merge_dict[index1] = list()
                point1 = gdf.geometry[index1]
                distances = gdf.distance(point1)
                mask = (distances < distance_to_merge) & (index != index1) & (~np.isin(index, list(index_already_merged)))
                merge_dict[index1].extend(index[mask].tolist())
                index_already_merged.update(index[mask])

        return merge_dict
    
    def transform_data(self, datasource: gpd.GeoDataFrame, merge_dict: dict):
        """
        Transforms the data from the GeoDataFrame based on the merge dictionary.

        Parameters:
            datasource (gpd.GeoDataFrame): The GeoDataFrame containing the original data.
            merge_dict (dict): A dictionary mapping charging station indices to their neighboring indices.
        """
        for charging_station_index in merge_dict.keys():
            raw_data_charging_station = datasource.iloc[charging_station_index]
            charging_station = self.transform_to_charging_station(charging_station_index, raw_data_charging_station)
            self.append_charging_station_to_charging_station_dataframe(charging_station)

            socket = self.transform_to_socket(charging_station_index, raw_data_charging_station)
            self.append_socket_to_sockets_dataframe(socket)
            for socket_index in merge_dict[charging_station_index]:
                socket = self.transform_to_socket(charging_station_index, datasource.iloc[socket_index])
                self.append_socket_to_sockets_dataframe(socket)
    
    def append_charging_station_to_charging_station_dataframe(self, charging_station: dict):
        """
        Appends a charging station record to the charging stations DataFrame.

        Parameters:
            charging_station (dict): A dictionary containing charging station data.
        """
        charging_station_record = pd.DataFrame(charging_station, index=["id"])
        if self._charging_stations is None:
            self._charging_stations = charging_station_record
        else:
            self._charging_stations = pd.concat([self._charging_stations, charging_station_record], ignore_index=True)
    
    def export_to_parquet_files(self, export_directory: str):
        """
        Exports the charging stations and sockets DataFrames to Parquet files.

        Parameters:
            export_directory (str): The directory where the Parquet files will be saved.
        """
        # Convert to GeoDataFrame to be exported into geoparquet
        charging_stations = to_geo_dataframe(self._charging_stations)
        sockets = to_geo_dataframe(self._sockets)

        charging_stations.to_parquet(f"{export_directory}charging_stations.parquet")
        sockets.to_parquet(f"{export_directory}sockets.parquet")

    def transform_to_charging_station(self, index: int, raw_data: dict) -> dict:
        """
        Transforms raw data into a charging station dictionary.

        Parameters:
            index (int): The index of the charging station.
            raw_data (dict): The raw data for the charging station.

        Returns:
            dict: A dictionary representing the charging station.
        """
        return {
            "id": index,
            "geometry": raw_data["geometry"]
        }
    
    def transform_to_socket(self, charging_station_index: int, raw_data: pd.Series) -> pd.Series:
        """
        Transforms raw data into a socket dictionary.

        Parameters:
            charging_station_index (int): The index of the associated charging station.
            raw_data (pd.Series): The raw data for the socket.

        Returns:
            pd.Series: A dictionary representing the socket.
        """
        result = raw_data.copy()
        result["id"] = str(uuid.uuid4())
        result["charging_station_index"] = charging_station_index
        
        return result

    def append_socket_to_sockets_dataframe(self, socket: pd.Series):
        """
        Appends a socket record to the sockets DataFrame if it does not already exist.

        Parameters:
            socket (dict): A dictionary containing socket data.
        """
        socket_record = socket.to_frame().T

        if self._sockets is None:
            self._sockets = socket_record
        else:
            sockets_already_added_into_this_charging_station = self._sockets[
                (self._sockets["charging_station_index"] == socket["charging_station_index"]) & 
                (self._sockets["power_rated"] == socket["power_rated"]) & 
                (self._sockets["socket_type_ef"] == socket["socket_type_ef"]) & 
                (self._sockets["socket_type_2"] == socket["socket_type_2"]) & 
                (self._sockets["socket_type_combo_ccs"] == socket["socket_type_combo_ccs"]) & 
                (self._sockets["socket_type_chademo"] == socket["socket_type_chademo"]) & 
                (self._sockets["socket_type_autre"] == socket["socket_type_autre"])
            ]

            if len(sockets_already_added_into_this_charging_station) == 0:
                self._sockets = pd.concat([self._sockets, socket_record], ignore_index=True)