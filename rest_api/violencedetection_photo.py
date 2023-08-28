# -*- coding: utf-8 -*-
"""
Created on Mon Aug 28 12:06:03 2023

@author: 88693
"""

from ultralytics import YOLO
from PIL import Image

# Load a pretrained YOLOv8n model
model = YOLO('model_- 17 july 2023 14_48.pt')

# Define path to image file
image_path = "C://Users//88693//Desktop//fight3.jpg"

results = model.predict(image_path)

# Show the results
for r in results:
    im_array = r.plot()  # plot a BGR numpy array of predictions
    im = Image.fromarray(im_array[..., ::-1])  # RGB PIL image
    boxes = r.boxes.xyxy.cpu().numpy()
    print(r.boxes)                                              # print boxes
    im.save("C://Users//88693//Desktop//fight3_test.jpg")  # save image