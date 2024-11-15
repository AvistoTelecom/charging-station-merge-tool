from chargingstationmergedtool.Transform import Transform
from shapely.geometry import Point
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