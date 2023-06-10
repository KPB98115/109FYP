# YOLOv5 🚀 by Ultralytics, GPL-3.0 license
"""
Perform test request
"""

import pprint

import requests

# Changed the prot to 5001
DETECTION_URL = "http://localhost:5001/v1/object-detection/yolov5s"
IMAGE = "test.jpeg"

# Read image
with open(IMAGE, "rb") as f:
    image_data = f.read()

response = requests.post(DETECTION_URL, files={"image": image_data}).json()

pprint.pprint(response)
