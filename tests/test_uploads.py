from io import BytesIO

import pytest
from werkzeug.datastructures import FileStorage

from app import create_app
from helpers.file_uploader import LocalStorage, create_storage, validate_upload
from validations.shared.exceptions import ValidationError


def test_local_storage_saves_with_safe_random_name(tmp_path):
    uploaded = FileStorage(stream=BytesIO(b"image-data"), filename="../../shop logo.png")
    result = LocalStorage(tmp_path).save(uploaded)

    assert result["original_filename"] == "shop_logo.png"
    assert result["filename"].endswith(".png")
    assert result["path"].startswith("uploads/")
    assert (tmp_path / result["filename"]).read_bytes() == b"image-data"


def test_upload_validation_rejects_missing_and_unsupported_files():
    with pytest.raises(ValidationError):
        validate_upload(None, {"png"})
    uploaded = FileStorage(stream=BytesIO(b"data"), filename="virus.exe")
    with pytest.raises(ValidationError):
        validate_upload(uploaded, {"png"})


def test_only_local_storage_is_supported(tmp_path):
    assert isinstance(create_storage("local", tmp_path), LocalStorage)
    with pytest.raises(ValueError):
        create_storage("s3", tmp_path)


def test_upload_endpoint_requires_admin_token(client):
    response = client.post(
        "/cafeteria/admin/uploads",
        data={"file": (BytesIO(b"image"), "shop.png")},
        content_type="multipart/form-data",
    )
    assert response.status_code == 401


def test_local_upload_can_be_served(tmp_path):
    app = create_app(
        {
            "TESTING": True,
            "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:",
            "UPLOAD_FOLDER": str(tmp_path),
        }
    )
    (tmp_path / "sample.png").write_bytes(b"image-data")
    response = app.test_client().get("/cafeteria/uploads/sample.png")
    assert response.status_code == 200
    assert response.data == b"image-data"
