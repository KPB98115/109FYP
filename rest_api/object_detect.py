##包含模型預測、簡易存取控制和特定物件屏蔽
import os
import torch
from PIL import Image
from yolov5 import detect
from torchvision import transforms
import io

def save_base64_string_as_image(binary_image):
  dirname = os.path.dirname(__file__)
  with open(os.path.join(dirname, "screenshot.jpg"), "wb") as file:
    file.write(binary_image)
  return "screenshot.jpg"

# 完成預測並存取控制
def filter_forbidden_objects(user_level, object_list, control_list):
  forbidden_object_indices = []

  for i, obj in enumerate(object_list):
    object_name = obj['name']
    object_level = control_list.get(object_name, 0)

    if user_level < object_level:
        forbidden_object_indices.append(i)

  return forbidden_object_indices

def get_forbidden_object_coordinates(forbidden_object_indices, object_list):
  forbidden_object_coordinates = []

  for index in forbidden_object_indices:
    obj = object_list[index]
    coordinates = {
        'xmin': obj['xmin'],
        'ymin': obj['ymin'],
        'xmax': obj['xmax'],
        'ymax': obj['ymax']
    }
    forbidden_object_coordinates.append(coordinates)

  return forbidden_object_coordinates

# Default user level is 0
def get_coordinates(binary_image, user_level = 0):
  try:
    # 控制清單
    control_list = {"car": 0, "person": 1, "gun": 2, "knife": 2, "blood": 3}
    # 調用函數獲取預測结果
    model = torch.hub.load('ultralytics/yolov5', 'yolov5s')
    image = save_base64_string_as_image(binary_image)
    results = model(image)
    # 提取物件名稱和座標
    pred_classes = results.pandas().xyxy[0]['name']
    pred_boxes = results.pandas().xyxy[0][['xmin', 'ymin', 'xmax', 'ymax']]
    # 建構物件清單
    object_list = []
    for i in range(len(pred_classes)):
      obj = {
          'name': pred_classes[i],
          'xmin': pred_boxes.iloc[i]['xmin'],
          'ymin': pred_boxes.iloc[i]['ymin'],
          'xmax': pred_boxes.iloc[i]['xmax'],
          'ymax': pred_boxes.iloc[i]['ymax']
      }
      object_list.append(obj)
    forbidden_object_indices = filter_forbidden_objects(user_level, object_list, control_list)
    result = get_forbidden_object_coordinates(forbidden_object_indices, object_list)
    os.remove('screenshot.jpg')
    return result

  except Exception as error:
    print("Failed extract coordinates.")
    return []

# Remark(2023/07/18): Modified the code from script to module, it can be called as module in api.py
# src: https://github.com/KPB98115/109FYP/blob/main/colob_tutorial/yolov5_detect%26AC%26mosaic.ipynb