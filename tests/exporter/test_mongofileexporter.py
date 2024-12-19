from chargingstationmergedtool.exporter import MongoFileExporter
import pandas as pd
from shapely.geometry import Point
import tempfile
import os

def test_export():
    with tempfile.TemporaryDirectory() as tmp_dir_name:
        charging_stations = pd.DataFrame({
            'id': [0, 1],
            'geometry': [Point(-61.72048, 15.999102), Point(-61.605293, 16.20394)]
        })

        points = [
            Point(2.3522, 48.8566),  # Notre-Dame de Paris
            Point(2.3444, 48.8554),  # Sainte-Chapelle
            Point(2.3442, 48.8550),  # Conciergerie
            Point(2.3500, 48.8555),  # Pont Saint-Louis
            Point(2.3600, 48.8420),  # Jardin des Plantes
            Point(2.2945, 48.8584),  # Tour Eiffel
            Point(2.3376, 48.8606),  # Louvre
            Point(2.3614, 48.8660),  # Opéra Garnier
            Point(2.2699, 48.8848),  # Montmartre
            Point(2.3300, 48.8738)   # Place de la Concorde
        ]

        # Création du GeoDataFrame
        sockets = pd.DataFrame({
            'id': [f"test{i+1}" for i in range(10)],
            'geometry': points,
            'power_rated': [22.0, 305.0, 3.8, 50.0, 105.0, 200.0, 150.0, 75.0, 120.0, 60.0],
            'number_of_sockets': [1, 2, 3, 4, 5, 2, 3, 1, 4, 2],
            'socket_type_ef': [True, False, False, False, False, True, False, False, True, False],
            'socket_type_2': [False, True, False, False, False, False, True, False, False, True],
            'socket_type_combo_ccs': [False, False, True, False, False, False, False, True, False, False],
            'socket_type_chademo': [False, False, False, True, False, False, False, False, True, False],
            'socket_type_autre': [False, False, False, False, True, False, False, False, False, True],
            'id_itinerance': [f"iti{i+1}" for i in range(10)],
            'charging_station_id': [0, 0, 0, 1, 1, 1, 1, 0, 0, 2],
            'retrieve_from': ["OSM", "OSM", "DATA_GOUV", "DATA_GOUV", "DATA_GOUV", "OSM", "DATA_GOUV", "OSM", "DATA_GOUV", "OSM"]
        })

        exporter = MongoFileExporter(charging_stations, sockets, tmp_dir_name)
        exporter.export()

        assert(len(os.listdir(tmp_dir_name))) == 2