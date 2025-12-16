"""

Scanner App: Aplikasi scanner yang dikhususkan untuk orang - orang dengan keterbatasan pada device mobile dalam menggunakan CamScanner

"""

# // Import cv2 / opencv for image processing
import cv2 as opcv

# // Import flask for http server
import flask

# // Import os for file management
import os

# // Import For Filepath
import pathlib


# Global Constant Raw Path, path for Raw Image
GC_FILE_PATH = pathlib.Path(__file__).parent.resolve()


app = flask.Flask(__name__)


@app.route("/")
def home():
    return "Server hidup"


@app.route("/ping", methods=["GET"])
def ping():
    return "pong"


@app.route("/pong", methods=["POST"])
def upload():
    # Header

    saved_filename = ""
    if "image" not in flask.request.files:
        print("one 1")
        return "one 1"

    # Lakukan Get Data,
    file = flask.request.files["image"]

    # Match Guard
    match file.filename:
        # // To Counter if None
        case None:
            print("one 2")
            return "one 2"

        # // For Any
        case _:
            # for saving filepath
            saved_filename = str("img/raw/Raw_") + file.filename

            # Simpan pada src/img/
            # Save This For Later Disposal
            filepath = os.path.join(GC_FILE_PATH, saved_filename)

            # DEBUG
            print("Filess=====: " + filepath)
            file.save(filepath)

            # Fungsi SCAN

            # Fungsi mengirimkan hasil ke clipboard
            # // todo

            print("All Is Done")
            return "All Is Done"


app.run(host="0.0.0.0", port=5000)
