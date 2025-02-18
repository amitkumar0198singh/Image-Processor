import csv
import uuid

from .tasks import process_image
from .models import ImageProcessingRequest, ProductImage


def compress_images(csv_file):
    decoded_file = csv_file.read().decode('utf-8').splitlines()
    reader = csv.reader(decoded_file)
    request_id = str(uuid.uuid4())
    image_request = ImageProcessingRequest.objects.create(request_id=request_id)
    for row in reader:
        if len(row) < 3:
            continue
        product_name, input_image_urls = row[1], row[2]
        urls = input_image_urls.split(',')
        for url in urls:
            ProductImage.objects.create(request=image_request, product_name=product_name, 
                                        input_image_urls=url.strip())
    
    from celery.result import AsyncResult
    from django.conf import settings

    print(f"Redis Config: {settings.CELERY_BROKER_URL}")  # Debug Redis Config
    print(f"Starting process_image task with request_id={request_id}")

    task = process_image.delay(request_id)
    print(f"Task ID: {task.id}")
    return {'status': True, 'message': "Image processing has been started", 'request_id': request_id}