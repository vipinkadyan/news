from flask import Flask, jsonify, render_template, send_from_directory
import os

# ================= CONFIG =================
DATA_DIR = os.getenv("DATA_DIR", os.path.dirname(os.path.abspath(__file__)))
PIC_FOLDER = os.path.join(DATA_DIR, "pic")
os.makedirs(PIC_FOLDER, exist_ok=True)
# =========================================

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/images")
def images():
    files = [
        f for f in os.listdir(PIC_FOLDER)
        if f.lower().endswith((".jpg", ".jpeg", ".png", ".webp"))
    ]
    files.sort()
    return jsonify(files)


@app.route("/pic/<filename>")
def serve_pic(filename):
    return send_from_directory(PIC_FOLDER, filename)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
