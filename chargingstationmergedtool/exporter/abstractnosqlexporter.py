"""
AbstractNoSqlExporter Module

This module provides an abstract class for exporting charging station and socket data to NoSQL databases.
It includes methods for transforming the data into a dictionary format suitable for exporting.

Classes:
    AbstractNoSqlExporter: A class to handle the transformation of charging station and socket data for NoSQL export.

Usage:
    To use this class, create a subclass that implements the specific export functionality for a NoSQL database.
    Initialize the subclass with DataFrames containing charging station and socket data, and use the transform_data_to_dict method
    to prepare the data for export.

Example:
    class MyNoSqlExporter(AbstractNoSqlExporter):
        def export(self):
            data = self.transform_data_to_dict()
            # Implement export logic here

    exporter = MyNoSqlExporter(charging_stations_df, sockets_df)
    exporter.export()

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

import pandas as pd


class AbstractNoSqlExporter:
    """
    A class to handle the transformation of charging station and socket data for NoSQL export.

    Attributes:
        __charging_stations (pd.DataFrame): DataFrame containing charging station data.
        __sockets (pd.DataFrame): DataFrame containing socket data.
    """

    def __init__(self, charging_stations: pd.DataFrame, sockets: pd.DataFrame):
        """
        Initializes the AbstractNoSqlExporter with the given charging stations and sockets DataFrames.

        Args:
            charging_stations (pd.DataFrame): DataFrame containing charging station data.
            sockets (pd.DataFrame): DataFrame containing socket data.
        """
        self._charging_stations = charging_stations
        self._sockets = sockets

    def transform_data_to_dict(self) -> list[dict]:
        """
        Transforms the charging station data into a list of dictionaries.

        Each dictionary contains the id, latitude, longitude, and associated sockets for a charging station.

        Returns:
            list[dict]: A list of dictionaries representing the charging stations and their sockets.
        """
        results = list()

        for _, row in self._charging_stations.iterrows():
            charging_station_id = row['id']
            results.append({
                "id": charging_station_id,
                "latitude": row['geometry'].y,
                "longitude": row['geometry'].x,
                "sockets": self.extract_sockets(charging_station_id)
            })

        return results
    
    def extract_sockets(self, charging_station_id: int) -> list[dict]:
        """
        Extracts socket information for a given charging station.

        This method retrieves all sockets associated with the specified charging station ID
        and returns them as a list of dictionaries.

        Args:
            charging_station_id (int): The ID of the charging station for which to extract sockets.

        Returns:
            list[dict]: A list of dictionaries representing the sockets associated with the charging station.
        """
        results = list()

        for _, row in self._sockets[self._sockets['charging_station_id'] == charging_station_id].iterrows():
            results.append({
                "id": row['id'],
                "latitude": row['geometry'].y,
                "longitude": row['geometry'].x,
                "power_rated": row['power_rated'],
                "number_of_sockets": row['number_of_sockets'],
                "socket_type_ef": row['socket_type_ef'],
                "socket_type_2": row['socket_type_2'],
                "socket_type_combo_ccs": row['socket_type_combo_ccs'],
                "socket_type_chademo": row['socket_type_chademo'],
                "socket_type_autre": row['socket_type_autre'],
                "id_itinerance": row['id_itinerance'],
                "retrieve_from": row['retrieve_from']
            })

        return results
