"""
MongoFileExporter Module

This module provides a class for exporting charging station and socket data to JSON files.
It extends the AbstractNoSqlExporter class and implements the export functionality specific to file-based storage.

Classes:
    MongoFileExporter: A class to handle the export of charging station and socket data to JSON files.

Usage:
    To use this class, initialize it with the charging station DataFrame, socket DataFrame, and the export directory path.
    Call the export method to save the data to JSON files in the specified directory.

Example:
    exporter = MongoFileExporter(charging_stations_df, sockets_df, '/path/to/export/directory')
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
from chargingstationmergedtool.exporter.AbstractNoSqlExporter import AbstractNoSqlExporter
import json

class MongoFileExporter(AbstractNoSqlExporter):
    """
    A class to handle the export of charging station and socket data to JSON files.

    Attributes:
        __export_directory_path (str): The directory path where the JSON files will be saved.
    """

    def __init__(self, charging_stations: pd.DataFrame, sockets: pd.DataFrame, export_directory_path: str):
        """
        Initializes the MongoFileExporter with the given data and export directory.

        Args:
            charging_stations (pd.DataFrame): DataFrame containing charging station data.
            sockets (pd.DataFrame): DataFrame containing socket data.
            export_directory_path (str): The directory path where the JSON files will be saved.
        """
        super().__init__(charging_stations, sockets)
        self.__export_directory_path = export_directory_path

    def export(self):
        """
        Exports the charging station and socket data to JSON files.

        This method creates a JSON file for each charging station in the specified export directory.
        The filename is based on the charging station ID.

        Raises:
            Exception: If there is an error during the file writing process.
        """
        for charging_station in self.transform_data_to_dict():
            with open(f"{self.__export_directory_path}/charging_station_{charging_station['id']}.json", 'w') as f:
                json.dump(charging_station, f, indent=2)
