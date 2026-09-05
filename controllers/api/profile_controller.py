"""Thin handlers for the signed-in staff or student profile."""

from flask import g, request

from helpers.response import success_response
from services.api.profile_service import ProfileService
from validations.api.profile import validate_profile_update


def get_profile():
    return success_response(ProfileService.get(int(g.auth["sub"])))


def update_profile():
    data = validate_profile_update(request.get_json(silent=True))
    return success_response(
        ProfileService.update(int(g.auth["sub"]), data), "Profile updated"
    )
