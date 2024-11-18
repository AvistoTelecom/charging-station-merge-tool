import quackosm as qosm
import urllib.request
import pandas as pd
import os
from shapely.geometry import Point

from chargingstationmergedtool.AbstractParser import AbstractParser
from chargingstationmergedtool.Config import Config
from chargingstationmergedtool.utils import is_power_rated_data, is_int_data, extract_power_rated

class OsmParser(AbstractParser):
    def __init__(self):
        super().__init__()

    def download_datasource(self, config: Config):
        datasource_url = "https://download.geofabrik.de/europe/france-latest.osm.pbf"

        config.osm_config["path_file"] = f"{config.export_directory_name}france-latest.osm.pbf"

        urllib.request.urlretrieve(datasource_url, config.osm_config["path_file"])

    def load_pbf(self, path_pbf):
        if os.path.exists(path_pbf):
            data = qosm.convert_pbf_to_geodataframe(path_pbf, tags_filter={"amenity": "charging_station", "way": False}, keep_all_tags=True)

            for index in range(len(data)):
                row = data.iloc[index]
                for borne in self.extract_bornes(row):
                    self.add_borne(borne)
        else:
            raise Exception("PBF file not found")

    def extract_bornes(self, data_borne: pd.DataFrame) -> list[dict]:
        geometry = data_borne['geometry']
        tags = data_borne['tags']

        bornes = list()

        if 'charging_station:output' in tags.keys():
            default_rated_power = extract_power_rated(tags['charging_station:output'])
        else:
            default_rated_power = None

        if 'capacity' in tags.keys():
            default_capacity = int(tags['capacity'])
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
            "retrive_from": "OSM"
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