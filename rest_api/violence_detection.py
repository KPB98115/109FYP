##此程式碼設計為輸入截圖並預測暴力物件，根據使用者授權狀況，輸出暴力物件預測座標。
#最後編輯時間為:2023/08/21 21:46 By Lynn
# 使用前請確認有適當安裝以下兩個套件
# pip install ultralytics
# pip install yolov5
import os
from ultralytics import YOLO
from PIL import Image, ImageDraw
import base64

class YOLOv5_singleton:
    _instance = None
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(YOLOv5_singleton, cls).__new__(cls)
            cls._instance.model = YOLO('20230714yolov5.pt')
        return cls._instance

# 控制使用者是否能存取暴力物件
def filter_forbidden_objects(user_level, object_list):
    if user_level == 0:
        return object_list
    else:
        return []

# 將 base64 字符串保存為圖片檔案
def save_base64_string_as_image(base64_string):
    dirname = os.path.dirname(__file__)
    # 移除 base64 字符串中的 data 屬性
    index = base64_string.find(',') + 1
    base64_string = base64_string[index:]
    # 解碼 base64 圖片
    image_data = base64.b64decode(base64_string)
    with open(os.path.join(dirname, "screenshot.jpg"), "wb") as file:
        file.write(image_data)
    return "screenshot.jpg"

# 將座標清單整理為整數，並作為返回值
def get_forbidden_object_coordinates(indices):
    coordinates_list = []
    for coordinates in indices:
        x_min, y_min, x_max, y_max = coordinates.values()
        coordinates_list.append({'xmin': int(x_min), 'ymin': int(y_min), 'xmax': int(x_max), 'ymax': int(y_max)})
    return coordinates_list

def violence_detection(base64_image, user_level = 0):
    try:

        # 載入預訓練的 YOLOv5s 模型(此處可以替換自定義的權重檔)
        model = YOLOv5_singleton()

        # 假設 base64_image 是您的 base64 圖片字符串
        image = save_base64_string_as_image(base64_image)

        # 在圖片上執行推論
        results = model.predict(image)  # 在圖片上執行預測

        # 創建一個包含被屏蔽物件座標的列表
        forbidden_object_coordinates = []

        # 處理預測結果
        for r in results:
            boxes = r.boxes.xyxy.cpu().numpy()  # 取得 xyxy 格式的框線座標，並轉換為 CPU 上的 numpy 陣列

            for box in boxes:
                # 提取框線座標
                x_min, y_min, x_max, y_max = map(int, box[:4])

                # 添加框線座標到屏蔽列表中
                forbidden_object_coordinates.append({'xmin': x_min, 'ymin': y_min, 'xmax': x_max, 'ymax': y_max})

        # 調用存取控制方法
        forbidden_object_indices = filter_forbidden_objects(user_level, forbidden_object_coordinates)

        # 獲取被屏蔽物件座標清單(整數)
        forbidden_coordinates_list = get_forbidden_object_coordinates(forbidden_object_indices)

        # 返回整數座標清單
        forbidden_coordinates_list
    
    except Exception as error:
          print("Failed extract coordinates:" + str(error))
          return []
