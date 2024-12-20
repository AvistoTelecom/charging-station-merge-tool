import pytest

from src.config import Config
from src.exception import ConfigParsingException


def test_correct_config_file():
    config = Config("tests/resources/correct_config_need_to_download.json")

    sql_config_expected = {
        "connection_url": "connection_url",
        "charging_stations_table_name": "sql_charging_stations_table_name",
        "sockets_table_name": "sql_sockets_table_name"
    }

    mongo_config_expected = {
        "connection_url": "connection_url",
        "database_name": "database_name",
        "charging_stations_collection_name": "mongo_charging_stations_collection_name"
    }

    assert(config.distance) == 1500
    assert(config.export_directory_name) is not None
    assert(config.osm_config["need_to_download"])
    assert(config.data_gouv_config["need_to_download"])
    assert(config.sql_config) == sql_config_expected
    assert(config.mongo_config) == mongo_config_expected

def test_correct_config_file_files_already_exists():
    config = Config("tests/resources/correct_config_datasource_already_exists.json")

    assert(config.distance) == 1500
    assert(config.export_directory_name) is not None
    assert(not config.osm_config["need_to_download"])
    assert(config.osm_config["path_file"]) == "test.pbf"
    assert(not config.data_gouv_config["need_to_download"])
    assert(config.data_gouv_config["path_file"]) == "test/ressources/consolidation-etalab-schema-irve-statique-v-2.3.1-20241113.csv"

def test_common_block_missing():
    with pytest.raises(ConfigParsingException, match="'common' block not found in config file"):
        Config("tests/resources/incorrect_config.json")

def test_file_not_found():
    with pytest.raises(FileNotFoundError, match="Config file not found"):
        Config("tests/resources/incorrect.json")

def test_key_missing():
    with pytest.raises(ConfigParsingException, match="distance key not in common block"):
        Config("tests/resources/incorrect_config2.json")