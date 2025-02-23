# Image Processing API

## Overview
The **Image Processing API** allows users to upload a CSV file containing product names and image URLs. The system processes the images by compressing them and provides an API to check the processing status. It also supports webhook notifications.

## Features
- Upload CSV file with image URLs.
- Process images by compressing them.
- Check the status of the image processing request.
- Send webhook notifications upon processing completion.
- RESTful API with OpenAPI documentation using `drf-spectacular`.

## Technologies Used
- **Django** & **Django REST Framework**
- **Celery** for asynchronous task processing
- **Redis** as the Celery message broker
- **Pillow** for image processing
- **drf-spectacular** for API schema generation

## Installation

### Prerequisites
Ensure you have the following installed:
- Python 3.12
- PostgreSQL/MySQL/SQLite (any supported Django database backend)
- Redis (for Celery)
- pipenv or virtualenv (for environment management)

### Setup
1. Clone the repository:
   ```sh
   git clone https://github.com/amitkumar0198singh/Image-Processor/
   cd Image-Processor
   ```

2. Create and activate a virtual environment:
   ```sh
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. Install dependencies:
   ```sh
   pip install -r requirements.txt
   ```

4. Apply migrations:
   ```sh
   python manage.py migrate
   ```

5. Start Redis and Celery:
   ```sh
   redis-server &
   celery -A image_processor worker --loglevel=info --pool=solo
   ```

6. Run the Django server:
   ```sh
   python manage.py runserver
   ```

## API Endpoints

### 1. Upload CSV File
**Endpoint:** `POST /image/upload-csv/`
- Uploads a CSV file containing product names and image URLs.
- **Request Body:** Multipart file upload
- **Response:**
  ```json
  {
    "status": true,
    "message": "Image processing has been started",
    "request_id": "123e4567-e89b-12d3-a456-426614174000"
  }
  ```

### 2. Check Processing Status
**Endpoint:** `GET /image/check-status/?request_id=<request_id>`
- Checks the processing status of a request.
- **Response:**
  ```json
  {
    "status": true,
    "process_request_status": "completed",
    "images": [
      {
        "product_name": "Laptop",
        "input_image_urls": ["http://example.com/image1.jpg"],
        "output_image_urls": ["http://example.com/compressed1.jpg"]
      }
    ]
  }
  ```

### 3. Send Webhook
**Endpoint:** `POST /image/send-webhook/`
- Sends a webhook notification for a completed request.
- **Request Body:**
  ```json
  {
    "request_id": "123e4567-e89b-12d3-a456-426614174000"
  }
  ```
- **Response:**
  ```json
  {
    "status": true,
    "message": "Webhook sent successfully"
  }
  ```

## Project Structure
```
image_processor/
│-- image_processing/
│   ├── models.py                # Database models for storing image requests
│   ├── serializers.py            # DRF serializers
│   ├── views.py                  # API views
│   ├── services.py               # Business logic for image processing
│   ├── tasks.py                  # Celery tasks for processing images
│   ├── urls.py                   # URL routing for APIs
│   ├── exceptions.py             # Custom exception handling
│   ├── enums.py                  # Processing status enums
│   ├── image_compression_service.py # Image compression logic
│-- image_processor/
│   ├── settings.py               # Django settings
│   ├── celery.py                 # Celery configuration
│   ├── urls.py                   # Root URL routing
│   ├── wsgi.py                   # WSGI application
│-- media/                        # Directory to store processed images
```

## Configuration
Modify the following settings in `image_processor/settings.py`:

```python
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

BASE_URL = 'http://127.0.0.1:8001'
WEBHOOK_URL = 'http://localhost:9001/webhook/'

CELERY_BROKER_URL = 'redis://localhost:6379/0'
CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'
```

## Running Celery Worker
Start Celery to process image compression tasks asynchronously:
```sh
celery -A image_processor worker --loglevel=info
```

## API Documentation
The API is documented using `drf-spectacular`.

- OpenAPI schema: [http://127.0.0.1:8001/api/schema/](http://127.0.0.1:8001/api/schema/)
- Swagger UI: [http://127.0.0.1:8001/api/schema/swagger-ui/](http://127.0.0.1:8001/api/schema/swagger-ui/)
- Redoc UI: [http://127.0.0.1:8001/api/schema/redoc/](http://127.0.0.1:8001/api/schema/redoc/)

## Contributing
1. Fork the repository
2. Create a new branch (`git checkout -b feature-branch`)
3. Commit your changes (`git commit -m 'Add new feature'`)
4. Push to the branch (`git push origin feature-branch`)
5. Open a Pull Request

## License
This project is licensed under the MIT License.

