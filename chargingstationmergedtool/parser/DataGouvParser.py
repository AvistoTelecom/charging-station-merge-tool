from chargingstationmergedtool.parser.CsvParser import CsvParser
from chargingstationmergedtool.Config import Config
from bs4 import BeautifulSoup
import urllib.request
import requests

class DataGouvParser(CsvParser):
    def __init__(self):
        super().__init__()

    def download_datasource(self, config: Config):
        base_url = "https://transport.data.gouv.fr/datasets/fichier-consolide-des-bornes-de-recharge-pour-vehicules-electriques"
        response = requests.get(base_url)

        if response.status_code == 200: 
            soup = BeautifulSoup(response.text, 'html.parser')
            
            try:
                datasource_url = soup.find_all("div", class_="ressources-list")[0].find_all("a", class_="download-button")[0]['href']
                config.data_gouv_config["path_file"] = f"{config.export_directory_name}data_gouv_datasource.csv"

                urllib.request.urlretrieve(datasource_url, config.data_gouv_config["path_file"])
            except:
                raise Exception("Error when parsing data gouv body to retrieve download url")
        else:
            raise Exception(f"Error when retrieve url = {base_url}")

    def parse_file(self, path_file: str):
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