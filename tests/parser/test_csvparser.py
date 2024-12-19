from chargingstationmergedtool.parser import CsvParser
from shapely.geometry import Point
import json

def test_transform_line_to_borne():
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
            'retrieve_from': 'data_gouv',
        }

    with open('tests/resources/line_data_gouv.json', 'r') as f:
        line = json.load(f)
    csv_parser = CsvParser()
    borne = csv_parser.transform_line_to_borne(line, mapping_dictionnary)
    assert(borne) == {
            "geometry": Point(-0.056488, 48.723084),
            'power_rated': 300,
            'number_of_sockets': 12,
            'socket_type_ef': False,
            'socket_type_2': False,
            'socket_type_combo_ccs': True,
            'socket_type_chademo': False,
            'socket_type_autre': False,
            'id_itinerance': 'ESZUNE1111ER1',
            'retrieve_from': 'data_gouv',
        }