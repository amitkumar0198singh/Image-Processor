import requests

from django.conf import settings
from django.urls import reverse

from celery import shared_task

from . import image_compression_service
from .models import ProductImage, ImageProcessingRequest
from .enums import ProcessingStatus



@shared_task(bind=True, autoretry_for=(Exception,), retry_backoff=3, max_retries=5)
def process_image(self, request_id):
    process_request = ImageProcessingRequest.objects.get(request_id=request_id)
    images = ProductImage.objects.filter(request=process_request)

    process_request.status = ProcessingStatus.PROCESSING.value
    process_request.save()
    processsing_failed = False
    for image in images:
        input_image_urls = image.input_image_urls.split(',')
        output_urls = image_compression_service.get_compressed_image_url(input_image_urls)
        if None in output_urls:
            processsing_failed = True
        image.output_image_urls = ','.join(filter(None, output_urls))
        image.save()
        print(f"Updated Product Image ID {image.id} with URLs: {image.output_image_urls}")
    if processsing_failed:
        process_request.status = ProcessingStatus.FAILED.value
    else:
        process_request.status = ProcessingStatus.COMPLETED.value
    process_request.save()
    print({'status': not processsing_failed, 'message': "Image processing completed" \
            if not processsing_failed else "Some images failed to process"})