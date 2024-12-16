"""
CsvParser Module

This module provides a class for parsing charging station data from CSV files.
It extends the AbstractParser class and implements specific logic for handling CSV data.

Classes:
    CsvParser: A class to handle the parsing of charging station data from CSV files.

Usage:
    To use this class, create an instance of CsvParser and call the parse_csv_file method
    with the path to the CSV file and a mapping dictionary to extract the relevant fields.

Example:
    parser = CsvParser()
    mapping = {
        'longitude': 0,
        'latitude': 1,
        'power_rated': 2,
        'number_of_sockets': 3,
        'socket_type_ef': 4,
        'socket_type_2': 5,
        'socket_type_combo_ccs': 6,
        'socket_type_chademo': 7,
        'socket_type_autre': 8,
        'id_pdc_itinerance': 9,
        'retrieve_from': 10
    }
    parser.parse_csv_file('path/to/file.csv', mapping)

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
from chargingstationmergedtool.parser.AbstractParser import AbstractParser
from shapely.geometry import Point
import csv
import os
from chargingstationmergedtool.utils import extract_power_rated

class CsvParser(AbstractParser):
    """
    A class to handle the parsing of charging station data from CSV files.

    Inherits from AbstractParser and implements methods for reading CSV files
    and transforming the data into a suitable format for further processing.
    """
    def __init__(self):
        """
        Initializes the CsvParser by calling the parent constructor.
        """
        super().__init__()

    def parse_csv_file(self, path_file: str, mapping_dictionnary: dict):
        """
        Parses a CSV file and adds the records to the DataFrame.

        This method reads the specified CSV file, transforms each line into a record,
        and adds it to the internal DataFrame.

        Args:
            path_file (str): The path to the CSV file to be parsed.
            mapping_dictionnary (dict): A dictionary mapping column names to their indices.

        Raises:
            Exception: If the specified CSV file does not exist.
        """
        if os.path.exists(path_file):
            with open(path_file, 'r') as f:
                lines = csv.DictReader(f)

                for line in lines:
                    borne = self.transform_line_to_borne(line, mapping_dictionnary)
                    self.add_borne(borne)
        else:
            raise Exception("CSV file not found")
        

    def transform_line_to_borne(self, line: list[str], mapping_with_index: dict) -> dict:
        """
        Transforms a line from the CSV file into a record.

        This method extracts the relevant fields from the line and creates a dictionary
        representing a charging station record.

        Args:
            line (dict): A dictionary representing a single line from the CSV file.
            mapping_with_index (dict): A dictionary mapping field names to their indices.

        Returns:
            dict: A dictionary representing the charging station record.
        """
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
            'retrieve_from': mapping_with_index['retrieve_from']
        }

        return borne

    def parse_bool(self, value: str) -> bool:
        """
        Parses a string value into a boolean.

        This method converts string representations of boolean values ("TRUE", "FALSE", "1", "0")
        into Python boolean values (True, False).

        Args:
            value (str): The string value to be parsed.

        Returns:
            bool: The corresponding boolean value, or None if the value is not recognized.
        """
        if value.upper() == "TRUE" or value == '1':
            return True
        elif value.upper() == "FALSE" or value == '0':
            return False
        else:
            return None