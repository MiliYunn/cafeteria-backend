from flask import request

from controllers.common import pagination_parameters
from helpers.response import paginated_response, success_response
from services.category_service import CategoryService
from validations.category import validate_category


def list_categories():
    result = CategoryService.list(*pagination_parameters())
    return paginated_response(result["items"], result["pagination"])


def category_options():
    return success_response(CategoryService.options())


def get_category(category_id: int):
    return success_response(CategoryService.get(category_id))


def create_category():
    return success_response(CategoryService.create(validate_category(request.get_json(silent=True))), "Category created", 201)


def update_category(category_id: int):
    return success_response(CategoryService.update(category_id, validate_category(request.get_json(silent=True), partial=True)), "Category updated")


def delete_category(category_id: int):
    CategoryService.delete(category_id)
    return success_response(message="Category deleted")
