import pandas as pd
import geopandas as gpd

class AbstractParser():
    def __init__(self):
        columns = [
            'geometry',
            'power_rated',
            'number_of_sockets',
            'socket_type_ef',
            'socket_type_2',
            'socket_type_combo_ccs',
            'socket_type_chademo',
            'socket_type_autre'
        ]

        self.df = None

    def add_borne(self, data: dict):
        new_record = pd.DataFrame([data])
        if self.df is None:
            self.df = new_record
        else:
            self.df = pd.concat([self.df, new_record], ignore_index=True)

    def convert_to_geoDataFrame(self) -> gpd.GeoDataFrame:
        return gpd.GeoDataFrame(self.df, geometry='geometry', crs="EPSG:4326")

    def export_to_geoparquet(self, filename):
        # gs = gpd.GeoSeries.from_wkb(self.df['geometry'])
        gdf = self.convert_to_geoDataFrame()

        with open(filename, "wb") as f:
            gdf.to_parquet(f)