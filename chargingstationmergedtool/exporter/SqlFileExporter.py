import pandas as pd
from jinja2 import Environment, PackageLoader, select_autoescape
import os

class SqlFileExporter:
    def __init__(self, charging_stations: pd.DataFrame, sockets: pd.DataFrame, export_directory_path: str):
        self.__export_directory_path = export_directory_path
        self.__charging_stations = charging_stations
        self.__sockets = sockets
        self.__env = Environment(
            loader=PackageLoader("chargingstationmergedtool"),
            autoescape=select_autoescape()
        )

    def export(self):
        self.export_charging_stations()
        self.export_sockets()

    def export_charging_stations(self):
        template = self.__env.get_template("sql/charging_stations.sql.j2")
        with open(f"{self.__export_directory_path}{os.sep}charging_stations.sql", 'w') as f:
            f.write(template.render(charging_stations=self.__charging_stations))

    def export_sockets(self):
        template = self.__env.get_template("sql/sockets.sql.j2")
        with open(f"{self.__export_directory_path}{os.sep}sockets.sql", 'w') as f:
            f.write(template.render(sockets=self.__sockets))