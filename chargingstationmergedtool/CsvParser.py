from chargingstationmergedtool.AbstractParser import AbstractParser
from shapely.geometry import Point
import csv
import os
from chargingstationmergedtool.utils import extract_power_rated

class CsvParser(AbstractParser):
    def __init__(self):
        super().__init__()

    def parse_csv_file(self, path_file: str, mapping_dictionnary: dict):
        if os.path.exists(path_file):
            with open(path_file, 'r') as f:
                lines = csv.DictReader(f)

                for line in lines:
                    borne = self.transform_line_to_borne(line, mapping_dictionnary)
                    self.add_borne(borne)
        else:
            raise Exception("CSV file not found")
        

    def transform_line_to_borne(self, line: list[str], mapping_with_index: dict) -> dict:
        longitude = float(line[mapping_with_index['longitude']])
        latitude = float(line[mapping_with_index['latitude']])

        point = Point(longitude, latitude)
        borne = {
            "geometry": point,
            'power_rated': extract_power_rated(line[mapping_with_index['power_rated']]),
            'number_of_sockets': int(line[mapping_with_index['number_of_sockets']]),
            'socket_type_ef': self.parse_bool(line[mapping_with_index['socket_type_ef']]),
            'socket_type_2': self.parse_bool(line[mapping_with_index['socket_type_2']]),
            'socket_type_combo_ccs': self.parse_bool(line[mapping_with_index['socket_type_combo_ccs']]),
            'socket_type_chademo': self.parse_bool(line[mapping_with_index['socket_type_chademo']]),
            'socket_type_autre': self.parse_bool(line[mapping_with_index['socket_type_autre']]),
            'id_itinerance': line[mapping_with_index['id_pdc_itinerance']],
            'retrive_from': mapping_with_index['retrive_from']
        }

        return borne

    def parse_bool(self, value: str) -> bool:
        if value.upper() == "TRUE" or value == '1':
            return True
        elif value.upper() == "FALSE" or value == '0':
            return False
        else:
            return None