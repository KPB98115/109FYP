#最後編輯時間為:2023/09/13 16:00 By Lynn
#使用"自定義的權重檔"，對"圖片"進行預測，可輸出暴力物件座標，也可以將暴力物件馬賽克圖片輸出。
#使用前請確認有適當安裝以下兩個套件
#pip install ultralytics
#pip install yolov5
##使用"自定義的權重檔"，對"圖片"進行預測，可輸出暴力物件座標。
import io
import os
from ultralytics import YOLO
from PIL import Image, ImageDraw
import base64
class YOLOv5_singleton:
    _instance = None
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(YOLOv5_singleton, cls).__new__(cls)
            cls._instance.model = YOLO('./model_- 3 september 2023 10_50.pt')
        return cls._instance
#將使用者截圖(base64)轉檔成圖片(暫未使用)    
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

# 控制使用者是否能存取暴力物件
def filter_forbidden_objects(user_level, object_list):
    if user_level == 0:
        return object_list
    else:
        return []
        
# 將座標清單整理為整數，並作為返回值
def get_forbidden_object_coordinates(indices):
    coordinates_list = []
    for coordinates in indices:
        x_min, y_min, x_max, y_max = coordinates.values()
        coordinates_list.append({'xmin': int(x_min), 'ymin': int(y_min), 'xmax': int(x_max), 'ymax': int(y_max)})
    return coordinates_list

# Default user level is 0
def get_coordinates(base64_str, user_level = 0):
    # 定義圖片檔案的路徑
    #image_path = save_base64_string_as_image(base64_image)
    # 檢查圖片是否成功保存
    #if image_path is None:
        #return []  # 或者返回其他錯誤信息
    #將使用者截圖(base64)轉檔成圖片
    try:
        # Remove the data attribute from the string
        index = base64_str.find(',') + 1
        base64_str = base64_str[index:]
        # Check for and remove null bytes
        base64_str = base64_str.replace('\x00', '')
        # Convert to JPEG format
        base64_image = base64.b64decode(base64_str)
    except Exception as error:
        print("Failed to convert image.")
        return False
    # 讀取圖像
    image = Image.open(base64_image)
    # 獲取原始圖像的寬度和高度
    original_width, original_height = image.size
    #TODO: This function should pass the original screen resolution and bounding box from yolo detection, and return the bounding box position of original image
    def scale_bounding_box_back_to_original(bounding_box_coordinates: list, original_width: int, original_height: int) -> dict:
        yolo_width: int = 0
        yolo_height: int = 0
        x_min: int = bounding_box_coordinates[0]
        y_min: int = bounding_box_coordinates[1]
        x_max: int = bounding_box_coordinates[2]
        y_max: int = bounding_box_coordinates[3]
        x_scale: int = original_width / yolo_width
        y_scale: int = original_height / yolo_height
        original_x_min: int = x_min * x_scale
        original_y_min: int = y_min * y_scale
        original_x_max:int = x_max * x_scale
        original_y_max: int = y_max * y_scale
        return { 'xmin': original_x_min, 'ymin': original_y_min, 'xmax': original_x_max, 'ymax': original_y_max }
    try:
        # 載入預訓練的 YOLOv5s 模型
        yolo_instance = YOLOv5_singleton()
        model = yolo_instance.model
        # 在圖片上執行推論
        results = model.predict(image_path)
        # 創建一個包含被屏蔽物件座標的列表
        forbidden_object_coordinates = []
        # 處理預測結果
        for r in results:
            boxes = r.boxes.xyxy.cpu().numpy()  # 取得 xyxy 格式的框線座標，並轉換為 CPU 上的 numpy 陣列
            for box in boxes:
                # 提取框線座標
                x_min, y_min, x_max, y_max = map(int, box[:4])
                # Scale the coordinates back to original positions
                coordinates_in_original = scale_bounding_box_back_to_original([x_min, y_min, x_max, y_max], original_width, original_height) #TODO: convert coordinates
                #coordinates_in_original = scale_bounding_box_back_to_original(map(int, box[:4]), original_screen_width, original_screen_height)
                # 添加框線座標到屏蔽列表中
                forbidden_object_coordinates.append({'xmin': x_min, 'ymin': y_min, 'xmax': x_max, 'ymax': y_max})
                forbidden_object_coordinates.append(coordinates_in_original) # TODO: add coordinate dict
        # 調用存取控制方法
        forbidden_object_indices = filter_forbidden_objects(user_level, forbidden_object_coordinates)
        os.remove('screenshot.png')
        return forbidden_object_indices
    except Exception as error:
        print("Failed extract coordinates:" + str(error))
        return []    
