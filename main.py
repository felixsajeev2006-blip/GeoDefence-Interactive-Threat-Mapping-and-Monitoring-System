
import sys

from PyQt6.QtWidgets import QApplication, QMainWindow
from PyQt6.QtWebEngineWidgets import QWebEngineView


class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()

        self.setWindowTitle("Defense Map System")
        self.resize(1400, 800)

        self.map_view = QWebEngineView()
        self.setCentralWidget(self.map_view)

        html = r"""
<!DOCTYPE html>
<html>

<head>

<meta charset="utf-8">

<link rel="stylesheet"
href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css">

<style>

html, body {
    margin: 0;
    padding: 0;
    width: 100%;
    height: 100%;
}

#map {
    width: 100%;
    height: 100%;
}


/* =========================
   DASHBOARD
========================= */

.dashboard {

    position: absolute;

    z-index: 1000;

    top: 15px;
    left: 15px;

    width: 280px;

    background: rgba(20, 25, 30, 0.96);

    color: white;

    padding: 18px;

    border-radius: 10px;

    box-shadow: 0 4px 15px rgba(0,0,0,0.5);

    font-family: Arial, sans-serif;

}


.title {

    font-size: 20px;

    font-weight: bold;

}


.subtitle {

    color: #aaa;

    font-size: 12px;

    margin-top: 5px;

    margin-bottom: 20px;

}


.section {

    border-top: 1px solid #444;

    padding-top: 12px;

    margin-top: 12px;

}


.section-title {

    color: #aaa;

    font-size: 12px;

    text-transform: uppercase;

    margin-bottom: 10px;

}


.status {

    display: flex;

    justify-content: space-between;

    padding: 7px 0;

}


.status-left {

    display: flex;

    align-items: center;

}


.dot {

    width: 11px;

    height: 11px;

    border-radius: 50%;

    margin-right: 9px;

}


.red {

    background: red;

}


.orange {

    background: orange;

}


.green {

    background: #20c968;

}


.count {

    font-weight: bold;

}


.total {

    font-size: 17px;

    font-weight: bold;

}


button {

    width: 100%;

    padding: 10px;

    margin-top: 6px;

    background: #3d4852;

    color: white;

    border: 1px solid #777;

    border-radius: 5px;

    cursor: pointer;

    font-weight: bold;

}


button:hover {

    background: #53606b;

}


.delete-button {

    background: #8b3030;

}


.delete-button:hover {

    background: #aa3b3b;

}


.footer {

    margin-top: 18px;

    text-align: center;

    color: #777;

    font-size: 10px;

}


/* =========================
   POPUP
========================= */

.popup-box {

    font-family: Arial, sans-serif;

    width: 230px;

}


.popup-box h3 {

    margin-top: 0;

}


.popup-box select,
.popup-box input,
.popup-box textarea {

    width: 100%;

    box-sizing: border-box;

    margin-bottom: 8px;

    padding: 7px;

}


.popup-box textarea {

    resize: vertical;

}


.popup-box button {

    margin-top: 4px;

}


/* =========================
   INSTRUCTION
========================= */

.map-instruction {

    position: absolute;

    z-index: 900;

    bottom: 20px;

    left: 50%;

    transform: translateX(-50%);

    background: rgba(20,25,30,0.9);

    color: white;

    padding: 8px 15px;

    border-radius: 5px;

    font-family: Arial;

    font-size: 12px;

}

</style>

</head>


<body>


<div id="map"></div>


<!-- =========================
     DASHBOARD
========================= -->

<div class="dashboard">

    <div class="title">
        DEFENSE MAP SYSTEM
    </div>

    <div class="subtitle">
        Interactive Geographic Monitoring
    </div>


    <div class="section">

        <div class="section-title">
            Detection Status
        </div>


        <div class="status">

            <div class="status-left">

                <div class="dot red"></div>

                High Threat

            </div>

            <div id="highCount" class="count">
                0
            </div>

        </div>


        <div class="status">

            <div class="status-left">

                <div class="dot orange"></div>

                Medium Threat

            </div>

            <div id="mediumCount" class="count">
                0
            </div>

        </div>


        <div class="status">

            <div class="status-left">

                <div class="dot green"></div>

                Low Threat

            </div>

            <div id="lowCount" class="count">
                0
            </div>

        </div>

    </div>


    <div class="section">

        <div class="section-title">
            System Summary
        </div>

        <div id="totalCount" class="total">
            Total Detections: 0
        </div>

    </div>


    <div class="section">

        <div class="section-title">
            Controls
        </div>

        <button onclick="centerIndia()">
            CENTER ON INDIA
        </button>

        <button onclick="clearAll()"
                class="delete-button">

            CLEAR ALL MARKERS

        </button>

    </div>


    <div class="footer">

        DEFENSE TECHNOLOGY PROTOTYPE

    </div>

</div>


<div class="map-instruction">

    Click anywhere on the map to add a detection

</div>


<script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js">
</script>


<script>


// =====================================================
// MAP
// =====================================================

var map = L.map("map").setView(
    [22.5937, 78.9629],
    5
);


// =====================================================
// MAP LAYERS
// =====================================================

var normal = L.tileLayer(

    "https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png",

    {
        maxZoom: 19,
        attribution: "OpenStreetMap"
    }

);


var terrain = L.tileLayer(

    "https://{s}.tile.opentopomap.org/{z}/{x}/{y}.png",

    {
        maxZoom: 17,
        attribution: "OpenTopoMap"
    }

);


var satellite = L.tileLayer(

    "https://server.arcgisonline.com/ArcGIS/rest/services/" +
    "World_Imagery/MapServer/tile/{z}/{y}/{x}",

    {
        maxZoom: 19,
        attribution: "Esri"
    }

);


normal.addTo(map);


L.control.layers(

    {

        "Normal": normal,

        "Terrain": terrain,

        "Satellite": satellite

    }

).addTo(map);


// =====================================================
// MARKER STORAGE
// =====================================================

var markers = [];

var detectionNumber = 1;


// =====================================================
// CREATE MARKER ICON
// =====================================================

function createIcon(color) {

    return L.divIcon({

        className: "",

        html:

        '<div style="' +

        'background:' + color + ';' +

        'width:18px;' +

        'height:18px;' +

        'border-radius:50%;' +

        'border:3px solid white;' +

        'box-shadow:0 0 6px black;' +

        '"></div>',

        iconSize: [24,24],

        iconAnchor: [12,12]

    });

}


// =====================================================
// CREATE DETECTION
// =====================================================

function addDetection(latlng) {


    var marker = L.marker(

        latlng,

        {

            icon: createIcon("red"),

            draggable: true

        }

    ).addTo(map);


    var id =

        "DET-" +

        String(detectionNumber).padStart(3, "0");


    detectionNumber++;


    var popup = `

        <div class="popup-box">

            <h3>New Detection</h3>


            <label>
                Detection Name
            </label>

            <input

                id="name-${id}"

                type="text"

                placeholder="Example: Plot A"

            >


            <label>
                Threat Level
            </label>

            <select id="threat-${id}">

                <option value="High">
                    High Threat
                </option>

                <option value="Medium">
                    Medium Threat
                </option>

                <option value="Low">
                    Low Threat
                </option>

            </select>


            <label>
                Description
            </label>

            <textarea

                id="description-${id}"

                rows="3"

                placeholder="Enter details">

            </textarea>


            <button

                onclick="saveDetection(
                    '${id}'
                )">

                SAVE DETECTION

            </button>


            <button

                class="delete-button"

                onclick="deleteDetection(
                    '${id}'
                )">

                DELETE

            </button>

        </div>

    `;


    marker.bindPopup(popup).openPopup();


    marker.detectionId = id;


    markers.push(marker);


    updateDashboard();

}


// =====================================================
// SAVE DETECTION
// =====================================================

function saveDetection(id) {


    var marker = markers.find(

        function(m) {

            return m.detectionId === id;

        }

    );


    if (!marker) return;


    var name =
        document.getElementById(
            "name-" + id
        ).value;


    var threat =
        document.getElementById(
            "threat-" + id
        ).value;


    var description =
        document.getElementById(
            "description-" + id
        ).value;


    if (name.trim() === "") {

        name = id;

    }


    var color;


    if (threat === "High") {

        color = "red";

    }

    else if (threat === "Medium") {

        color = "orange";

    }

    else {

        color = "#20c968";

    }


    marker.setIcon(
        createIcon(color)
    );


    marker.threat = threat;


    marker.detectionName = name;


    marker.description = description;


    marker
        .bindPopup(

            "<b>" +
            name +
            "</b><br><br>" +

            "<b>Detection ID:</b> " +
            id +
            "<br>" +

            "<b>Threat:</b> " +
            threat +
            "<br><br>" +

            description +

            "<br><br>" +

            "<i>Drag marker to move location.</i>"

        );


    marker.openPopup();


    updateDashboard();

}


// =====================================================
// DELETE DETECTION
// =====================================================

function deleteDetection(id) {


    var marker = markers.find(

        function(m) {

            return m.detectionId === id;

        }

    );


    if (!marker) return;


    map.removeLayer(marker);


    markers = markers.filter(

        function(m) {

            return m.detectionId !== id;

        }

    );


    updateDashboard();

}


// =====================================================
// CLICK MAP → ADD DETECTION
// =====================================================

map.on(

    "click",

    function(e) {

        addDetection(e.latlng);

    }

);


// =====================================================
// UPDATE DASHBOARD
// =====================================================

function updateDashboard() {


    var high = 0;

    var medium = 0;

    var low = 0;


    markers.forEach(

        function(marker) {


            if (marker.threat === "High") {

                high++;

            }

            else if (marker.threat === "Medium") {

                medium++;

            }

            else if (marker.threat === "Low") {

                low++;

            }

        }

    );


    document.getElementById(
        "highCount"
    ).innerText = high;


    document.getElementById(
        "mediumCount"
    ).innerText = medium;


    document.getElementById(
        "lowCount"
    ).innerText = low;


    document.getElementById(
        "totalCount"
    ).innerText =

        "Total Detections: " +

        markers.length;

}


// =====================================================
// CENTER INDIA
// =====================================================

function centerIndia() {

    map.setView(

        [22.5937, 78.9629],

        5

    );

}


// =====================================================
// CLEAR ALL
// =====================================================

function clearAll() {


    markers.forEach(

        function(marker) {

            map.removeLayer(marker);

        }

    );


    markers = [];


    updateDashboard();

}


</script>


</body>

</html>
"""

        self.map_view.setHtml(html)


app = QApplication(sys.argv)

window = MainWindow()

window.show()

sys.exit(app.exec())

