from chargingstationmergedtool.CsvParser import CsvParser

class DataGouvParser(CsvParser):
    def __init__(self):
        super().__init__()

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
            'socket_type_autre': 'prise_type_autre'
        }

        self.parse_csv_file(path_file, mapping_dictionnary)