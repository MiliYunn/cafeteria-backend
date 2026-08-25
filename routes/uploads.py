"""Public access to locally stored uploads."""

from flask import Blueprint

from helpers.file_uploader import serve_upload

uploads_bp = Blueprint("uploads", __name__, url_prefix="/uploads")
uploads_bp.get("/<path:filename>")(serve_upload)
