from unittest.mock import patch

import pytest
from shapely.geometry import Point

from chargingstationmergedtool.config import Config
from chargingstationmergedtool.exception import DownloadException
from chargingstationmergedtool.parser import OsmParser


def test_extract_borne():
    osm_parser = OsmParser()

    data_borne_1 = {'amenity': 'charging_station', 'authentication:nfc': 'yes', 'authentication:phone_call': 'yes', 'capacity': '3', 'fee': 'yes', 'motorcar': 'yes', 'name': 'Borne de recharge Saint-Pierre-de-Boeuf', 'network': 'move in pure', 'opening_hours': '24/7', 'operator': 'Freshmile', 'owner': 'CNR', 'parking:fee': 'no', 'ref': 'PUVY, PUKN', 'ref:EU:EVSE': 'FR*CN1*PFXETRZ', 'socket:chademo': '2', 'socket:type2': '2', 'socket:type2_combo': '2'}

    point = Point(4.29184, 44.53852)

    borne_1_chademo = osm_parser.extract_socket_as_borne('socket:chademo', data_borne_1, 22.0, 0, point)
    assert(borne_1_chademo["geometry"]) == point
    assert(borne_1_chademo["power_rated"]) == 22.0
    assert(borne_1_chademo["number_of_sockets"]) == 2
    assert(not borne_1_chademo["socket_type_ef"])
    assert(not borne_1_chademo["socket_type_2"])
    assert(not borne_1_chademo["socket_type_combo_ccs"])
    assert(borne_1_chademo["socket_type_chademo"])
    assert(not borne_1_chademo["socket_type_autre"])

    borne_1_type2 = osm_parser.extract_socket_as_borne('socket:type2', data_borne_1, 22.0, 0, point)
    assert(borne_1_type2["geometry"]) == point
    assert(borne_1_type2["power_rated"]) == 22.0
    assert(borne_1_type2["number_of_sockets"]) == 2
    assert(not borne_1_type2["socket_type_ef"])
    assert(borne_1_type2["socket_type_2"])
    assert(not borne_1_type2["socket_type_combo_ccs"])
    assert(not borne_1_type2["socket_type_chademo"])
    assert(not borne_1_type2["socket_type_autre"])

    data_borne_2 = {'amenity': 'charging_station', 'socket:type2_combo': '2', 'socket:type2_combo:output': '22 kW'}
    borne_2_type2_combo = osm_parser.extract_socket_as_borne('socket:type2_combo', data_borne_2, 3.8, 0, point)
    assert(borne_2_type2_combo["geometry"]) == point
    assert(borne_2_type2_combo["power_rated"]) == 22.0
    assert(borne_2_type2_combo["number_of_sockets"]) == 2
    assert(not borne_2_type2_combo["socket_type_ef"])
    assert(not borne_2_type2_combo["socket_type_2"])
    assert(borne_2_type2_combo["socket_type_combo_ccs"])
    assert(not borne_2_type2_combo["socket_type_chademo"])
    assert(not borne_2_type2_combo["socket_type_autre"])

    data_borne_3 = {'amenity': 'charging_station', 'socket:type2_combo': 'yes', 'socket:type2_combo:output': '22 kW'}
    borne_3_type2_combo = osm_parser.extract_socket_as_borne('socket:type2_combo', data_borne_3, 3.8, 0, point)
    assert(borne_3_type2_combo["number_of_sockets"]) == 1

    data_borne_4 = {'amenity': 'charging_station', 'socket:type2_combo': 'no', 'socket:type2_combo:output': '22 kW'}
    borne_4_type2_combo = osm_parser.extract_socket_as_borne('socket:type2_combo', data_borne_4, 3.8, 0, point)
    assert(borne_4_type2_combo) is None

    data_borne_4 = {'amenity': 'charging_station', 'socket:type2_combo': '22 kW'}
    borne_4_type2_combo = osm_parser.extract_socket_as_borne('socket:type2_combo', data_borne_4, 3.8, 2, point)
    assert(borne_4_type2_combo["number_of_sockets"]) == 2
    assert(borne_4_type2_combo["power_rated"]) == 22.0

def test_extract_bornes():
    osm_parser = OsmParser()

    point = Point(4.29184, 44.53852)

    data_3_sockets = {"geometry": point, "tags": {'amenity': 'charging_station', 'authentication:nfc': 'yes', 'authentication:phone_call': 'yes', 'capacity': '3', 'fee': 'yes', 'motorcar': 'yes', 'name': 'Borne de recharge Saint-Pierre-de-Boeuf', 'network': 'move in pure', 'opening_hours': '24/7', 'operator': 'Freshmile', 'owner': 'CNR', 'parking:fee': 'no', 'ref': 'PUVY, PUKN', 'ref:EU:EVSE': 'FR*CN1*PFXETRZ', 'socket:chademo': '2', 'socket:type2': '2', 'socket:type2_combo': '2'}}
    assert(len(osm_parser.extract_bornes(data_3_sockets))) == 3

    data_0_socket = {"geometry": point, "tags": {'amenity': 'charging_station', 'authentication:nfc': 'yes', 'authentication:phone_call': 'yes', 'capacity': '3', 'fee': 'yes', 'motorcar': 'yes', 'name': 'Borne de recharge Saint-Pierre-de-Boeuf', 'network': 'move in pure', 'opening_hours': '24/7', 'operator': 'Freshmile', 'owner': 'CNR', 'parking:fee': 'no', 'ref': 'PUVY, PUKN', 'ref:EU:EVSE': 'FR*CN1*PFXETRZ'}}
    assert(len(osm_parser.extract_bornes(data_0_socket))) == 0

def test_load_data():
    osm_parser = OsmParser()

    osm_parser.load_pbf("/home/vincent/Projets/Deki/implementations/maps/rhone-alpes-latest.osm.pbf")
    assert len(osm_parser.df) > 0

def test_download_datasource():
    osm_parser = OsmParser()
    config = Config("tests/resources/correct_config_need_to_download.json")

    with patch("urllib.request.urlretrieve") as mock_urlretrieve:
        mock_urlretrieve.return_value.status_code = 200
        
        osm_parser.download_datasource(config)

        assert(config.osm_config["path_file"]) == f"{config.export_directory_name}france-latest.osm.pbf"

    mock_urlretrieve.assert_called_once_with("https://download.geofabrik.de/europe/france-latest.osm.pbf", f"{config.export_directory_name}france-latest.osm.pbf")
    
def test_download_datasource_error():
    osm_parser = OsmParser()
    config = Config("tests/resources/correct_config_need_to_download.json")

    with patch("urllib.request.urlretrieve") as mock_urlretrieve:
        mock_urlretrieve.return_value.status_code = 404

        with pytest.raises(DownloadException, match="Error when retrieving URL = https://download.geofabrik.de/europe/france-latest.osm.pbf"):
            osm_parser.download_datasource(config)
    