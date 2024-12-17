# How to use

Run command
```bash
python main.py -c config.json
```

## Configuration File Description
```json
{
    "common": {
        "distance": 1500,
        "type_export": "sql_files" 
    },
    "osm": {
        "path_file": ""
    },
    "data_gouv": {
        "path_file": ""
    },
    "sql": {
        "connection_url": "",
        "charging_stations_table_name": "",
        "sockets_table_name": ""
    },
    "mongo": {
        "connection_url": "",
        "database_name": "",
        "charging_stations_collection_name": ""
    }
}
```
This configuration file is structured in JSON format and is used to define various settings for the application. Below is a breakdown of its components:

### Common Settings

- **`common`**: This section contains settings that are applicable across the application.
  - **`distance`**: Specifies the distance (in meters) used to group charging stations together. In this example, the distance is set to 1500 meters.
  - **`type_export`**: Defines the type of export format to be used. In this case, it is set to `"sql_files"`. 

#### Export Options
You have the option to choose from several formats for exporting your data. The available options are:

- `sql_files`
- `sql`
- `mongo_files`
- `mongo`
- `parquet`
- (or nothing)

**Important Note**: Regardless of the format you choose, an export in Parquet format will always be generated. This means that even if you select one of the other options, the system will automatically perform a Parquet export in addition. The Parquet format is particularly advantageous for data storage and analysis, as it allows for efficient compression and fast reading.

### OSM Settings

- **`osm`**: This section is dedicated to settings related to OpenStreetMap data.
  - **`path_file`**: Specifies the path to the OSM data file. If left empty, the system will automatically download the latest version from the internet.

### Data Gouv Settings

- **`data_gouv`**: This section is for settings related to government data sources.
  - **`path_file`**: Specifies the path to the government data file. Similar to the OSM section, if this value is empty, the system will download the latest version automatically.

### SQL Database Settings

- **`sql`**: This section contains settings for connecting to an SQL database.
  - **`connection_url`**: The URL used to connect to the SQL database. This should be filled with the appropriate connection string.
  - **`charging_stations_table_name`**: The name of the table in the SQL database that contains charging station data.
  - **`sockets_table_name`**: The name of the table in the SQL database that contains socket data.

### MongoDB Settings

- **`mongo`**: This section is for settings related to MongoDB.
  - **`connection_url`**: The URL used to connect to the MongoDB database. This should be filled with the appropriate connection string.
  - **`database_name`**: The name of the MongoDB database to be used.
  - **`charging_stations_collection_name`**: The name of the collection in MongoDB that contains charging station data.

### Input File Processing

Once the input files are parsed, the system will perform a checksum on them to detect any modifications since the last execution. If both files have not been modified, the program will terminate immediately, avoiding unnecessary processing. This mechanism ensures that the application only runs when there are changes to the input data, optimizing performance and resource usage.