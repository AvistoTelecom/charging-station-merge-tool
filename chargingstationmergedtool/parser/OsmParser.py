"""
Module: OsmParser

This module provides the OsmParser class, which is responsible for downloading,
filtering, and loading OpenStreetMap (OSM) data related to charging stations.

Imports:
    - quackosm as qosm
    - urllib.request
    - pandas as pd
    - os
    - subprocess
    - shapely.geometry.Point
    - shlex
    - chargingstationmergedtool.parser.AbstractParser
    - chargingstationmergedtool.Config
    - chargingstationmergedtool.utils

Classes:
    - OsmParser

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
import quackosm as qosm
import urllib.request
import pandas as pd
import os
import subprocess
from shapely.geometry import Point
import shlex

from chargingstationmergedtool.parser.AbstractParser import AbstractParser
from chargingstationmergedtool.Config import Config
from chargingstationmergedtool.utils import is_power_rated_data, is_int_data, extract_power_rated

class OsmParser(AbstractParser):
    """
    A parser for OpenStreetMap data related to charging stations.

    Inherits from AbstractParser.
    """
    def __init__(self):
        """
        Initializes the OsmParser instance.
        """
        super().__init__()

    def download_datasource(self, config: Config):
        """
        Downloads the OSM data source for France and saves it to the specified path.

        Parameters:
            config (Config): The configuration object containing export directory information.
        """
        datasource_url = "https://download.geofabrik.de/europe/france-latest.osm.pbf"

        config.osm_config["path_file"] = f"{config.export_directory_name}france-latest.osm.pbf"

        urllib.request.urlretrieve(datasource_url, config.osm_config["path_file"])

    def filtering_with_osmosis(self, path_intput_pbf: str, path_output_pbf: str):
        """
        Filters the input PBF file using Osmosis to retain only charging station nodes.

        Parameters:
            path_intput_pbf (str): The path to the input PBF file.
            path_output_pbf (str): The path to save the filtered output PBF file.

        Raises:
            Exception: If the input PBF file does not exist.
        """
        if os.path.exists(path_intput_pbf):
            subprocess.run([
                '/usr/bin/osmosis',
                '--read-pbf',
                path_intput_pbf,
                '--tf',
                'reject-relations',
                '--tf',
                'reject-ways',
                '--tf',
                'accept-nodes',
                'amenity=charging_station',
                '--write-pbf',
                path_output_pbf
            ], check=True)
        else:
            raise Exception("PBF file not found")

    def load_pbf(self, path_pbf):
        """
        Loads the PBF file and extracts charging station data.

        Parameters:
            path_pbf (str): The path to the PBF file.

        Raises:
            Exception: If the PBF file does not exist.
        """
        if os.path.exists(path_pbf):
            data = qosm.convert_pbf_to_geodataframe(path_pbf, tags_filter={"amenity": "charging_station", "way": False}, keep_all_tags=True)

            for index in range(len(data)):
                row = data.iloc[index]
                for borne in self.extract_bornes(row):
                    self.add_borne(borne)
        else:
            raise Exception("PBF file not found")

    def extract_bornes(self, data_borne: pd.DataFrame) -> list[dict]:
        """
        Extracts charging station information from the given data.

        Parameters:
            data_borne (pd.DataFrame): The DataFrame containing charging station data.

        Returns:
            list[dict]: A list of dictionaries containing information about each charging station.
        """
        geometry = data_borne['geometry']
        tags = data_borne['tags']

        bornes = list()

        if 'charging_station:output' in tags.keys():
            default_rated_power = extract_power_rated(tags['charging_station:output'])
        else:
            default_rated_power = None

        if 'capacity' in tags.keys():
            try:
                default_capacity = int(tags['capacity'])
            except ValueError:
                default_capacity = None
        else:
            default_capacity = None

        type_sockets = [
            'socket:type2_combo',
            'socket:type2',
            'socket:type2_cable',
            'socket:chademo',
            'socket:typee',
            'socket:type3c'
        ]

        for type_socket in type_sockets:
            if type_socket in tags.keys():
                borne = self.extract_socket_as_borne(type_socket, tags, default_rated_power, default_capacity, geometry)
                if borne is not None:
                    bornes.append(borne)

        return bornes

    def extract_socket_as_borne(self, type_socket: str, data: dict, default_power_rated: float, default_capacity: int, geometry: Point) -> dict:
        """
        Extracts information about a specific type of socket and returns it as a dictionary.

        Parameters:
            type_socket (str): The type of socket (e.g., 'socket:type2', 'socket:chademo').
            data (dict): The dictionary containing the tags associated with the charging station.
            default_power_rated (float): The default power rating for the charging station.
            default_capacity (int): The default capacity of the charging station.
            geometry (Point): The geometry point representing the location of the charging station.

        Returns:
            dict: A dictionary containing information about the socket, including geometry, power rating,
                  number of sockets, and other relevant details. Returns None if the socket is not available.
        """
        number_of_sockets = data[type_socket]
        if number_of_sockets == "no":
            return None
        elif number_of_sockets == "yes":
            number_of_sockets = 1
        elif is_power_rated_data(number_of_sockets):
            default_power_rated = extract_power_rated(number_of_sockets)
            number_of_sockets = default_capacity
        elif not is_int_data(number_of_sockets):
            return None

        borne = {
            "geometry": geometry,
            "power_rated": default_power_rated,
            "number_of_sockets": int(number_of_sockets),
            "retrieve_from": "OSM"
        }

        if 'ref:EU:EVSE' in data.keys():
            borne['id_itinerance'] = data['ref:EU:EVSE'].replace('*', '')

        if type_socket + ':output' in data.keys() and is_power_rated_data(data[type_socket + ':output']):
            borne["power_rated"] = extract_power_rated(data[type_socket + ':output'])

        borne["socket_type_ef"] = type_socket == 'socket:typee'
        borne["socket_type_2"] = (type_socket == 'socket:type2' or type_socket == 'socket:type2_cable')
        borne["socket_type_combo_ccs"] = type_socket == 'socket:type2_combo'
        borne["socket_type_chademo"] = type_socket == 'socket:chademo'
        borne["socket_type_autre"] = not (borne["socket_type_ef"] or borne["socket_type_2"] or borne["socket_type_combo_ccs"] or borne["socket_type_chademo"])
        
        return borne