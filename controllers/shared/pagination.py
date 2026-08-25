from flask import request

from validations.shared.fields import validate_pagination


def pagination_parameters() -> tuple[int, int]:
    return validate_pagination(request.args.get("page"), request.args.get("per_page"))
