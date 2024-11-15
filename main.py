from chargingstationmergedtool.OsmParser import OsmParser
from chargingstationmergedtool.DataGouvParser import DataGouvParser
from chargingstationmergedtool.Transform import Transform
import geopandas as gpd
import pandas as pd

# osm_parser = OsmParser()
# osm_parser.load_pbf("/home/vincent/Projets/Deki/implementations/maps/rhone-alpes-latest.osm.pbf")
# osm_parser.export_to_geoparquet("osm.parquet")
# osm_parser_geo_data_frame = osm_parser.convert_to_geoDataFrame()

# data_gouv = DataGouvParser()
# data_gouv.parse_file("consolidation-etalab-schema-irve-statique-v-2.3.1-20241113.csv")
# data_gouv.export_to_geoparquet("data_gouv.parquet")
# data_gouv_geo_data_frame = data_gouv.convert_to_geoDataFrame()

osm_parser_geo_data_frame = gpd.read_parquet("osm.parquet")
data_gouv_geo_data_frame = gpd.read_parquet("data_gouv.parquet")

transformer = Transform()

combined_datasource = transformer.merge_datasources(osm_parser_geo_data_frame, data_gouv_geo_data_frame)

merge_dict = transformer.group_neighbouring(combined_datasource, 1500)

transformer.transform_data(combined_datasource, merge_dict)
transformer.export_to_parquet_files("test1")