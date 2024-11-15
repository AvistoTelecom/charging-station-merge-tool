from chargingstationmergedtool.OsmParser import OsmParser
from chargingstationmergedtool.DataGouvParser import DataGouvParser
from chargingstationmergedtool.Transform import Transform
import geopandas as gpd
import pandas as pd

# osm_parser = OsmParser()
# print("[ ] - Parse OSM file")
# osm_parser.load_pbf("/home/vincent/Projets/Deki/implementations/maps/rhone-alpes-latest.osm.pbf")
# print("[x] - Parse OSM file")
# osm_parser.export_to_geoparquet("osm.parquet")
# osm_parser_geo_data_frame = osm_parser.convert_to_geoDataFrame()

# data_gouv = DataGouvParser()
# print("[ ] - Parse Data gouv file")
# data_gouv.parse_file("tests/ressources/consolidation-etalab-schema-irve-statique-v-2.3.1-20241113.csv")
# print("[x] - Parse Data gouv file")
# data_gouv.export_to_geoparquet("data_gouv.parquet")
# data_gouv_geo_data_frame = data_gouv.convert_to_geoDataFrame()

osm_parser_geo_data_frame = gpd.read_parquet("osm.parquet")
data_gouv_geo_data_frame = gpd.read_parquet("data_gouv.parquet")

transformer = Transform()
print("[ ] - Merge datasources")
combined_datasource = transformer.merge_datasources(osm_parser_geo_data_frame, data_gouv_geo_data_frame)
combined_datasource.to_parquet("combined.parquet")
print("[x] - Merge datasources")

print("[ ] - Group neighbors")
merge_dict = transformer.group_neighbouring(combined_datasource, 1500)
print("[x] - Group neighbors")

print("[ ] - Transform data")
transformer.transform_data(combined_datasource, merge_dict)
print("[x] - Transform data")
print("[ ] - Export files to parquet")
transformer.export_to_parquet_files("test1")
print("[x] - Export files to parquet")