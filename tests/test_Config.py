from chargingstationmergedtool.Config import Config
import pytest

def test_correct_config_file():
    config = Config("tests/ressources/correct_config_need_to_download.json")

    assert(config.distance) == 1500
    assert(config.export_directory_name) is not None
    assert(config.osm_config["need_to_download"])
    assert(config.data_gouv_config["need_to_download"])

def test_correct_config_file_files_already_exists():
    config = Config("tests/ressources/correct_config_datasource_already_exists.json")

    assert(config.distance) == 1500
    assert(config.export_directory_name) is not None
    assert(not config.osm_config["need_to_download"])
    assert(config.osm_config["path_file"]) == "test.pbf"
    assert(not config.data_gouv_config["need_to_download"])
    assert(config.data_gouv_config["path_file"]) == "test/ressources/consolidation-etalab-schema-irve-statique-v-2.3.1-20241113.csv"

def test_common_block_missing():
    with pytest.raises(Exception, match="'common' block not found in config file") as e:
        Config("tests/ressources/incorrect_config.json")

def test_file_not_found():
    with pytest.raises(Exception, match="Config file not found") as e:
        Config("tests/ressources/incorrect.json")

def test_key_missing():
    with pytest.raises(Exception, match="distance key not in common block") as e:
        Config("tests/ressources/incorrect_config2.json")