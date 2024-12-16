# How to use

Create a config file
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
For type_export values allowed : 'sql_files', 'sql', 'mongo_files', 'mongo'

Run command
```bash
python main.py -c config.json
```