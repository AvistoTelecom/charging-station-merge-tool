import pandas as pd
from chargingstationmergedtool.exporter.AbstractNoSqlExporter import AbstractNoSqlExporter
import json

class MongoFileExporter(AbstractNoSqlExporter):
    def __init__(self, charging_stations: pd.DataFrame, sockets: pd.DataFrame, export_directory_path: str):
        super().__init__(charging_stations, sockets)
        self.__export_directory_path = export_directory_path

    def export(self):
        for charging_station in self.transform_data_to_dict():
            with open(f"{self.__export_directory_path}/charing_station_{charging_station['id']}", 'w') as f:
                json.dump(charging_station, f, indent=2)