##包含模型預測、簡易存取控制和特定物件屏蔽
import torch
from PIL import Image
from yolov5 import detect
import base64

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
def get_coordinates(base64_image, user_level = 0):
  try:
    # Remove the data attribute from the string
    index = base64_image.find(',') + 1
    base64_image = base64_image[index:]
    # 控制清單
    control_list = {"car": 0, "person": 1, "gun": 2, "knife": 2, "blood": 3}
    # 調用函數獲取預測结果
    model = torch.hub.load('ultralytics/yolov5', 'yolov5s')
    image = base64.b64decode(base64_image)
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
    return get_forbidden_object_coordinates(forbidden_object_indices, object_list)

  except Exception as error:
    print("Failed extract coordinates:" + str(error))
    return []

