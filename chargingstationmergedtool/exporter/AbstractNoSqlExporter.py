import pandas as pd

class AbstractNoSqlExporter:
    def __init__(self, charging_stations: pd.DataFrame, sockets: pd.DataFrame):
        self.__charging_stations = charging_stations
        self.__sockets = sockets

    def transform_data_to_dict(self) -> list[dict]:
        results = list()

        for _, row in self.__charging_stations.iterrows():
            id = row['id']
            results.append({
                "id": id,
                "latitude": row['geometry'].y,
                "longitude": row['geometry'].x,
                "sockets": self.extract_sockets(id)
            })

        return results
    
    def extract_sockets(self, charging_station_id: int) -> list[dict]:
        results = list()

        for _, row in self.__sockets[self.__sockets['charging_station_id'] == charging_station_id].iterrows():
            results.append({
                "id": row['id'],
                "latitude": row['geometry'].y,
                "longitude": row['geometry'].x,
                "power_rated": row['power_rated'],
                "number_of_sockets": row['number_of_sockets'],
                "socket_type_ef": row['socket_type_ef'],
                "socket_type_2": row['socket_type_2'],
                "socket_type_combo_ccs": row['socket_type_combo_ccs'],
                "socket_type_chademo": row['socket_type_chademo'],
                "socket_type_autre": row['socket_type_autre'],
                "id_itinerance": row['id_itinerance'],
                "retrieve_from": row['retrieve_from']
            })

        return results