import csv, uuid, requests

from django.conf import settings

from . import exceptions
from .tasks import process_image
from .models import ImageProcessingRequest, ProductImage
from .serializers import ProductImageSerializer


def get_processing_request(request_id):
    try:
        return ImageProcessingRequest.objects.get(request_id=str(request_id))
    except ImageProcessingRequest.DoesNotExist:
        raise exceptions.DataNotFoundException(f"Process request not found with request id {request_id}")
    

def get_all_images(process_request: ImageProcessingRequest):
    images = ProductImage.objects.filter(request=process_request)
    image_serializer = ProductImageSerializer(images, many=True)
    return image_serializer.data



def compress_images(csv_file):
    decoded_file = csv_file.read().decode('utf-8').splitlines()
    reader = csv.reader(decoded_file)
    request_id = str(uuid.uuid4())
    image_request = ImageProcessingRequest.objects.create(request_id=request_id)
    next(reader, None)
    product_data = {}
    for row in reader:
        if len(row) < 3:
            continue
        product_name, input_image_urls = row[1], row[2]
        urls = [url.strip() for url in input_image_urls.split(',')]
        if product_name in product_data:
            product_data[product_name].extend(urls)
        else:
            product_data[product_name] = urls
    for product_name, urls in product_data.items():
        ProductImage.objects.create(request=image_request, product_name=product_name, 
                                    input_image_urls=','.join(urls))
    print(f"Celery Task Started for Request ID: {request_id}")
    task = process_image.delay(request_id)  # Start processing images
    print(f"Celery Task ID: {task.id}")
    return {'status': True, 'message': "Image processing has been started", 'request_id': request_id}


def send_webhook(request_id):
    process_request = get_processing_request(request_id)
    images = get_all_images(process_request)
    webhook_data = {'request_id': request_id, 'status': process_request.status, 'images': images}
    response = requests.post(url=settings.WEBHOOK_URL, json=webhook_data, timeout=10)
    if response.status_code == 200:
        return {'status': True, 'message': f'Webhook sent successfully for Request ID: {request_id}'}
    return {'status': False, 'message': f'Error occured sending webhook of Request ID: {request_id}'}

