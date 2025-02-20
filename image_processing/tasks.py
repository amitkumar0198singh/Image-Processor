import requests

from django.conf import settings

from celery import shared_task

from .models import ProductImage, ImageProcessingRequest
from .enums import ProcessingStatus



@shared_task(bind=True, autoretry_for=(Exception,), retry_backoff=3, max_retries=5)
def process_image(self, request_id):
    process_request = ImageProcessingRequest.objects.get(request_id=request_id)
    images = ProductImage.objects.filter(request=process_request)

    try:
        process_request.status = ProcessingStatus.PROCESSING.value
        process_request.save()

        for image in images:
            input_image_urls = image.input_image_urls.split(',')
            output_urls = []
            for url in input_image_urls:
                response = requests.post(settings.COMPRESS_IMAGE_URL, json={'image_url': url})
                if response.status_code == 201:
                    output_urls.append(response.json().get('compressed_image_url'))
                else:
                    print(f"Failed to process image: {url}")
                    output_urls.append(None)
            print(output_urls)
            image.output_image_urls = ','.join(filter(None, output_urls))
            image.save()
            print(f"Updated Product Image ID {image.id} with URLs: {image.output_image_urls}")
        process_request.status = ProcessingStatus.COMPLETED.value
        process_request.save()
        return {'status': True, 'message': "Image processing has been completed"}
    except Exception as e:
        process_request.status = ProcessingStatus.FAILED.value
        process_request.save()
        return {'status': False, 'message': f"Execption occurs during processing image:{e}"}
    