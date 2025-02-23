from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import ImageProcessingRequest
from .services import send_webhook
from .enums import ProcessingStatus


@receiver(post_save, sender=ImageProcessingRequest)
def trigger_webhook_on_status_change(sender, instance, **kwargs):

    if instance.status in [ProcessingStatus.COMPLETED.value, ProcessingStatus.FAILED.value]:
        send_webhook(instance.request_id)