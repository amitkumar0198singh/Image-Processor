import csv
import uuid

from rest_framework.response import Response
from rest_framework import views, status

from .models import ImageProcessingRequest, ProductImage
from .serializers import UploadCSVSerializer
from .tasks import process_image


# Create your views here.
class UploadCSV(views.APIView):
    def post(self, request):
        serializer = UploadCSVSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        csv_file = serializer.validated_data.get('csv_file')
        decoded_file = csv_file.read().decode('utf-8').splitlines()
        reader = csv.reader(decoded_file)

        request_id = str(uuid.uuid4())
        image_request = ImageProcessingRequest.objects.create(request_id=request_id)

        for row in reader:
            if len(row) < 3:
                continue
            product_name, input_urls = row[1], row[2]
            urls = input_urls.split(',')
            for url in urls:
                ProductImage.objects.create(request=image_request, product_name=product_name, 
                                            input_urls=url.strip())
        process_image.delay(request_id)
        return Response({
            'status': True, 'message': "Image processing has been started", 'request_id': request_id
        }, status=status.HTTP_202_ACCEPTED)