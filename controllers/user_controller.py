from flask import g, request

from controllers.common import pagination_parameters
from helpers.response import paginated_response, success_response
from services.user_service import UserService
from validations.user import validate_user


def list_users():
    result = UserService.list(*pagination_parameters())
    return paginated_response(result["items"], result["pagination"])


def get_user(user_id: int):
    return success_response(UserService.get(user_id))


def create_user():
    return success_response(UserService.create(validate_user(request.get_json(silent=True))), "User created", 201)


def update_user(user_id: int):
    return success_response(UserService.update(user_id, validate_user(request.get_json(silent=True), partial=True)), "User updated")


def delete_user(user_id: int):
    UserService.delete(user_id, int(g.auth["sub"]))
    return success_response(message="User deleted")
