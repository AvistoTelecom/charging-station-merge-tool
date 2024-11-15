from chargingstationmergedtool.CsvParser import CsvParser
from shapely.geometry import Point

# def test_transform_line_to_borne():
#     mapping_dictionnary = {
#             'longitude': 'consolidated_longitude',
#             'latitude': 'consolidated_latitude',
#             'power_rated': 'puissance_nominale',
#             'number_of_sockets': 'nbre_pdc',
#             'socket_type_ef': 'prise_type_ef',
#             'socket_type_2': 'prise_type_2',
#             'socket_type_combo_ccs': 'prise_type_combo_ccs',
#             'socket_type_chademo': 'prise_type_chademo',
#             'socket_type_autre': 'prise_type_autre'
#         }

#     line = ['Grupo Easycharger', '', '', 'Zunder | ES*ZUN,roaming@zunder.com', '', 'Zunder', 'ESZUNP5074587027866670894', '863358', 'Zunder/74654', 'Station dédiée à la recharge rapide', '"  D924, Aire du Pays d’Argentan, Écouché-les-Vallées  61200  France"', '', '" [-0.056488 , 48.723084] "', '12', 'ESZUNE1111ER1', '2231424', '300', 'False', 'False', 'True', 'False', 'False', 'False', 'False', '', 'True', '', 'Accès libre', 'False', '24/7', 'Accessibilité inconnue', 'Restriction de gabarit non précisée', 'False', '', '', '', '', '2024-10-25', 'False', '2024-11-01T03:01:21+00:00', '63dccb1307e9b2f213a5130c', '61387a4e-22f7-4662-b241-d5cac4dd91fd', 'gireve-2', '2023-03-24T14:32:54.036000+00:00', '-0.056488', '48.723084', '', '', 'False', 'False']

#     csv_parser = CsvParser()
#     borne = csv_parser.transform_line_to_borne(line, mapping_dictionnary)
#     assert(borne) == {
#             "geometry": Point(48.723084, -0.056488),
#             'power_rated': 300,
#             'number_of_sockets': 12,
#             'socket_type_ef': False,
#             'socket_type_2': False,
#             'socket_type_combo_ccs': True,
#             'socket_type_chademo': False,
#             'socket_type_autre': False
#         }