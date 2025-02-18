import os
import requests

from io import BytesIO
from PIL import Image

from celery import shared_task
from .services import get_processing_request

from .models import ImageProcessingRequest, ProductImage
from .enums import ProcessingStatus



@shared_task(bind=True, autoretry_for=(Exception,), retry_backoff=3, max_retries=5)
def process_image(self, request_id):
    process_request = get_processing_request(request_id)
    images = ProductImage.objects.filter(request=process_request)

    try:
        process_request.status = ProcessingStatus.PROCESSING.value
        process_request.save()

        for image in images:
            input_image_urls = image.input_image_urls.split(',')
            output_urls = []
            for url in input_image_urls:
                try:
                    response = requests.get(url.strip(), stream=True, timeout=10)
                    if response.status_code == 200:
                        img = Image.open(BytesIO(response.content))
                        output_dir = 'media/output'
                        os.makedirs(output_dir, exist_ok=True)
                        output_path = f"{output_dir}/{os.path.basename(url.strip())}"
                        img.save(output_path, quality=50)
                        output_urls.append(output_path)
                    else:
                        output_urls.append(None)
                except Exception as e:
                    output_urls.append(None)
            image.output_urls = ','.join(filter(None, output_urls))
            image.save()
        process_request.status = ProcessingStatus.COMPLETED.value
        process_request.save()
        return {'status': True, 'message': "Image processing has been completed"}
    except Exception as e:
        process_request.status = ProcessingStatus.FAILED.value
        process_request.save()
        return {'status': False, 'errors': f"Execption occurs during processing image:{e}"}
    