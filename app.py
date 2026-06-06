"""Flask interface for the Casio .g2e eActivity generator."""

import io

from flask import Flask, jsonify, render_template, request, send_file

from g2e import _parse_text, create_g2e, import_g2e, sanitize_casio_filename

app = Flask(__name__)
app.config["MAX_CONTENT_LENGTH"] = 512 * 1024


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


@app.route("/import", methods=["POST"])
def import_file():
    uploaded = request.files.get("file")
    if uploaded is None or uploaded.filename == "":
        return jsonify({"error": "No se seleccionó ningún archivo .g2e."}), 400

    raw = uploaded.read()
    try:
        result = import_g2e(raw, uploaded.filename)
    except ValueError as exc:
        return jsonify({"error": str(exc)}), 400

    return jsonify({
        "filename": result.filename,
        "content": result.content,
        "warnings": result.warnings,
    })


if __name__ == "__main__":
    app.run(debug=True)
