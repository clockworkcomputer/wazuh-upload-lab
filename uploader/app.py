import os
from flask import Flask, request, abort
from werkzeug.utils import secure_filename

UPLOAD_DIR = os.getenv("UPLOAD_DIR", "/uploads")
MAX_UPLOAD_MB = int(os.getenv("MAX_UPLOAD_MB", "50"))
MAX_CONTENT_LENGTH = MAX_UPLOAD_MB * 1024 * 1024

app = Flask(__name__)
app.config["MAX_CONTENT_LENGTH"] = MAX_CONTENT_LENGTH

os.makedirs(UPLOAD_DIR, exist_ok=True)

@app.get("/health")
def health():
    return "ok\n", 200

@app.post("/upload")
def upload():
    if "file" not in request.files:
        abort(400, "ERROR: missing file field")

    f = request.files["file"]
    if not f.filename:
        abort(400, "ERROR: empty filename")

    filename = secure_filename(f.filename)
    if not filename:
        abort(400, "ERROR: invalid filename")

    dst = os.path.join(UPLOAD_DIR, filename)
    f.save(dst)

    return f"OK: archivo subido -> {filename}", 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
