import csv
import uuid

from .tasks import process_image
from .models import ImageProcessingRequest, ProductImage


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
        
    task = process_image.delay(request_id)
    print(f"Task ID: {task.id}")
    return {'status': True, 'message': "Image processing has been started", 'request_id': request_id}