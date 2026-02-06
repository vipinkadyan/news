from flask import Flask, jsonify, render_template, send_from_directory
import os

app = Flask(__name__)

PIC_FOLDER = os.path.join(app.root_path, "static", "pic")

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

# ✅ ADD THIS ROUTE (ONLY REQUIRED FIX)
@app.route("/pic/<path:filename>")
def serve_pic(filename):
    return send_from_directory(PIC_FOLDER, filename)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
