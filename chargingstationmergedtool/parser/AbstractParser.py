"""
AbstractParser Module

This module provides an abstract class for parsing and managing geographic data.
It includes methods for adding records, converting to a GeoDataFrame, and exporting/importing data in GeoParquet format.

Classes:
    AbstractParser: A class to handle the parsing and management of geographic data.

Usage:
    To use this class, create a subclass that implements specific parsing logic.
    Use the methods to add data, convert to a GeoDataFrame, and export or import data.

Example:
    class MyParser(AbstractParser):
        def parse(self, data):
            for record in data:
                self.add_borne(record)

    parser = MyParser()
    parser.parse(data)
    parser.export_to_geoparquet('output_file.parquet')

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

import pandas as pd
import geopandas as gpd

class AbstractParser:
    """
    A class to handle the parsing and management of geographic data.

    Attributes:
        df (pd.DataFrame): DataFrame to store the parsed data.
    """

    def __init__(self):
        """
        Initializes the AbstractParser with an empty DataFrame.
        """
        self.df = None

    def add_borne(self, data: dict):
        """
        Adds a new record to the DataFrame.

        This method takes a dictionary representing a record and appends it to the DataFrame.

        Args:
            data (dict): A dictionary containing the data to be added as a new record.
        """
        new_record = pd.DataFrame([data])
        if self.df is None:
            self.df = new_record
        else:
            self.df = pd.concat([self.df, new_record], ignore_index=True)

    def convert_to_geoDataFrame(self) -> gpd.GeoDataFrame:
        """
        Converts the DataFrame to a GeoDataFrame.

        This method creates a GeoDataFrame from the stored DataFrame, using the 'geometry' column
        and setting the coordinate reference system to EPSG:4326.

        Returns:
            gpd.GeoDataFrame: A GeoDataFrame containing the geographic data.
        """
        return gpd.GeoDataFrame(self.df, geometry='geometry', crs="EPSG:4326")

    def export_to_geoparquet(self, filename: str):
        """
        Exports the data to a GeoParquet file.

        This method converts the DataFrame to a GeoDataFrame and saves it to a file in GeoParquet format.

        Args:
            filename (str): The name of the file to which the data will be exported.
        """
        gdf = self.convert_to_geoDataFrame()

        with open(filename, "wb") as f:
            gdf.to_parquet(f)

    def import_from_geoparquet(self, filename: str) -> gpd.GeoDataFrame:
        """
        Imports data from a GeoParquet file.

        This method reads a GeoParquet file and returns a GeoDataFrame.

        Args:
            filename (str): The name of the file from which to import the data.

        Returns:
            gpd.GeoDataFrame: A GeoDataFrame containing the imported geographic data.
        """
        return gpd.read_parquet(filename)
