import pandas as pd
from sqlalchemy import create_engine
from chargingstationmergedtool.utils import to_geo_dataframe

class SqlExporter:
    def __init__(self, config: dict, charging_stations: pd.DataFrame, sockets: pd.DataFrame):
        self.__config = config
        self.__charging_stations = charging_stations
        self.__sockets = sockets
        self.__engine = create_engine(config["connection_url"])

    def export_charging_stations(self):
        to_geo_dataframe(self.__charging_stations).to_postgis(self.__config['charging_stations_table_name'], self.__engine)

    def export_sockets(self):
        to_geo_dataframe(self.__sockets).to_postgis(self.__config['sockets_table_name'], self.__engine)