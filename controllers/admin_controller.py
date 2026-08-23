from flask import request

from helpers.response import success_response
from services.admin_service import AdminService
from validations.category import validate_category_create


def list_users():
    return success_response(AdminService.list_users())


def list_categories():
    return success_response(AdminService.list_categories())


def create_category():
    data = validate_category_create(request.get_json(silent=True))
    return success_response(AdminService.create_category(data), "Category created", 201)

