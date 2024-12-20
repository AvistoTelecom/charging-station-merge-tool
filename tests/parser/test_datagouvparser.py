from unittest.mock import patch

import pytest

from src.config import Config
from src.exception import (
    DataGouvScrapingException,
    DownloadException,
)
from src.parser import DataGouvParser


def test_download_datasource():
    data_gouv_parser = DataGouvParser()
    config = Config("tests/resources/correct_config_need_to_download.json")

    with patch("requests.get") as requests_mock:
        with open('tests/resources/data_gouv_page.html', 'r') as f:
            requests_mock.return_value.status_code = 200
            requests_mock.return_value.text = f.read()

        with patch("urllib.request.urlretrieve") as urlretrieve_mock:
            data_gouv_parser.download_datasource(config)

            assert(config.data_gouv_config["path_file"]) == f"{config.export_directory_name}data_gouv_datasource.csv"

        urlretrieve_mock.assert_called_once_with("https://www.data.gouv.fr/fr/datasets/r/eb76d20a-8501-400e-b336-d85724de5435", f"{config.export_directory_name}data_gouv_datasource.csv")

def test_download_datasource_error():
    data_gouv_parser = DataGouvParser()
    config = Config("tests/resources/correct_config_need_to_download.json")

    with patch("requests.get") as requests_mock:
        requests_mock.return_value.status_code = 404

        with pytest.raises(DownloadException, match="Error when retrieving URL = https://transport.data.gouv.fr/datasets/fichier-consolide-des-bornes-de-recharge-pour-vehicules-electriques"):
            data_gouv_parser.download_datasource(config)

def test_download_datasource_error_retrieve_url():
    data_gouv_parser = DataGouvParser()
    config = Config("tests/resources/correct_config_need_to_download.json")

    with patch("requests.get") as requests_mock:
        requests_mock.return_value.status_code = 200
        requests_mock.return_value.text = ""

        with pytest.raises(DataGouvScrapingException, match="Error when parsing Data Gouv body to retrieve download URL"):
            data_gouv_parser.download_datasource(config)