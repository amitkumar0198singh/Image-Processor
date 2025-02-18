import os

import requests
from io import BytesIO
from PIL import Image

from celery import shared_task
from .models import ImageProcessingRequest, ProductImage
from .enums import ProcessingStatus


@shared_task(bind=True, autoretry_for=(Exception,), retry_backoff=3, max_retries=5)
def process_image(request_id):
    images = ProductImage.objects.filter(request__request_id=request_id)
    process_request = ImageProcessingRequest.objects.get(request_id=request_id)

    try:
        process_request.status = ProcessingStatus.PROCESSING.value
        process_request.save()

        processed_images = []
        for image in images:
            response = requests.get(image.input_url)
            if response.status_code == 200:
                img = Image.open(BytesIO(response.content))
                output_path = f"media/output/{os.path.basename(image.input_url)}"
                img.save(output_path, quality=50)
                image.output_url = output_path
                image.save()
                processed_images.append(output_path)
        process_request.status = ProcessingStatus.COMPLETED.value
        process_request.save()
        return {'status': True, 'processed_images': processed_images}
    except Exception as e:
        process_request.status = ProcessingStatus.FAILED.value
        process_request.save()
        return {'status': False, 'errors': f"Execption occurs during processing image as {e}"}
    