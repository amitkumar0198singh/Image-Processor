from django.urls import path
from .views import UploadCSV, CheckStatus


urlpatterns = [
    path('upload-csv/', UploadCSV.as_view(), name='upload_csv'),
    path('check-status/', CheckStatus.as_view(), name='check_status'),
]