##使用"自定義的權重檔"，對"圖片"進行預測，可輸出暴力物件座標，也可以將暴力物件馬賽克圖片輸出。
#使用前請確認有適當安裝以下兩個套件
#pip install ultralytics
#pip install yolov5
##使用"自定義的權重檔"，對"圖片"進行預測，可輸出暴力物件座標。
import os
from ultralytics import YOLO
from PIL import Image, ImageDraw

# 控制使用者是否能存取暴力物件
def filter_forbidden_objects(user_level, object_list):
    if user_level == 0:
        return object_list
    else:
        return []

# 使用者等級，默認為0
user_level = 0

# 載入預訓練的 YOLOv5s 模型
model = YOLO('/content/drive/MyDrive/20230714yolov5.pt')

# 定義圖片檔案的路徑
image_path = '/content/drive/MyDrive/Colab Notebooks/violencetest/violencetest4.png'

# 在圖片上執行推論
results = model.predict(image_path)  # 在圖片上執行預測

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

# 將座標清單整理為整數，並作為返回值
def get_forbidden_object_coordinates(indices):
    coordinates_list = []
    for coordinates in indices:
        x_min, y_min, x_max, y_max = coordinates.values()
        coordinates_list.append({'xmin': int(x_min), 'ymin': int(y_min), 'xmax': int(x_max), 'ymax': int(y_max)})
    return coordinates_list

# 获取整数的被屏蔽物件座標清單
forbidden_coordinates_list = get_forbidden_object_coordinates(forbidden_object_indices)

# 返回整数座標清單
forbidden_coordinates_list
