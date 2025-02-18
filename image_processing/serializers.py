import os

from rest_framework import serializers
from .models import ImageProcessingRequest


class UploadCSVSerializer(serializers.Serializer):
    csv_file = serializers.FileField()
    
    def validate_csv_file(self, data):
        extension = os.path.splitext(data.name)[1].lower()
        if extension != '.csv':
            raise serializers.ValidationError({'error': "Only CSV files are allowed"})
        if data.content_type not in ['text/csv', 'application/vnd.ms-excel']:
            raise serializers.ValidationError({'error': "Please upload CSV file"})
        return data
        
