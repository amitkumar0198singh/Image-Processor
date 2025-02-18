from rest_framework.response import Response
from rest_framework import views, status

from .services import get_processing_request
from .utils import compress_images

from .serializers import UploadCSVSerializer


# Create your views here.
class UploadCSV(views.APIView):
    def post(self, request):
        serializer = UploadCSVSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        response = compress_images(serializer.validated_data.get('csv_file'))
        return Response(response, status=status.HTTP_202_ACCEPTED)
    

class CheckStatus(views.APIView):
    def get(self, request):
        request_id = request.GET.get('request_id')
        process_request = get_processing_request(str(request_id))
        print(process_request)
        return Response({'status': True, 'image_status': process_request.status}, 
                        status=status.HTTP_200_OK)