from drf_spectacular.utils import extend_schema, inline_serializer, OpenApiParameter
from rest_framework import serializers
from .serializers import UploadCSVSerializer


UploadCSVResponse = inline_serializer(
    name='UploadCSVResponse',
    fields={
        'status': serializers.BooleanField(help_text='Status of the request', required=False),
        'message': serializers.CharField(help_text='Message describing the status of the request', required=False),
        'request_id': serializers.CharField(help_text='Unique identifier for the request', required=False)
    }
)


StatusSuccessResponse = inline_serializer(
    name='StatusSuccessResponse',
    fields={
        'status': serializers.BooleanField(help_text='Status of the request', required=False),
        'image_processing_status': serializers.CharField(help_text='Status of the image processing request', required=False)
    }
)

StatusFailureResponse = inline_serializer(
    name='StatusFailureResponse',
    fields={
        'status': serializers.BooleanField(help_text='Status of the request', required=False),
        'message': serializers.CharField(help_text='Error message describing why the request failed', required=False)
    }
)


SerializerValidationFailureResponse = inline_serializer(
    name='ErrorResponse',
    fields={
        'errors': serializers.ListField(
            child=serializers.CharField(),
            help_text='List of error messages describing why the request was invalid.',
            required=False
        )
    }
)



def upload_csv_schema():
    return extend_schema(
        summary="Upload CSV file",
        description="Upload a CSV file containing product name and image URIs",
        tags=['Image Processing'],
        request=UploadCSVSerializer,
        responses={
            202: UploadCSVResponse,
            400: SerializerValidationFailureResponse,
        },
    )


def check_status_schema():
    return extend_schema(
        summary="Check Status",
        description="Check the status of the image processing request",
        tags=['Image Processing'],
        parameters=[OpenApiParameter(
            type=str, 
            name='request_id',
            required=True, 
            location=OpenApiParameter.QUERY,
            description='Unique identifier for the request'
        )],
        responses={
            200: StatusSuccessResponse,
            400: StatusFailureResponse
        },
    )
