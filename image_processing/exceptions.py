from rest_framework import status
from rest_framework.views import exception_handler
from rest_framework.response import Response



class CustomException(Exception):
    message = None
    status_code = None
    detail = None

    def __init__(self, detail=None, message=None, status_code=None):
        self.detail = detail or self.detail
        self.message = message or self.message
        self.status_code = status_code or self.status_code


class DataNotFoundException(CustomException):
    message = "Data not found"
    status_code = status.HTTP_404_NOT_FOUND




def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)
    if isinstance(exc, CustomException):
        response = Response({'message': exc.message, 'status_code': exc.status_code,
                            'detail': exc.detail}, status=exc.status_code)
    return response