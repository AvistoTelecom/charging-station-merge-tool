import json
import os
from datetime import datetime

class Config:
    distance: int
    type_export: str
    osm_config: dict
    data_gouv_config: dict
    sql_config: dict
    mongo_config: dict

    __key_path_file: str = "path_file"

    def __init__(self, path_config_file: str):

        if not os.path.exists(path_config_file):
            raise Exception("Config file not found")
        
        self._parse_config_file(path_config_file)
        self.export_directory_name = f"results{os.sep}{datetime.now().strftime('%d_%m_%Y_%H_%M_%S')}{os.sep}"


    def _parse_config_file(self, path_config_file: str):
        with open(path_config_file, 'r') as f:
            config_data = json.load(f)

            self._parse_common_block(config_data)
            self.osm_config = self.__extract_default_block(config_data, "osm")
            self.data_gouv_config = self.__extract_default_block(config_data, "data_gouv")
            self.sql_config = self.__extract_block(config_data, "sql")
            self.mongo_config = self.__extract_block(config_data, "mongo")

    def _parse_common_block(self, config_data: dict):
        block_name = "common"
        common_block = self.__extract_block(config_data, block_name)
        self.distance = self.__extract_key_in_block(common_block, "distance", block_name)
        self.type_export = self.__extract_key_in_block(common_block, "type_export", block_name)

    def __extract_default_block(self, config_data: dict, block_name: str) -> dict:
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
        if key not in block.keys():
            raise Exception(f"{key} key not in {block_name} block")
        
        return block[key]

    def __extract_block(self, config_data: dict, block_name: str) -> dict:
        if block_name not in config_data.keys():
            raise Exception(f"'{block_name}' block not found in config file")
        
        return config_data[block_name]