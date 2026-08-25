"""File upload validation, storage, and HTTP handlers.

Local project storage is the only supported driver for now. Additional drivers,
such as S3, can be added behind ``create_storage`` later.
"""

from __future__ import annotations

from pathlib import Path
from uuid import uuid4

from flask import current_app, request, send_from_directory, url_for
from werkzeug.datastructures import FileStorage
from werkzeug.utils import secure_filename

from helpers.response import success_response
from validations.shared.exceptions import ValidationError


class LocalStorage:
    """Save uploaded files inside the configured project directory."""

    def __init__(self, root: str | Path):
        self.root = Path(root).resolve()
        self.root.mkdir(parents=True, exist_ok=True)

    def save(self, uploaded_file: FileStorage) -> dict[str, str]:
        safe_name = secure_filename(uploaded_file.filename or "")
        extension = Path(safe_name).suffix.lower()
        stored_name = f"{uuid4().hex}{extension}"
        destination = (self.root / stored_name).resolve()
        if destination.parent != self.root:
            raise ValueError("Invalid upload destination")
        uploaded_file.save(destination)
        return {
            "filename": stored_name,
            "original_filename": safe_name,
            "path": f"uploads/{stored_name}",
        }


def create_storage(driver: str, local_path: str | Path) -> LocalStorage:
    if driver == "local":
        return LocalStorage(local_path)
    raise ValueError(f"Unsupported storage driver: {driver}")


def validate_upload(
    uploaded_file: FileStorage | None,
    allowed_extensions: set[str],
) -> FileStorage:
    if uploaded_file is None or not uploaded_file.filename:
        raise ValidationError(errors={"file": "A file is required"})
    extension = Path(uploaded_file.filename).suffix.lower().lstrip(".")
    if not extension or extension not in allowed_extensions:
        allowed = ", ".join(sorted(allowed_extensions))
        raise ValidationError(
            errors={"file": f"File type is not allowed. Allowed types: {allowed}"}
        )
    return uploaded_file


def upload_file():
    """Validate and store the file from the current multipart request."""

    uploaded_file = validate_upload(
        request.files.get("file"),
        current_app.config["ALLOWED_UPLOAD_EXTENSIONS"],
    )
    storage = create_storage(
        current_app.config["STORAGE"],
        current_app.config["UPLOAD_FOLDER"],
    )
    result = storage.save(uploaded_file)
    result["url"] = url_for(
        "cafeteria.uploads.serve_upload",
        filename=result["filename"],
    )
    return success_response(result, "File uploaded", 201)


def serve_upload(filename: str):
    """Serve a file from the configured local upload directory."""

    return send_from_directory(current_app.config["UPLOAD_FOLDER"], filename)
