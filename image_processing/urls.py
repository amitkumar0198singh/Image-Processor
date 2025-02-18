from django.urls import path
from .views import UploadCSV


urlpatterns = [
    path('upload-csv/', UploadCSV.as_view(), name='upload_csv'),
]