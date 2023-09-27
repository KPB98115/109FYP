##呼叫create_mosaicvideo，輸入使用者權限等級和影片，輸出暴力物件偵測完的馬賽克影片。
#最後編輯時間:2023/09/21 22:00 
#在開始執行前，請確認安裝必要套件
#pip install ultralytics
#pip install yolov5
from ultralytics import YOLO
import cv2
import numpy as np
from PIL import Image
from io import BytesIO

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
        scale_factor = 0.04
        small_mosaic = mosaic_region.resize((round((x_max - x_min) * scale_factor), round((y_max - y_min) * scale_factor)), Image.NEAREST)

        # 放大馬賽克區域
        enlarge_factor = 1
        enlarge_size = round((x_max - x_min) * (enlarge_factor - 1) / 2)
        enlarged_mosaic = small_mosaic.resize((x_max - x_min + 2 * enlarge_size, y_max - y_min + 2 * enlarge_size), Image.NEAREST)

        # 將馬賽克區域放回原始圖像
        image_copy.paste(enlarged_mosaic, (x_min - enlarge_size, y_min - enlarge_size))

    return image_copy

def create_mosaicvideo(user_permission, video_path):
    # 載入預訓練的 YOLOv5s 模型
    model = YOLO('20230714yolov5.pt')#請在此更改欲使用之權重檔名稱，並確定路徑。
    
    # 定義影片檔案的路徑
    source = video_path
    
    # 打開影片文件
    cap = cv2.VideoCapture(source)
    
    # 獲取輸入影片的寬度和高度
    input_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    input_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    
    # 獲取輸入影片的幀率
    fps = cap.get(cv2.CAP_PROP_FPS)
    
    # 在影片上進行推論
    results = model.predict(source, stream=True)  # 在影片上執行預測，stream=True 表示以流的方式處理
    
    # 創建 VideoWriter 物件，將影片資料寫入記憶體中
    output = BytesIO()
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')  # 定義編碼方式
    out = cv2.VideoWriter(output, fourcc, fps, (input_width, input_height))
    
    # 設定馬賽克停留的幀數
    mosaic_duration_frames = int(fps * 10)  # 停留 2 秒（若 fps = 30，則為 60 幀）
    
    # 顯示結果
    frame_count = 0  # 計算目前的幀數
    mosaic_active = False  # 是否處於馬賽克模式
    
    for r in results:
        im_array = r.orig_img  # 取得原始影像的 numpy 陣列
        boxes = r.boxes.xyxy.cpu().numpy()[:, :4]  # 取得框線座標，轉換至 CPU 上的 numpy 陣列
    
        # 判斷是否進入馬賽克模式
        if not mosaic_active and len(boxes) > 0:
            mosaic_active = True
            mosaic_remaining_frames = mosaic_duration_frames
    
        if mosaic_active:
            # 對原始影像進行馬賽克處理
            im_pil = Image.fromarray(im_array)
            im_mosaic = put_mosaic(im_pil, [{'xmin': int(x_min), 'ymin': int(y_min), 'xmax': int(x_max), 'ymax': int(y_max)} for x_min, y_min, x_max, y_max in boxes])
    
            # 調整影像大小以符合輸出規格
            im_cv_resized = cv2.resize(np.array(im_mosaic), (input_width, input_height))
    
            # 寫入記憶體中的影片資料
            out.write(im_cv_resized)
    
            # 更新剩餘停留幀數
            mosaic_remaining_frames -= 1
    
            # 若停留時間結束，退出馬賽克模式
            if mosaic_remaining_frames == 0:
                mosaic_active = False
    
        else:
            # 調整影像大小以符合輸出規格
            im_cv_resized = cv2.resize(im_array, (input_width, input_height))
    
            # 寫入記憶體中的影片資料
            out.write(im_cv_resized)
    
        frame_count += 1
    
    # 關閉 VideoWriter 物件
    out.release()
    
    # 回傳記憶體中的影片資料
    output.seek(0)
    return output.getvalue()
