from flask import Flask, send_file, abort
import sqlite3
import os
import io

app = Flask(__name__)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")


# Find MBTiles files
mbtiles_files = [
    os.path.join(DATA_DIR, file)
    for file in os.listdir(DATA_DIR)
    if file.lower().endswith(".mbtiles")
]

if not mbtiles_files:
    raise FileNotFoundError(
        "No .mbtiles file found inside the data folder."
    )


# Use the largest MBTiles file
MBTILES_FILE = max(
    mbtiles_files,
    key=os.path.getsize
)

print("--------------------------------")
print("OFFLINE MAP SERVER")
print("--------------------------------")
print("Using:")
print(MBTILES_FILE)
print("--------------------------------")


@app.route("/")
def home():
    return "Offline Map Server is running."


@app.route("/tiles/<int:z>/<int:x>/<int:y>.png")
def get_tile(z, x, y):

    try:

        # XYZ → TMS
        tms_y = (1 << z) - 1 - y

        connection = sqlite3.connect(MBTILES_FILE)

        cursor = connection.cursor()

        cursor.execute(
            """
            SELECT tile_data
            FROM tiles
            WHERE zoom_level = ?
            AND tile_column = ?
            AND tile_row = ?
            """,
            (z, x, tms_y)
        )

        result = cursor.fetchone()

        connection.close()

        if result is None:
            return abort(404)

        tile_data = result[0]

        # Detect image type
        if tile_data.startswith(b"\x89PNG"):
            mime_type = "image/png"

        elif tile_data.startswith(b"\xff\xd8"):
            mime_type = "image/jpeg"

        else:
            mime_type = "image/png"

        return send_file(
            io.BytesIO(tile_data),
            mimetype=mime_type
        )

    except Exception as e:

        print("Tile error:", e)

        return abort(500)


if __name__ == "__main__":

    app.run(
        host="127.0.0.1",
        port=5000,
        debug=False
    )