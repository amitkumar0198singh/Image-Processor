from rest_framework.response import Response
from rest_framework import status

from .models import ImageProcessingRequest



def get_processing_request(request_id):
    try:
        return ImageProcessingRequest.objects.get(request_id=request_id)
    except ImageProcessingRequest.DoesNotExist:
        return None
    

