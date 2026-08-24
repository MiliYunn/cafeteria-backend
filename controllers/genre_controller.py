from flask import request

from controllers.common import pagination_parameters
from helpers.response import paginated_response, success_response
from services.genre_service import GenreService
from validations.genre import validate_genre


def list_genres():
    result = GenreService.list(*pagination_parameters())
    return paginated_response(result["items"], result["pagination"])


def genre_options():
    return success_response(GenreService.options())


def get_genre(genre_id: int):
    return success_response(GenreService.get(genre_id))


def create_genre():
    return success_response(GenreService.create(validate_genre(request.get_json(silent=True))), "Genre created", 201)


def update_genre(genre_id: int):
    return success_response(GenreService.update(genre_id, validate_genre(request.get_json(silent=True), partial=True)), "Genre updated")


def delete_genre(genre_id: int):
    GenreService.delete(genre_id)
    return success_response(message="Genre deleted")
