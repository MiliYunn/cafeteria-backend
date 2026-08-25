from helpers.response import success_response


def health():
    return success_response({"status": "healthy"})
