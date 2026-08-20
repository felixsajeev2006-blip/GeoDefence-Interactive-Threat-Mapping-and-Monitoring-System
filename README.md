# GeoDefence – Interactive Threat Mapping and Monitoring System

GeoDefence is a Python-based interactive mapping and monitoring system developed as part of an internship project. It allows users to mark geographical detection points, assign threat levels, add descriptions, and monitor detection statistics through a desktop-based interface.

The project combines **PyQt6, Leaflet.js, HTML, CSS, and JavaScript**, along with an **offline map tile server using Flask and MBTiles**.

## Features

* Interactive geographical map
* Normal, Terrain, and Satellite map views
* Location-based detection marking
* High, Medium, and Low threat classification
* Color-coded detection markers
* Detection name, ID, and description
* Draggable detection markers
* Detection statistics dashboard
* Delete individual or all detections
* Offline map tile support using MBTiles

## Technologies Used

| Technology     | Purpose                                                   |
| -------------- | --------------------------------------------------------- |
| Python         | Core application development                              |
| PyQt6          | Desktop application interface                             |
| QWebEngineView | Displays the web-based map inside the desktop application |
| Leaflet.js     | Interactive map and marker management                     |
| HTML/CSS       | Structure and styling of the interface                    |
| JavaScript     | Map interaction and detection management                  |
| Flask          | Local offline tile server                                 |
| SQLite         | Reading map tile data                                     |
| MBTiles        | Storage format for offline map tiles                      |

## Project Structure

```text
GeoDefence/
│
├── data/
│   └── *.mbtiles
├── leaflet/
├── detections.json
├── main.py
├── maintry.py
├── tile_server.py
└── README.md
```

## Installation

Clone the repository:

```bash
git clone https://github.com/felixsajeev2006-blip/GeoDefence-Interactive-Threat-Mapping-and-Monitoring-System.git
cd GeoDefence-Interactive-Threat-Mapping-and-Monitoring-System
```

Install the required packages:

```bash
pip install PyQt6 PyQt6-WebEngine Flask
```

## Running the Application

Run the main application:

```bash
python main.py
```

For the offline tile server:

```bash
python tile_server.py
```

The offline server uses `.mbtiles` files placed inside the `data` directory.

## How It Works

The user can click on the map to create a detection marker. Each detection can be assigned a name, threat level, and description. The marker color changes according to the selected threat level, and the dashboard automatically updates the detection counts.

The offline component uses Flask to serve locally stored MBTiles through a tile endpoint, allowing map data to be accessed without relying entirely on external map tile services.

## Project Status

This project was developed as an **internship prototype** to explore interactive geographic mapping, threat visualization, and offline map technologies.

## Author

**Felix K S**

B.Tech – Artificial Intelligence and Machine Learning

GitHub: https://github.com/felixsajeev2006-blip
