import logging

from rest_framework.views import exception_handler
from rest_framework.status import (
    HTTP_401_UNAUTHORIZED,
    HTTP_403_FORBIDDEN,
    HTTP_500_INTERNAL_SERVER_ERROR,
)

from fitness_studio.response import ErrorResponse

from rest_framework.exceptions import APIException

error_logger = logging.getLogger("error_logger")
request_logger = logging.getLogger("request_logger")

class CustomExceptionHandler(object):
    """
    Custom Exception Handler
    """

    def __new__(self, exc, context):
        request_data = {}
        req = context.get("request")
        if req:
            path = req.path
            method = req.method
           
            request_data["data"] = getattr(req, "_data", {})
            request_data["query"] = req.query_params.dict()
        else:
            path = "N/A"
            method = "N/A"
            request_data = {}

       
        request_logger.info(str(request_data))

       
        
        response = exception_handler(exc, context)
        if response is not None:
            status_code = response.status_code
        else:
            status_code = HTTP_500_INTERNAL_SERVER_ERROR

        error_logger.error(
            f"API: {path} | Method: {method} | Status Code: {status_code} | Error: {str(exc)}"
        )
        if response is not None:
            if response.status_code == HTTP_401_UNAUTHORIZED:
                message = "Unauthorized: Access is denied."
            elif response.status_code == HTTP_403_FORBIDDEN:
                return ErrorResponse(
                    status_code=HTTP_401_UNAUTHORIZED, message=str(exc)
                )
            else:
                try:
                    message = str(exc.detail.get("non_field_errors")[0])
                except Exception as e:
                    error_logger.error(e) 
                    message = str(exc)
            return ErrorResponse(
                status_code=response.status_code, message=message
            )

        return ErrorResponse(
            message="Server is facing technical difficulties, Please try after some time.",
            status_code=HTTP_500_INTERNAL_SERVER_ERROR,
        )
