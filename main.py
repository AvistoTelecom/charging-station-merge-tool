"""
chargingstationmergedtool

This module provides a command-line tool for merging French charging station data sources.
It utilizes the ChargingStationMergeTools class to process the specified configuration file.

Usage:
    python script_name.py -c config_file

Arguments:
    -c, --config_file: The path to the configuration file that contains the necessary settings
                        for merging charging station data sources. This argument is required.

Example:
    python script_name.py -c /path/to/config.json

Classes:
    ChargingStationMergeTools: A class that handles the merging of charging station data sources.

    Methods:
        __init__(self, config_file):
            Initializes the ChargingStationMergeTools instance with the provided configuration file.

        process(self):
            Processes the charging station data sources based on the configuration file.
License:
    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU Lesser General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
    GNU Lesser General Public License for more details.

    You should have received a copy of the GNU Lesser General Public License
    along with this program. If not, see <https://www.gnu.org/licenses/>.
"""

from argparse import ArgumentParser

from src.chargingstationmergetool import ChargingStationMergeTools

if __name__ == '__main__':
    parser = ArgumentParser(prog="", description="A tool for merged French charging stations datasources")
    parser.add_argument('-c', '--config_file', required=True)

    args = parser.parse_args()

    chargingStationMergeTools = ChargingStationMergeTools(args.config_file)
    chargingStationMergeTools.process()
