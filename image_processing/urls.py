from django.urls import path

from .views import UploadCSV, CheckStatus, WebhookView

app_name = 'image_processing'

urlpatterns = [
    path('upload-csv/', UploadCSV.as_view(), name='upload_csv'),
    path('check-status/', CheckStatus.as_view(), name='check_status'),
    path('send-webhook/', WebhookView.as_view(), name='send_webhook'),
]