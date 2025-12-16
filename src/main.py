# Untuk Parsing CLI
import argparse
import cv2 as opcv
import flask


app = flask.Flask(__name__)


@app.route("/")
def home():
    return "Server hidup"


@app.route("/ping", methods=["GET"])
def ping():
    return "pong"


@app.route("/pong", methods=["POST"])
def upload():
    # TODO:

    # Lakukan Get Data,

    # Simpan pada src/img/

    # Fungsi SCAN

    # Fungsi mengirimkan hasil ke clipboard

    return "Server hidup"


app.run(host="0.0.0.0", port=8000)
