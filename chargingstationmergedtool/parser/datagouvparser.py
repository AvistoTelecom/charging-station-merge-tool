"""
DataGouvParser Module

This module provides a class for parsing charging station data from the Data Gouv platform.
It extends the CsvParser class and implements specific logic for downloading and parsing Data Gouv CSV files.

Classes:
    DataGouvParser: A class to handle the downloading and parsing of charging station data from Data Gouv.

Usage:
    To use this class, create an instance of DataGouvParser and call the download_datasource method
    to download the CSV file, followed by the parse_file method to process the data.

Example:
    parser = DataGouvParser()
    config = Config('path/to/config/file')
    parser.download_datasource(config)
    parser.parse_file(config.data_gouv_config["path_file"])

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

import urllib.request

import requests
from bs4 import BeautifulSoup

from chargingstationmergedtool.config import Config
from chargingstationmergedtool.parser.csvparser import CsvParser
from chargingstationmergedtool.exception import DownloadException, DataGouvScrapingException


class DataGouvParser(CsvParser):
    """
    A class to handle the downloading and parsing of charging station data from Data Gouv.

    Inherits from CsvParser and implements methods for downloading the data source
    and parsing the CSV file into a suitable format for further processing.
    """

    def __init__(self):
        """
        Initializes the DataGouvParser by calling the parent constructor.
        """
        super().__init__()

    def download_datasource(self, config: Config):
        """
        Downloads the charging station data source from the Data Gouv website.

        This method retrieves the URL of the CSV file containing the charging station data
        and saves it to the specified path in the configuration.

        Args:
            config (Config): The configuration object containing export directory and path information.

        Raises:
            Exception: If there is an error retrieving the data source URL or downloading the file.
        """
        base_url = "https://transport.data.gouv.fr/datasets/fichier-consolide-des-bornes-de-recharge-pour-vehicules-electriques"
        response = requests.get(base_url)

        if response.status_code == 200: 
            soup = BeautifulSoup(response.text, 'html.parser')
            
            try:
                datasource_url = soup.find_all("div", class_="ressources-list")[0].find_all("a", class_="download-button")[0]['href']
                config.data_gouv_config["path_file"] = f"{config.export_directory_name}data_gouv_datasource.csv"

                urllib.request.urlretrieve(datasource_url, config.data_gouv_config["path_file"])
            except Exception as e:
                raise DataGouvScrapingException("Error when parsing Data Gouv body to retrieve download URL") from e
        else:
            raise DownloadException(f"Error when retrieving URL = {base_url}")

    def parse_file(self, path_file: str):
        """
        Parses the downloaded CSV file and adds the records to the DataFrame.

        This method uses a mapping dictionary to extract relevant fields from the CSV file
        and adds them to the internal DataFrame.

        Args:
            path_file (str): The path to the CSV file to be parsed.
        """
        mapping_dictionnary = {
            'longitude': 'consolidated_longitude',
            'latitude': 'consolidated_latitude',
            'power_rated': 'puissance_nominale',
            'number_of_sockets': 'nbre_pdc',
            'socket_type_ef': 'prise_type_ef',
            'socket_type_2': 'prise_type_2',
            'socket_type_combo_ccs': 'prise_type_combo_ccs',
            'socket_type_chademo': 'prise_type_chademo',
            'socket_type_autre': 'prise_type_autre',
            'id_pdc_itinerance': 'id_pdc_itinerance',
            'retrieve_from': 'data_gouv'
        }

        self.parse_csv_file(path_file, mapping_dictionnary)
