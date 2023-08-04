import requests
import base64
from pathlib import Path

def main():
  URL = "http://127.0.0.1:80/screenshot_detection"
  #with open('base64_example.txt', 'r') as file:
  #  IMAGE_IN_BASE64 = file.read()
  with open('image/test.jpg', 'rb') as img:
    image = img.read()
    base64_image = base64.b64encode(image)
    base64_str = base64_image.decode('utf-8')
    response = requests.post(URL, data={'image': base64_str})
    print(response.json())

if __name__ == '__main__':
  main()