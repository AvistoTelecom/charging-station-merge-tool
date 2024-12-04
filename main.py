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






