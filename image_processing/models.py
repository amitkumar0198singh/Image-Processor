from django.db import models
from .enums import ProcessingStatus


STATUS_CHOICES = [
    (status.value, status.name) for status in ProcessingStatus
]

# Create your models here.
class ImageProcessingRequest(models.Model):
    id = models.AutoField(primary_key=True)
    request_id = models.CharField(max_length=255, unique=True)
    status = models.CharField(max_length=255, choices=STATUS_CHOICES, 
                              default=ProcessingStatus.PENDING.value)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'image_processing_request'



class ProductImage(models.Model):
    id = models.AutoField(primary_key=True)
    request = models.ForeignKey(ImageProcessingRequest, to_field='request_id', 
                                on_delete=models.CASCADE, db_column='request')
    product_name = models.CharField(max_length=255, null=True)
    input_image_urls = models.TextField(null=True, blank=True)
    output_image_urls = models.TextField(null=True, blank=True)

    class Meta:
        db_table = 'product_image'