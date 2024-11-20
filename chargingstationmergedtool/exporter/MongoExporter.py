import pandas as pd
from chargingstationmergedtool.exporter.AbstractNoSqlExporter import AbstractNoSqlExporter
from pymongo import MongoClient

class MongoExporter(AbstractNoSqlExporter):
    def __init__(self, config: dict, charging_stations: pd.DataFrame, sockets: pd.DataFrame):
        super().__init__(charging_stations, sockets)
        self.__config = config
        self.__client = MongoClient(config['connection_url'], timeoutMS=7200)

    def export(self):
        db = self.__client.get_database(self.__config['database_name'])
        collection = db.get_collection(self.__config['charging_stations_collection_name'])

        collection.insert_many(self.transform_data_to_dict())