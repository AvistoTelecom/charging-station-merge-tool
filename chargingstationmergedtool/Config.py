"""
Module: Config

This module provides the Config class, which is responsible for loading and parsing
configuration settings from a JSON file.

Imports:
    - json
    - os
    - datetime

Classes:
    - Config

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

import json
import os
from datetime import datetime

class Config:
    """
    A class to handle configuration settings for the application.

    Attributes:
        distance (int): The distance setting from the configuration.
        type_export (str): The type of export setting from the configuration.
        osm_config (dict): Configuration settings related to OSM.
        data_gouv_config (dict): Configuration settings related to data from the government.
        sql_config (dict): Configuration settings for SQL database.
        mongo_config (dict): Configuration settings for MongoDB.
        export_directory_name (str): The directory name for export results, timestamped.
    """

    distance: int
    type_export: str
    osm_config: dict
    data_gouv_config: dict
    sql_config: dict
    mongo_config: dict

    __key_path_file: str = "path_file"

    def __init__(self, path_config_file: str):
        """
        Initializes the Config instance by loading the configuration from the specified file.

        Parameters:
            path_config_file (str): The path to the configuration file.

        Raises:
            Exception: If the configuration file does not exist.
        """
        if not os.path.exists(path_config_file):
            raise Exception("Config file not found")
        
        self._parse_config_file(path_config_file)
        self.export_directory_name = f"results{os.sep}{datetime.now().strftime('%d_%m_%Y_%H_%M_%S')}{os.sep}"

    def _parse_config_file(self, path_config_file: str):
        """
        Parses the configuration file and extracts relevant settings.

        Parameters:
            path_config_file (str): The path to the configuration file.
        """
        with open(path_config_file, 'r') as f:
            config_data = json.load(f)

            self._parse_common_block(config_data)
            self.osm_config = self.__extract_default_block(config_data, "osm")
            self.data_gouv_config = self.__extract_default_block(config_data, "data_gouv")
            self.sql_config = self.__extract_block(config_data, "sql")
            self.mongo_config = self.__extract_block(config_data, "mongo")

    def _parse_common_block(self, config_data: dict):
        """
        Parses the common block of the configuration data.

        Parameters:
            config_data (dict): The entire configuration data loaded from the JSON file.
        """
        block_name = "common"
        common_block = self.__extract_block(config_data, block_name)
        self.distance = self.__extract_key_in_block(common_block, "distance", block_name)
        self.type_export = self.__extract_key_in_block(common_block, "type_export", block_name)

    def __extract_default_block(self, config_data: dict, block_name: str) -> dict:
        """
        Extracts a default block from the configuration data.

        Parameters:
            config_data (dict): The entire configuration data loaded from the JSON file.
            block_name (str): The name of the block to extract.

        Returns:
            dict: A dictionary containing the default configuration for the specified block.
        """
        block = self.__extract_block(config_data, block_name)

        path_file = self.__extract_key_in_block(block, self.__key_path_file, block_name)

        config = {
            "need_to_download": True,
            "path_file": ""
        }

        if path_file is not None and path_file != "":
            config = {
                "need_to_download": False,
                "path_file": path_file
            }

        return config

    def __extract_key_in_block(self, block: dict, key: str, block_name: str):
        """
        Extracts a specific key from a given block of configuration data.

        Parameters:
            block (dict): The block of configuration data.
            key (str): The key to extract from the block.
            block_name (str): The name of the block for error reporting.

        Returns:
            The value associated with the specified key.

        Raises:
            Exception: If the key is not found in the block.
        """
        if key not in block.keys():
            raise Exception(f"{key} key not in {block_name} block")
        
        return block[key]

    def __extract_block(self, config_data: dict, block_name: str) -> dict:
        """
        Extracts a specific block from the configuration data.

        Parameters:
            config_data (dict): The entire configuration data loaded from the JSON file.
            block_name (str): The name of the block to extract.

        Returns:
            dict: The dictionary corresponding to the specified block.

        Raises:
            Exception: If the specified block is not found in the configuration data.
        """
        if block_name not in config_data.keys():
            raise Exception(f"'{block_name}' block not found in config file")
        
        return config_data[block_name]