##使用"自定義的權重檔"，對"圖片"進行預測，可輸出暴力物件座標，也可以將暴力物件馬賽克圖片輸出。
#使用前請確認有適當安裝以下兩個套件
#pip install ultralytics
#pip install yolov5
import os
from ultralytics import YOLO
from PIL import Image, ImageDraw

# 控制使用者是否能存取暴力物件
def filter_forbidden_objects(user_level, object_list):
    if user_level == 0:
        return object_list
    else:
        return []

# 針對禁止物件進行馬賽克
def put_mosaic(image, forbidden_object_coordinates):
    # 複製原始圖像
    image_copy = image.copy()

    # 遍歷邊界框列表
    for box in forbidden_object_coordinates:
        # 提取座標值
        x_min, y_min, x_max, y_max = box['xmin'], box['ymin'], box['xmax'], box['ymax']

        # 將座標值轉換為整數
        x_min, y_min, x_max, y_max = int(x_min), int(y_min), int(x_max), int(y_max)

        # 提取要進行馬賽克的區域
        mosaic_region = image_copy.crop((x_min, y_min, x_max, y_max))

        # 縮小馬賽克區域
        scale_factor = 0.05
        small_mosaic = mosaic_region.resize((round((x_max - x_min) * scale_factor), round((y_max - y_min) * scale_factor)), Image.NEAREST)

        # 放大馬賽克區域
        enlarge_factor = 1.5
        enlarge_size = round((x_max - x_min) * (enlarge_factor - 1) / 2)
        enlarged_mosaic = small_mosaic.resize((x_max - x_min + 2 * enlarge_size, y_max - y_min + 2 * enlarge_size), Image.NEAREST)

        # 將馬賽克區域放回原始圖像
        image_copy.paste(enlarged_mosaic, (x_min - enlarge_size, y_min - enlarge_size))
        
    # 移除預測的紅線框
    draw = ImageDraw.Draw(image_copy)
    draw.rectangle((0, 0, image.width, image.height), outline=(0, 0, 0), width=0)
        
    return image_copy

# 使用者等級，默認為0
user_level = 0

# 載入預訓練的 YOLOv5s 模型
model = YOLO('20230714yolov5.pt')

# 定義圖片檔案的路徑
image_path = 'violencetest4.png'

# 在圖片上執行推論
results = model.predict(image_path)  # 在圖片上執行預測

# 處理預測結果
for r in results:
    im_array = r.plot()  # 將預測結果畫成 BGR 格式的 numpy 陣列
    im = Image.fromarray(im_array[..., ::-1])  # 轉換為 RGB 格式的 PIL 影像
    
    boxes = r.boxes.xyxy.cpu().numpy()  # 取得 xyxy 格式的框線座標，並轉換為 CPU 上的 numpy 陣列

    # 創建一個包含被屏蔽物件座標的列表
    forbidden_object_coordinates = []

    for i, box in enumerate(boxes):
        # 提取框線座標
        x_min, y_min, x_max, y_max = map(int, box[:4])

        # 添加框線座標到屏蔽列表中
        forbidden_object_coordinates.append({'xmin': x_min, 'ymin': y_min, 'xmax': x_max, 'ymax': y_max})

    # 對影像進行馬賽克處理
    im_mosaic = put_mosaic(im, forbidden_object_coordinates)
    
    # 顯示馬賽克影像
    im_mosaic.show()

    # 儲存馬賽克影像
    save_path = os.path.join('/output/', f'mosaic_{i}.png')
    im_mosaic.save(save_path)
    
# 調用存取控制方法
forbidden_object_indices = filter_forbidden_objects(user_level, forbidden_object_coordinates)

# 印出座標清單
for i, coordinates in enumerate(forbidden_object_indices):
    x_min, y_min, x_max, y_max = coordinates.values()
    print(f'Box {i + 1}: x_min: {x_min}, y_min: {y_min}, x_max: {x_max}, y_max: {y_max}')