from flask import Flask, request, jsonify, render_template, send_file
from flask_cors import CORS
import face_detect
import violencedetection_video
from PIL import Image
import numpy as np
import cv2
import os

app = Flask(__name__)
CORS(app)
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

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

@app.route('/create_mosaic', methods=['POST'])
def create_mosaic():
    try:
        # 獲取使用者權限等級
        user_permission = request.form['user_permission']
        # 獲取上傳的影片檔案
        uploaded_file = request.files['video_file']
        # 檢查檔案是否為空
        if uploaded_file.filename == '':
            return jsonify({'error': 'No file selected.'}), 400
        # 保存上傳的影片檔案
        video_path = os.path.join(app.config['UPLOAD_FOLDER'], uploaded_file.filename)
        uploaded_file.save(video_path)
        # 調用 create_mosaicvideo 函數來處理影片
        output_video_path = create_mosaicvideo(user_permission, video_path)
        # 返回處理後的影片
        return send_file(output_video_path, as_attachment=True)
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
#Run the script with $flask run -h 172.31.114.168
if __name__ == '__main__':
    app.run(debug=True)
