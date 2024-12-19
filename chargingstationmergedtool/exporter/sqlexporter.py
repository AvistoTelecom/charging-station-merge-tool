"""
SqlExporter Module

This module provides a class for exporting charging station and socket data to a SQL database.
It uses SQLAlchemy to connect to the database and export the data as geographic data.

Classes:
    SqlExporter: A class to handle the export of charging station and socket data to a SQL database.

Usage:
    To use this class, initialize it with the database configuration, charging station DataFrame, and socket DataFrame.
    Call the export method to save the data to the specified SQL tables.

Example:
    config = {
        'connection_url': 'postgresql://user:password@localhost:5432/mydatabase',
        'charging_stations_table_name': 'charging_stations',
        'sockets_table_name': 'sockets'
    }
    exporter = SqlExporter(config, charging_stations_df, sockets_df)
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
from sqlalchemy import create_engine

from chargingstationmergedtool.utils import to_geo_dataframe


class SqlExporter:
    """
    A class to handle the export of charging station and socket data to a SQL database.

    Attributes:
        __config (dict): Configuration dictionary containing database connection details.
        __charging_stations (pd.DataFrame): DataFrame containing charging station data.
        __sockets (pd.DataFrame): DataFrame containing socket data.
        __engine (Engine): SQLAlchemy engine instance for connecting to the database.
    """

    def __init__(self, config: dict, charging_stations: pd.DataFrame, sockets: pd.DataFrame):
        """
        Initializes the SqlExporter with the given configuration and data.

        Args:
            config (dict): Configuration dictionary containing database connection details.
            charging_stations (pd.DataFrame): DataFrame containing charging station data.
            sockets (pd.DataFrame): DataFrame containing socket data.
        """
        self._config = config
        self._charging_stations = charging_stations
        self._sockets = sockets
        self._engine = create_engine(config["connection_url"])

    def export(self):
        """
        Exports the charging station and socket data to the specified SQL tables.

        This method calls the export_charging_stations and export_sockets methods
        to save the data to the database.
        """
        self.export_charging_stations()
        self.export_sockets()

    def export_charging_stations(self):
        """
        Exports the charging station data to the specified SQL table.

        This method converts the charging stations DataFrame to a GeoDataFrame
        and saves it to the database using the table name specified in the configuration.
        """
        to_geo_dataframe(self._charging_stations).to_postgis(self._config['charging_stations_table_name'], self._engine)

    def export_sockets(self):
        """
        Exports the socket data to the specified SQL table.

        This method converts the sockets DataFrame to a GeoDataFrame
        and saves it to the database using the table name specified in the configuration.
        """
        to_geo_dataframe(self._sockets).to_postgis(self._config['sockets_table_name'], self._engine)
