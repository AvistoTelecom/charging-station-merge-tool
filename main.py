from chargingstationmergedtool.parser.OsmParser import OsmParser
from chargingstationmergedtool.parser.DataGouvParser import DataGouvParser
from chargingstationmergedtool.Transform import Transform
from chargingstationmergedtool.Config import Config
from argparse import ArgumentParser
import os

parser = ArgumentParser(prog="", description="A tool for merged French charging stations datasources")
parser.add_argument('-c', '--config_file', required=True)

args = parser.parse_args()

config = Config(args.config_file)

# Create result directory
os.makedirs(config.export_directory_name, exist_ok=True)

osm_parser = OsmParser()

if config.osm_config["need_to_download"]:
    print("[ ] - Download OSM file")
    osm_parser.download_datasource(config)
    print("[x] - Download OSM file")

print("[ ] - Parse OSM file")
osm_parser.load_pbf(config.osm_config["path_file"])
print("[x] - Parse OSM file")
osm_parser.export_to_geoparquet(f"{config.export_directory_name}osm.parquet")
osm_parser_geo_data_frame = osm_parser.convert_to_geoDataFrame()


data_gouv = DataGouvParser()

if config.data_gouv_config["need_to_download"]:
    print("[ ] - Download Data gouv file")
    data_gouv.download_datasource(config)
    print("[x] - Download Data gouv file")

print("[ ] - Parse Data gouv file")
data_gouv.parse_file(config.data_gouv_config["path_file"])
print("[x] - Parse Data gouv file")
data_gouv.export_to_geoparquet(f"{config.export_directory_name}data_gouv.parquet")
data_gouv_geo_data_frame = data_gouv.convert_to_geoDataFrame()


transformer = Transform()
print("[ ] - Merge datasources")
combined_datasource = transformer.merge_datasources(osm_parser_geo_data_frame, data_gouv_geo_data_frame)
combined_datasource.to_parquet(f"{config.export_directory_name}combined.parquet")
print("[x] - Merge datasources")

print("[ ] - Group neighbors")
merge_dict = transformer.group_neighbouring(combined_datasource, config.distance)
print("[x] - Group neighbors")

print("[ ] - Transform data")
transformer.transform_data(combined_datasource, merge_dict)
print("[x] - Transform data")
print("[ ] - Export files to parquet")
transformer.export_to_parquet_files(config.export_directory_name)
print("[x] - Export files to parquet")