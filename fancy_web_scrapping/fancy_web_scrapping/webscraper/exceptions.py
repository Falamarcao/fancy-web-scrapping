from rest_framework.exceptions import APIException


class ValidationError(APIException):
    status_code = 500  # or whatever you want
    # default_code = '4026'
    default_detail = {"error": "ValidationError",
                      "message": r"missing 'id' URL parameter e.g. /api/v1/webscraper?id={integer}"}
