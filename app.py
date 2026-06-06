"""Web interface for the Casio .g2e eActivity generator."""

import io
import os

from flask import Flask, jsonify, redirect, render_template, request, send_file, url_for

from g2e import _parse_text, create_g2e, import_g2e, sanitize_casio_filename

app = Flask(__name__, static_url_path="/calculadora/static")
app.config["MAX_CONTENT_LENGTH"] = 512 * 1024

DESKTOP_DOWNLOAD_URL = os.environ.get("DESKTOP_DOWNLOAD_URL", "").strip()


def render_editor():
    """Render the editor using the production subpath endpoints."""
    return render_template(
        "index.html",
        generate_url=url_for("generate"),
        import_url=url_for("import_file"),
        desktop_download_url=DESKTOP_DOWNLOAD_URL,
    )


@app.route("/", methods=["GET"])
def root():
    return redirect(url_for("index"))


@app.route("/calculadora", methods=["GET"])
def calculadora_redirect():
    return redirect(url_for("index"))


@app.route("/calculadora/", methods=["GET"])
def index():
    return render_editor()


@app.route("/calculadora/generate", methods=["POST"])
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


@app.route("/calculadora/import", methods=["POST"])
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


# Compatibility routes for older local builds.
@app.route("/generate", methods=["POST"])
def generate_legacy():
    return generate()


@app.route("/import", methods=["POST"])
def import_file_legacy():
    return import_file()


if __name__ == "__main__":
    app.run(debug=True)
