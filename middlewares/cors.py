"""CORS policy configuration."""

from flask import Flask
from flask_cors import CORS


def configure_cors(app: Flask, origins: list[str]) -> None:
    CORS(
        app,
        resources={r"/cafeteria/*": {"origins": origins}},
        allow_headers=["Authorization", "Content-Type"],
        methods=["GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS"],
    )
