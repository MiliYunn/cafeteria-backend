from flask import request

from controllers.shared.pagination import pagination_parameters
from helpers.response import paginated_response, success_response
from services.admin.role_service import RoleService
from validations.admin.filters import validate_role_filters
from validations.admin.role import validate_role


def list_roles():
    """List roles. Query: page, per_page, search, is_active."""

    result = RoleService.list(*pagination_parameters(), validate_role_filters(request.args))
    return paginated_response(result["items"], result["pagination"])


def role_options():
    return success_response(RoleService.options())


def get_role(role_id: int):
    return success_response(RoleService.get(role_id))


def create_role():
    return success_response(RoleService.create(validate_role(request.get_json(silent=True))), "Role created", 201)


def update_role(role_id: int):
    return success_response(RoleService.update(role_id, validate_role(request.get_json(silent=True), partial=True)), "Role updated")


def delete_role(role_id: int):
    RoleService.delete(role_id)
    return success_response(message="Role deleted")
