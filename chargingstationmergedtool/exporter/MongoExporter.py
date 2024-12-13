"""
MongoExporter Module

This module provides a class for exporting charging station and socket data to a MongoDB database.
It extends the AbstractNoSqlExporter class and implements the export functionality specific to MongoDB.

Classes:
    MongoExporter: A class to handle the export of charging station and socket data to MongoDB.

Usage:
    To use this class, initialize it with the MongoDB configuration, charging station DataFrame, and socket DataFrame.
    Call the export method to save the data to the specified MongoDB collection.

Example:
    config = {
        'connection_url': 'mongodb://localhost:27017',
        'database_name': 'charging_stations_db',
        'charging_stations_collection_name': 'stations'
    }
    exporter = MongoExporter(config, charging_stations_df, sockets_df)
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
from pymongo import MongoClient

class MongoExporter(AbstractNoSqlExporter):
    """
    A class to handle the export of charging station and socket data to MongoDB.

    Attributes:
        __config (dict): Configuration dictionary containing MongoDB connection details.
        __client (MongoClient): MongoDB client instance for connecting to the database.
    """

    def __init__(self, config: dict, charging_stations: pd.DataFrame, sockets: pd.DataFrame):
        """
        Initializes the MongoExporter with the given configuration and data.

        Args:
            config (dict): Configuration dictionary containing MongoDB connection details.
            charging_stations (pd.DataFrame): DataFrame containing charging station data.
            sockets (pd.DataFrame): DataFrame containing socket data.
        """
        super().__init__(charging_stations, sockets)
        self.__config = config
        self.__client = MongoClient(config['connection_url'], timeoutMS=7200)

    def export(self):
        """
        Exports the charging station and socket data to the specified MongoDB collection.

        This method retrieves the database and collection specified in the configuration
        and inserts the transformed data into the collection.

        Raises:
            Exception: If there is an error during the export process.
        """
        db = self.__client.get_database(self.__config['database_name'])
        collection = db.get_collection(self.__config['charging_stations_collection_name'])

        collection.insert_many(self.transform_data_to_dict())
