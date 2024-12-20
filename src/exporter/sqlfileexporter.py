"""
SqlFileExporter Module

This module provides a class for exporting charging station and socket data to SQL files.
It uses Jinja2 templates to generate SQL scripts based on the provided DataFrames.

Classes:
    SqlFileExporter: A class to handle the export of charging station and socket data to SQL files.

Usage:
    To use this class, initialize it with the charging station DataFrame, socket DataFrame, and the export directory path.
    Call the export method to save the data to SQL files in the specified directory.

Example:
    exporter = SqlFileExporter(charging_stations_df, sockets_df, '/path/to/export/directory')
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

import os

import pandas as pd
from jinja2 import Environment, PackageLoader, select_autoescape


class SqlFileExporter:
    """
    A class to handle the export of charging station and socket data to SQL files.

    Attributes:
        __export_directory_path (str): The directory path where the SQL files will be saved.
        __charging_stations (pd.DataFrame): DataFrame containing charging station data.
        __sockets (pd.DataFrame): DataFrame containing socket data.
        __env (Environment): Jinja2 environment for rendering SQL templates.
    """

    def __init__(self, charging_stations: pd.DataFrame, sockets: pd.DataFrame, export_directory_path: str):
        """
        Initializes the SqlFileExporter with the given data and export directory.

        Args:
            charging_stations (pd.DataFrame): DataFrame containing charging station data.
            sockets (pd.DataFrame): DataFrame containing socket data.
            export_directory_path (str): The directory path where the SQL files will be saved.
        """
        self._export_directory_path = export_directory_path
        self._charging_stations = charging_stations
        self._sockets = sockets
        self._env = Environment(
            loader=PackageLoader("src"),
            autoescape=select_autoescape()
        )

    def export(self):
        """
        Exports the charging station and socket data to SQL files.

        This method calls the export_charging_stations and export_sockets methods
        to save the data to the respective SQL files.
        """
        self.export_charging_stations()
        self.export_sockets()

    def export_charging_stations(self):
        """
        Exports the charging station data to a SQL file.

        This method uses a Jinja2 template to generate the SQL script for inserting
        charging station data and saves it to a file named 'charging_stations.sql'
        in the specified export directory.
        """
        template = self._env.get_template(f"sql{os.sep}charging_stations.sql.j2")
        with open(f"{self._export_directory_path}{os.sep}charging_stations.sql", 'w') as f:
            f.write(template.render(charging_stations=self._charging_stations))

    def export_sockets(self):
        """
        Exports the socket data to a SQL file.

        This method uses a Jinja2 template to generate the SQL script for inserting
        socket data and saves it to a file named 'sockets.sql' in the specified
        export directory.
        """
        template = self._env.get_template(f"sql{os.sep}sockets.sql.j2")
        with open(f"{self._export_directory_path}{os.sep}sockets.sql", 'w') as f:
            f.write(template.render(sockets=self._sockets))
