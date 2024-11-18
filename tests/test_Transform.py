from chargingstationmergedtool.Transform import Transform
from shapely.geometry import Point
import geopandas as gpd
import uuid

def test_append_charging_station_to_charging_station_dataframe():
    transform = Transform()

    charging_station = {
        "id": 1,
        "geometry": Point(45.0, 0.0)
    }

    charging_station2 = {
        "id": 2,
        "geometry": Point(45.0, 0.0)
    }

    assert(transform.get_charging_stations()) is None
    transform.append_charging_station_to_charging_station_dataframe(charging_station)
    assert(len(transform.get_charging_stations())) == 1
    transform.append_charging_station_to_charging_station_dataframe(charging_station2)
    assert(len(transform.get_charging_stations())) == 2

def test_append_socket_to_sockets_dataframe():
    transform = Transform()

    socket1 = {
            "id": uuid.uuid4(),
            "power_rated": 22.0,
            "number_of_sockets": 2,
            "socket_type_ef": False,
            "socket_type_2": True,
            "socket_type_combo_ccs": False,
            "socket_type_chademo": False,
            "socket_type_autre": False,
            "charging_station_index": 1
        }

    socket2 = {
            "id": uuid.uuid4(),
            "power_rated": 3.8,
            "number_of_sockets": 1,
            "socket_type_ef": False,
            "socket_type_2": True,
            "socket_type_combo_ccs": False,
            "socket_type_chademo": False,
            "socket_type_autre": False,
            "charging_station_index": 1
        }

    socket_duplicate = {
            "id": uuid.uuid4(),
            "power_rated": 3.8,
            "number_of_sockets": 2,
            "socket_type_ef": False,
            "socket_type_2": True,
            "socket_type_combo_ccs": False,
            "socket_type_chademo": False,
            "socket_type_autre": False,
            "charging_station_index": 1
        }

    assert(transform.get_sockets()) is None

    transform.append_socket_to_sockets_dataframe(socket1)
    assert(len(transform.get_sockets())) == 1
    transform.append_socket_to_sockets_dataframe(socket2)
    assert(len(transform.get_sockets())) == 2
    transform.append_socket_to_sockets_dataframe(socket_duplicate)
    assert(len(transform.get_sockets())) == 2


def test_merge_datasources():
    transform = Transform()

    datasource1 = gpd.GeoDataFrame({
        'id': [1, 2],
        'geometry': [Point(1, 1), Point(2, 2)]
    }, crs="EPSG:4326")

    datasource2 = gpd.GeoDataFrame({
        'id': [3, 4],
        'geometry': [Point(3, 3), Point(4, 4)]
    }, crs="EPSG:4326")

    merged = transform.merge_datasources(datasource1, datasource2)

    assert(isinstance(merged, gpd.GeoDataFrame))
    assert(len(merged)) == 4
    assert(list(merged['id'])) == [1, 2, 3, 4]
    assert(list(merged['geometry'])) == [Point(1, 1), Point(2, 2), Point(3, 3), Point(4, 4)]

def test_transform_to_charging_station():
    transform = Transform()
    socket = {
        "power_rated": 22.0,
        "geometry": Point(1, 1),
        "number_of_sockets": 2,
        "socket_type_ef": False,
        "socket_type_2": True,
        "socket_type_combo_ccs": False,
        "socket_type_chademo": False,
        "socket_type_autre": False
    }
    
    charging_station = transform.transform_to_charging_station(1, socket)
    assert(charging_station["geometry"]) == Point(1, 1)
    assert(charging_station["id"]) == 1

def test_transform_to_socket():
    transform = Transform()
    socket = {
        "power_rated": 22.0,
        "geometry": Point(1, 1),
        "number_of_sockets": 2,
        "socket_type_ef": False,
        "socket_type_2": True,
        "socket_type_combo_ccs": False,
        "socket_type_chademo": False,
        "socket_type_autre": False,
        "id_itinerance": 125,
        "retrive_from": "OSM"
    }
    
    socket_formatted = transform.transform_to_socket(1, socket)
    assert(socket_formatted["id"]) is not None
    assert(socket_formatted["geometry"]) == Point(1, 1)
    assert(socket_formatted["power_rated"]) == 22.0
    assert(socket_formatted["number_of_sockets"]) == 2
    assert(socket_formatted["socket_type_ef"]) == False
    assert(socket_formatted["socket_type_2"]) == True
    assert(socket_formatted["socket_type_combo_ccs"]) == False
    assert(socket_formatted["socket_type_chademo"]) == False
    assert(socket_formatted["socket_type_autre"]) == False
    assert(socket_formatted["id_itinerance"]) == 125
    assert(socket_formatted["retrive_from"]) == "OSM"
    assert(socket_formatted["charging_station_index"]) == 1

def test_append_charging_station_to_charging_station_dataframe():
    transform = Transform()
    charging_station1 = {
        "id": 1,
        "geometry": Point(1, 1),
    }
    charging_station2 = {
        "id": 2,
        "geometry": Point(2, 2),
    }

    transform.append_charging_station_to_charging_station_dataframe(charging_station1)
    assert(len(transform.get_charging_stations())) == 1

    transform.append_charging_station_to_charging_station_dataframe(charging_station2)
    assert(len(transform.get_charging_stations())) == 2

def test_transform_data():
    transform = Transform()

    datasource = gpd.GeoDataFrame({
        'geometry': [Point(1, 1), Point(2, 2), Point(3, 3), Point(4, 4), Point(5, 5)],
        'power_rated': [22.0, 305.0, 3.8, 50.0, 105.0],
        'number_of_sockets': [1, 2, 3, 4, 5],
        'socket_type_ef': [True, False, False, False, False],
        'socket_type_2': [False, True, False, False, False],
        'socket_type_combo_ccs': [False, False, True, False, False],
        'socket_type_chademo': [False, False, False, True, False],
        'socket_type_autre': [False, False, False, False, True],
        'id_itinerance': ["iti1", "iti2", "iti3", "iti4", "iti5"],
        'retrive_from': ["OSM", "OSM", "DATA_GOUV", "DATA_GOUV", "DATA_GOUV"]
    }, crs="EPSG:4326")

    merge_dict = {
        0: [1, 2],
        3: [],
        4: []
    }

    transform.transform_data(datasource, merge_dict)

    assert(len(transform.get_charging_stations())) == 3
    assert(len(transform.get_sockets())) == 5

    assert(list(transform.get_charging_stations()['id'])) ==  [0, 3, 4]
    assert(list(transform.get_sockets()['charging_station_index'])) ==  [0, 0, 0, 3, 4]

def test_group_neighbouring():
    transform = Transform()
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
    gdf = gpd.GeoDataFrame({
        'geometry': points,
        'power_rated': [22.0, 305.0, 3.8, 50.0, 105.0, 200.0, 150.0, 75.0, 120.0, 60.0],
        'number_of_sockets': [1, 2, 3, 4, 5, 2, 3, 1, 4, 2],
        'socket_type_ef': [True, False, False, False, False, True, False, False, True, False],
        'socket_type_2': [False, True, False, False, False, False, True, False, False, True],
        'socket_type_combo_ccs': [False, False, True, False, False, False, False, True, False, False],
        'socket_type_chademo': [False, False, False, True, False, False, False, False, True, False],
        'socket_type_autre': [False, False, False, False, True, False, False, False, False, True],
        'id_itinerance': [f"iti{i+1}" for i in range(10)],
        'retrive_from': ["OSM", "OSM", "DATA_GOUV", "DATA_GOUV", "DATA_GOUV", "OSM", "DATA_GOUV", "OSM", "DATA_GOUV", "OSM"]
    }, crs="EPSG:4326")

    merge_dict = transform.group_neighbouring(gdf, 1500)

    merge_dict_expected = {
        0: [1, 2, 3],
        4: [],
        5: [],
        6: [],
        7: [],
        8: [],
        9: [],
    }

    assert(merge_dict) == merge_dict_expected