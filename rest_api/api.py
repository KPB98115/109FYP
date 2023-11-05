from flask import Flask, request, jsonify, render_template, send_file
from flask_cors import CORS
import face_detect
from violencedetection_video import create_mosaicvideo
from PIL import Image
import numpy as np
import cv2
import Yoloviolencedetection
import os
import base64
from video_detection import create_mosaicvideo

app = Flask(__name__)
CORS(app)
dir_name = os.path.dirname(__file__)

@app.route('/', methods=['GET'])
def welcome():
  return '''<h1>109 FYP</h1>'''

@app.route('/template', methods=['GET'])
def template():
  return render_template('index.html', video_src1 = '', video_src2 = '', video_src3 = '')

@app.route('/authentication', methods=['POST'])
def authentication():
  return {
    'auth': True, 'user': 'root', 'status': 'Welcome, root user'
  }

@app.route('/facial_authentication', methods=['POST'])
def faical_authentication():
  # Read the image from the HTTP request
  print('Processing faical detection')
  imageData = request.form['image']

  try:
    # Perform facial recognition and return the result
    # The result should either be Boolean or List object
    result = face_detect.detection(imageData)
    if type(result) is list:
      user = result[0]
      is_authenticated = result[1]
      status = result[2]
      return {
          "auth": is_authenticated,
          "user": user,
          "status": status
      }
    else:
      return {
        "auth": False,
          "user": '',
          "status": 'No valid user detected'
      }
  except Exception as error:
    print(str(error))
    return {
      "auth": False,
      "user": "",
      "status": str(error)
    }
  
@app.route('/realtime_authentication', methods=['POST'])
def realtime_authentication():
  # Read the image from the HTTP request
  try:
    formData = request.form['image']
    userID = request.form['username']
  except KeyError as keyerror:
    print(str(keyerror))
    return {'auth': False, 'status': 'formData not found'}

  try:
    # Perform facial recognition and return the result as a boolean value
    result = face_detect.realtime_detection(userID, formData)
    print(type(result))
    if result:
      print('Status: Access granted')
      return {'auth': result, 'status': ''}
    print('Status: Access declined, ')
    return {'auth': result, 'status': ''}
  except Exception as error:
    print(str(error))

@app.route('/video_pixelation', methods=['POST'])
def video_pixelation():
  try:
    # 獲取使用者權限等級
    user_permission = request.form['permission']
    # 獲取上傳的影片檔案
    uploaded_file = request.files.get('file')
    # 檢查檔案是否為空
  except:
    return jsonify({'error': 'No file founded.'}), 400
  try:
    # 保存上傳的影片檔案
    video_path = os.path.join(dir_name, uploaded_file.filename)
    uploaded_file.save(video_path)
    # 調用 create_mosaicvideo 函數來處理影片
    create_mosaicvideo(user_permission, video_path)
    return None
  except Exception as e:
    return jsonify({'error': str(e)}), 500
  
@app.route('/get_previewImage', methods=['GET'])
def get_previewImage():
  try:
    images_response = {}
    for filename in os.listdir(f'{dir_name}/image/previews'):
      with open(os.path.join(f'{dir_name}/image/previews', filename), 'rb') as file:
        images_response[os.path.basename(file.name)] = base64.b64encode(file.read()).decode('utf-8')
        # Output: {'filename': base64_string, ...}
    return jsonify(images_response)
  except Exception as e:
    return jsonify({'error': str(e)}), 500

@app.route('/get_media', methods=['GET'])
def get_media():
  try:
    # 獲取輸入的影片名稱
    #video_name = request.form('video_name')
    video_name = request.args['title']
    # 構造 _mosaic.mp4 文件的完整路徑
    pixelate_video_path = os.path.join(f'{dir_name}/static', video_name)
    # 檢查文件是否存在
    if os.path.exists(pixelate_video_path):
      # 返回 _mosaic.mp4 文件
      return send_file(pixelate_video_path, as_attachment=True, download_name=video_name)
    else:
      return jsonify({'error': 'pixelate video not found.'}), 404
  except Exception as e:
    return jsonify({'error': str(e)}), 500

#Run the script with $flask --app api run --host=172.31.114.168
if __name__ == '__main__':
  app.run(debug=True)
