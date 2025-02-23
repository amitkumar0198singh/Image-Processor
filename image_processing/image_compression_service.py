import io, os, random, string, requests

from PIL import Image

from django.conf import settings


def get_random_string(length=10):
    return ''.join(random.choices(string.ascii_lowercase + string.digits, k=length))

def get_compressed_image_url(urls: list, quality=50):
    output_urls = []
    for url in urls:
        try:
            image_response = requests.get(url.strip(), stream=True, timeout=10)
            image_response.raise_for_status()
            if not image_response.headers.get('Content-Type', '').startswith('image/'):
                print(f"URL '{url}' does not point to an image")
                output_urls.append(None)
                continue
            image = Image.open(io.BytesIO(image_response.content))
            image = image.convert('RGB')

            file_name = f"{get_random_string(10)}.jpg"
            output_directory = os.path.join(settings.MEDIA_ROOT, 'output')
            os.makedirs(output_directory, exist_ok=True)
            output_path = os.path.join(output_directory, file_name)
            image.save(output_path, format='JPEG', quality=quality)
            output_image_url = f"{settings.BASE_URL}{settings.MEDIA_URL}output/{file_name}"
            output_urls.append(output_image_url)
        except Exception as e :
            print(f"Error while processing image {url}: {e}")
            output_urls.append(None)
    return output_urls