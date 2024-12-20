# Charging Station Merge Tools

Welcome to our Electric Charging Station Data Management Tool. This tool has been designed to facilitate access to and analysis of data available on the French government's OpenData site, as well as data from PBF (Protocolbuffer Binary Format) files.

## 🚀 Features
- **Automated Download**: The tool automatically downloads the necessary files before parsing them.
- **Data Merging**: It merges charging points located within a specified radius to form coherent charging stations.
- **Flexible Export Options**: Data can be exported in Parquet format, with additional options for exporting to SQL or to a NoSQL database like MongoDB.

![introduction charging station merged tool](docs/modules_merge_charging_station_tools.png "Process")

This tool is ideal for professionals and researchers looking to analyze charging infrastructure and contribute to the energy transition.

We invite you to explore the features of this tool and integrate it into your projects to optimize the management of charging stations.

## 🛠 Installation
### Dependencies
- [osmosis](https://github.com/openstreetmap/osmosis)
- [poetry](https://python-poetry.org/)

### Install
```bash
poetry install
```

## 💻 Usage
Run command
```bash
python main.py -c config.json
```

## 📝 License
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

## 🤝 Contributing
We welcome contributions!

Fork the repository.

Create a feature branch:
```bash 
git checkout -b feature-branch  
```

Make your changes and commit them:
```bash 
git commit -m "Describe your changes"  
```

Push to your branch:
```bash 
git push origin feature-branch
```

Submit a Pull Request.