"""
app.py — Flask web UI for the Casio .g2e eActivity generator
Run:  python app.py
Then open http://localhost:5000 in your browser.

ChatGPT note (2026-05-26): filename is sanitized to an 8-character
calculator-safe base name before generating/downloading.  That same base name
is used as the fallback eActivity heading when the user did not write a
"=== Title ===" strip marker.
"""

from flask import Flask, render_template, request, send_file
import io
from g2e import _parse_text, create_g2e, sanitize_casio_filename

app = Flask(__name__)


@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")


@app.route("/generate", methods=["POST"])
def generate():
    content = request.form.get("content", "")
    requested_filename = request.form.get("filename", "eactivity")
    safe_filename = sanitize_casio_filename(requested_filename, fallback="EACT")
    default_title = safe_filename[:-4]

    strips = _parse_text(content)
    data = create_g2e(strips, default_title=default_title)

    return send_file(
        io.BytesIO(data),
        mimetype="application/octet-stream",
        as_attachment=True,
        download_name=safe_filename,
    )


if __name__ == "__main__":
    app.run(debug=True)
