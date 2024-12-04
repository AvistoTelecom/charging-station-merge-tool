from chargingstationmergedtool.chargingstationmergetool import ChargingStationMergeTools
from argparse import ArgumentParser

if __name__ == '__main__':
    parser = ArgumentParser(prog="", description="A tool for merged French charging stations datasources")
    parser.add_argument('-c', '--config_file', required=True)

    args = parser.parse_args()

    chargingStationMergeTools = ChargingStationMergeTools(args.config_file)
    chargingStationMergeTools.process()