from django.core.exceptions import ValidationError as DjangoValidationError
from rest_framework import status
from rest_framework.exceptions import APIException
from rest_framework.response import Response
from rest_framework.views import exception_handler as drf_exception_handler


def custom_exception_handler(exc, context) -> Response:
    """
    Global exception handler

    Wraps all DRF error responses in a consistent envelope:
    {
        "success": false,
        "message": "A human-readable summary",
        "errors":  { ... }   # field-level detail when available
    }
    """

    # Let DRF handle what it konws first
    response = drf_exception_handler(exc, context)

    # Conver Django's own ValidationError so it is also caught
    if response is None and isinstance(exc, DjangoValidationError):
        response = Response(
            {"detail": exc.messages},
            status=status.HTTP_400_BAD_REQUEST,
        )

    if response is not None:
        original_data = response.data

        # Normalise the payload
        if isinstance(original_data, dict):
            # Try to extract a top-level message
            message = (
                original_data.get("detail")
                or original_data.get("message")
                or _first_error(original_data)
                or "An error occured"
            )
            errors = {k: v for k, v in original_data.items() if k != "detail"}
        else:
            message = str(original_data)
            errors = {}

        response.data = {
            "success": False,
            "message": str(message),
            "errors": errors,
        }

    return response


def _first_error(data: dict) -> str:
    """Extract the first error string from a nested error dict."""
    for value in data.values():
        if isinstance(value, list) and value:
            return str(value[0])
        if isinstance(value, str):
            return value
    return ""
