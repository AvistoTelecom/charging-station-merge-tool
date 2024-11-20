import geopandas as gpd
import pandas as pd
import numpy as np
import uuid
from chargingstationmergedtool.utils import to_geo_dataframe

class Transform:
    def __init__(self):
        self.__charging_stations = None
        self.__sockets = None

    def get_charging_stations(self):
        return self.__charging_stations

    def get_sockets(self):
        return self.__sockets

    def merge_datasources(self, datasource1: gpd.GeoDataFrame, datasource2: gpd.GeoDataFrame) -> gpd.GeoDataFrame:
        return gpd.GeoDataFrame(pd.concat([datasource1, datasource2]), geometry='geometry', crs="EPSG:4326")
    
    def group_neighbouring(self, datasource: gpd.GeoDataFrame, distance_to_merge: int) -> dict:
        # Supposons que combined_geo_data_frame soit déjà défini
        geometries = datasource['geometry'].to_list()

        # Convertir toutes les géométries en GeoDataFrame une seule fois
        gdf = gpd.GeoDataFrame({'geometry': geometries}, crs='EPSG:4326')
        gdf = gdf.to_crs('EPSG:5234')

        # Extraire les index et les géométries en tant que tableaux NumPy
        index = gdf.index.to_numpy()  # Convertir les index en tableau NumPy
        length = len(index)  # Longueur des index
        index_already_merged = set()  # Ensemble pour suivre les index déjà fusionnés
        merge_dict = {}  # Dictionnaire pour stocker les résultats de fusion

        for index1 in range(length):
            if index1 not in index_already_merged:
                print(f"current index1 = {index1}")
                index_already_merged.add(index1)
                merge_dict[index1] = list()
                point1 = gdf.geometry[index1]

                # Calculer les distances pour tous les points en une seule opération
                distances = gdf.distance(point1)

                # Utiliser un masque pour trouver les index à ajouter
                mask = (distances < distance_to_merge) & (index != index1) & (~np.isin(index, list(index_already_merged)))

                # Ajouter les index correspondants au dictionnaire de fusion
                merge_dict[index1].extend(index[mask].tolist())
                
                # Mettre à jour l'ensemble des index déjà fusionnés
                index_already_merged.update(index[mask])

        return merge_dict
    
    def transform_data(self, datasource: gpd.GeoDataFrame, merge_dict: dict):
        for charging_station_index in merge_dict.keys():
            raw_data_charging_station = datasource.iloc[charging_station_index]
            charging_station = self.transform_to_charging_station(charging_station_index, raw_data_charging_station)
            self.append_charging_station_to_charging_station_dataframe(charging_station)

            socket = self.transform_to_socket(charging_station_index, raw_data_charging_station)
            self.append_socket_to_sockets_dataframe(socket)
            for socket_index in merge_dict[charging_station_index]:
                socket = self.transform_to_socket(charging_station_index, datasource.iloc[socket_index])
                self.append_socket_to_sockets_dataframe(socket)
    
    def append_charging_station_to_charging_station_dataframe(self, charging_station: dict):
        charging_station_record = pd.DataFrame(charging_station, index=["id"])
        if self.__charging_stations is None:
            self.__charging_stations = charging_station_record
        else:
            self.__charging_stations = pd.concat([self.__charging_stations, charging_station_record], ignore_index=True)
    
    def export_to_parquet_files(self, export_directory: str):
        # Convert to GeoDataFrame to be export into geoparquet
        charging_stations = to_geo_dataframe(self.__charging_stations)
        sockets = to_geo_dataframe(self.__sockets)

        with open(f"{export_directory}charging_stations.parquet", "wb") as f:
            charging_stations.to_parquet(f)

        with open(f"{export_directory}sockets.parquet", "wb") as f:
            sockets.to_parquet(f)

    def transform_to_charging_station(self, index: int, raw_data: dict) -> dict:
        return {
            "id": index,
            "geometry": raw_data["geometry"]
        }
    
    def transform_to_socket(self, charging_station_index: int, raw_data: dict) -> dict:
        return {
            "id": str(uuid.uuid4()),
            "geometry": raw_data["geometry"],
            "power_rated": raw_data["power_rated"],
            "number_of_sockets": raw_data["number_of_sockets"],
            "socket_type_ef": raw_data["socket_type_ef"],
            "socket_type_2": raw_data["socket_type_2"],
            "socket_type_combo_ccs": raw_data["socket_type_combo_ccs"],
            "socket_type_chademo": raw_data["socket_type_chademo"],
            "socket_type_autre": raw_data["socket_type_autre"],
            "charging_station_index": charging_station_index,
            "id_itinerance": raw_data['id_itinerance'],
            "retrieve_from": raw_data['retrieve_from']
        }

    def append_socket_to_sockets_dataframe(self, socket: dict):
        socket_record = pd.DataFrame(socket, index=["id"])

        if self.__sockets is None:
            self.__sockets = socket_record
        else:
            sockets_already_added_into_this_charging_station = self.__sockets[
                (self.__sockets["charging_station_index"] == socket["charging_station_index"]) & 
                (self.__sockets["power_rated"] == socket["power_rated"]) & 
                (self.__sockets["socket_type_ef"] == socket["socket_type_ef"]) & 
                (self.__sockets["socket_type_2"] == socket["socket_type_2"]) & 
                (self.__sockets["socket_type_combo_ccs"] == socket["socket_type_combo_ccs"]) & 
                (self.__sockets["socket_type_chademo"] == socket["socket_type_chademo"]) & 
                (self.__sockets["socket_type_autre"] == socket["socket_type_autre"])
            ]

            if len(sockets_already_added_into_this_charging_station) == 0:
                self.__sockets = pd.concat([self.__sockets, socket_record], ignore_index=True)