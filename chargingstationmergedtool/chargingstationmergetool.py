"""
ChargingStationMergeTools Module

This module provides a class for processing and merging charging station data from OpenStreetMap (OSM) and Data Gouv sources.
It includes functionalities for downloading, parsing, transforming, and exporting the data.

Classes:
    ChargingStationMergeTools: A class to handle the merging of charging station data from different sources.

Usage:
    To use this module, create an instance of the ChargingStationMergeTools class with the path to the configuration file,
    and then call the process method to execute the data processing workflow.

Example:
    tool = ChargingStationMergeTools('path/to/config/file')
    tool.process()

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
import geopandas as gpd
from chargingstationmergedtool.Config import Config
from chargingstationmergedtool.parser import OsmParser, DataGouvParser
from chargingstationmergedtool.Transform import Transform
from chargingstationmergedtool.exporter import *
from chargingstationmergedtool.utils import compare_hash, write_hash_file, extract_path_last_execution, write_path_last_execution

class ChargingStationMergeTools:
    """
    A class to handle the merging of charging station data from OpenStreetMap (OSM) and Data Gouv sources.

    Attributes:
        osm_parser_geo_data_frame (gpd.GeoDataFrame): GeoDataFrame containing parsed OSM data.
        data_gouv_parser_geo_data_frame (gpd.GeoDataFrame): GeoDataFrame containing parsed Data Gouv data.
    """
    osm_parser_geo_data_frame: gpd.GeoDataFrame
    data_gouv_parser_geo_data_frame: gpd.GeoDataFrame

    def __init__(self, path_config_file: str):
        """
        Initializes the ChargingStationMergeTools with the given configuration file.

        Args:
            path_config_file (str): The path to the configuration file.
        """
        self.__config = Config(path_config_file)
        self.__osm_file_no_change = False
        self.__data_gouv_file_no_change = False
        os.makedirs(self.__config.export_directory_name, exist_ok=True)

    def process(self):
        """
        Main processing method that orchestrates the downloading, parsing, transforming, and exporting of data.
        """
        self.path_last_execution = extract_path_last_execution()
        self.process_osm()
        self.process_data_gouv()
        if not (self.__osm_file_no_change == True and self.__data_gouv_file_no_change == True):
            self.process_transform()
            write_path_last_execution(self.__config.export_directory_name)
        else:
            print("Files not changed")
            os.rmdir(self.__config.export_directory_name)

    def process_osm(self):
        """
        Processes the OSM data by downloading, filtering, parsing, and exporting it to a GeoDataFrame.
        """
        osm_parser = OsmParser()
        if self.__config.osm_config["need_to_download"]:
            print("[ ] - Download OSM file")
            osm_parser.download_datasource(self.__config)
            print("[x] - Download OSM file")

        # Filter initial pbf
        print("[ ] - Filter with osmosis")
        osm_parser.filtering_with_osmosis(self.__config.osm_config["path_file"], f"{self.__config.export_directory_name}filtered_charging_stations.osm.pbf")
        self.__config.osm_config["path_file"] = f"{self.__config.export_directory_name}filtered_charging_stations.osm.pbf"
        print("[x] - Filter with osmosis")

        if self.path_last_execution is None or not compare_hash(f"{self.path_last_execution}osm.hash", self.__config.osm_config["path_file"]):
            print("[ ] - Parse OSM file")
            osm_parser.load_pbf(self.__config.osm_config["path_file"])
            print("[x] - Parse OSM file")
            osm_parser.export_to_geoparquet(f"{self.__config.export_directory_name}osm.parquet")
            self.osm_parser_geo_data_frame = osm_parser.convert_to_geoDataFrame()
            write_hash_file(f"{self.__config.export_directory_name}osm.hash", self.__config.osm_config["path_file"])
        else:
            print("OSM file no change since last process")
            self.__osm_file_no_change = True
            self.osm_parser_geo_data_frame = osm_parser.import_from_geoparquet(f"{self.path_last_execution}osm.parquet")


    def process_data_gouv(self):
        """
        Processes the Data Gouv data by downloading, parsing, and exporting it to a GeoDataFrame.
        """
        data_gouv_parser = DataGouvParser()

        if self.__config.data_gouv_config["need_to_download"]:
            print("[ ] - Download Data gouv file")
            data_gouv_parser.download_datasource(self.__config)
            print("[x] - Download Data gouv file")

        if self.path_last_execution is None or not compare_hash(f"{self.path_last_execution}data_gouv.hash", self.__config.osm_config["path_file"]):
            print("[ ] - Parse Data gouv file")
            data_gouv_parser.parse_file(self.__config.data_gouv_config["path_file"])
            print("[x] - Parse Data gouv file")
            data_gouv_parser.export_to_geoparquet(f"{self.__config.export_directory_name}data_gouv.parquet")
            self.data_gouv_geo_data_frame = data_gouv_parser.convert_to_geoDataFrame()
            write_hash_file(f"{self.__config.export_directory_name}data_gouv.hash", self.__config.osm_config["path_file"])
        else:
            print("Data gouv file no change since last process")
            self.__data_gouv_file_no_change = True
            self.osm_parser_geo_data_frame = data_gouv_parser.import_from_geoparquet(f"{self.path_last_execution}data_gouv.parquet")


    def process_transform(self):
        """
        Transforms the parsed data from OSM and Data Gouv sources.

        This method merges the two GeoDataFrames (osm_parser_geo_data_frame and data_gouv_geo_data_frame),
        groups neighboring charging stations, and transforms the data for further processing.
        The transformed data is then exported using the process_export method.

        Raises:
            Exception: If there is an error during the transformation process.
        """
        transformer = Transform()
        print("[ ] - Merge datasources")
        combined_datasource = transformer.merge_datasources(self.osm_parser_geo_data_frame, self.data_gouv_geo_data_frame)
        combined_datasource.to_parquet(f"{self.__config.export_directory_name}combined.parquet")
        print("[x] - Merge datasources")

        print("[ ] - Group neighbors")
        merge_dict = transformer.group_neighbouring(combined_datasource, self.__config.distance)
        print("[x] - Group neighbors")

        print("[ ] - Transform data")
        transformer.transform_data(combined_datasource, merge_dict)
        print("[x] - Transform data")

        self.process_export(transformer)

    def process_export(self, transformer: Transform):
        """
        Exports the transformed data to the specified format.

        This method exports the charging stations and sockets data to the configured export format (SQL, MongoDB, etc.).
        It uses the Transform instance to retrieve the necessary data for exporting.

        Args:
            transformer (Transform): An instance of the Transform class that contains the transformed data.

        Raises:
            Exception: If the specified export type is not implemented.
        """
        print("[ ] - Export files to parquet")
        transformer.export_to_parquet_files(self.__config.export_directory_name)
        print("[x] - Export files to parquet")

        match self.__config.type_export:
            case "sql":
                exporter = SqlExporter(self.__config.sql_config, transformer.get_charging_stations(), transformer.get_sockets())
            case "sql_files":
                exporter = SqlFileExporter(transformer.get_charging_stations(), transformer.get_sockets(), self.__config.export_directory_name)
            case "mongo":
                exporter = MongoExporter(self.__config.mongo_config, transformer.get_charging_stations(), transformer.get_sockets())
            case "mongo_files":
                exporter = MongoFileExporter(transformer.get_charging_stations(), transformer.get_sockets(), self.__config.export_directory_name)
            case _:
                raise Exception(f"{self.__config.type_export} is not implemented, allowed value : sql, sql_files, mongo, mongo_files")
            
        exporter.export()