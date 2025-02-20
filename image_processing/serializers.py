import os

from rest_framework import serializers
from .models import ProductImage


class UploadCSVSerializer(serializers.Serializer):
    csv_file = serializers.FileField()
    
    def validate_csv_file(self, data):
        extension = os.path.splitext(data.name)[1].lower()
        if extension != '.csv':
            raise serializers.ValidationError({'error': "Only CSV files are allowed"})
        if data.content_type not in ['text/csv', 'application/vnd.ms-excel']:
            raise serializers.ValidationError({'error': "Please upload CSV file"})
        return data
        


class ProductImageSerializer(serializers.ModelSerializer):
    input_image_urls = serializers.SerializerMethodField()
    output_image_urls = serializers.SerializerMethodField()

    class Meta:
        model = ProductImage
        fields = ['product_name', 'input_image_urls', 'output_image_urls']

    def get_input_image_urls(self, image):
        if not image.input_image_urls:
            return []
        return [url.strip() for url in image.input_image_urls.split(',')]
    
    def get_output_image_urls(self, image):
        if not image.output_image_urls:
            return []
        return [url.strip() for url in image.output_image_urls.split(',')]
