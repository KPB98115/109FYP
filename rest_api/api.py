from flask import Flask, request, jsonify, render_template, send_file
from flask_cors import CORS
import face_detect
import os
from video_detection import create_mosaicvideo

app = Flask(__name__)
CORS(app)
dir_name = os.path.dirname(__file__)

@app.route('/', methods=['GET'])
def welcome():
  return '''<h1>109 FYP</h1>'''

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
    userID = request.form['username']
    if 'image' not in request.form:
      print('Using local cache to process recognition...')
      cachedImagePath = os.path.join(f'{dir_name}/image/cache', f'{userID}.jpg')
      with open(cachedImagePath, 'rb') as file:
        # The snapshot is bytes object
        snapshot = file.read()
    else:
      # The snapshot is base64 string
      print('Using image from client request to process recognition...')
      snapshot = request.form['image']
  except FileNotFoundError as error:
    print(str(error))
    snapshot = request.form['image']

  try:
    # Perform facial recognition and return the result as a boolean value
    result = face_detect.realtime_detection(userID, snapshot)
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
    # 獲取上傳的影片檔案
    print(request.files)
    uploaded_file = request.files.get('file')
  except:
    return jsonify({'error': 'No file founded.'}), 400
  try:
    # 保存上傳的影片檔案
    video_path = os.path.join(f'{dir_name}/static/videos', uploaded_file.filename)
    uploaded_file.save(video_path)
    # 調用 create_mosaicvideo 函數來處理影片
    create_mosaicvideo(video_path, uploaded_file.filename)
    print('video pixelation successfully.')
  except Exception as e:
    return jsonify({'error': str(e)}), 500
  
@app.route('/get_previewImage', methods=['GET'])
def get_previewImage():
  try:
    images_response = {}
    for filename in os.listdir(f'{dir_name}/static/previews'):
      with open(os.path.join(f'{dir_name}/static/previews', filename), 'rb') as file:
        images_response[os.path.basename(file.name[:-4])] = f'static/previews/{filename}'
        #images_response[os.path.basename(file.name)] = base64.b64encode(file.read()).decode('utf-8')
        # Output: {'filename': base64_string, ...}
    return jsonify(images_response)
  except Exception as e:
    return jsonify({'error': str(e)}), 500

<<<<<<< Updated upstream
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

@app.route('/yoloviolencedetection', methods=['POST'])
def yoloviolence_detection():
  try:
    #userID = request.form['user']
    screenshot_in_base64 = request.form['screenshot']
    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
      future = executor.submit(yoloviolencedetection.get_coordinates, screenshot_in_base64, user_level = 0)
    result = future.result()
    print(result)
    return jsonify(result)
  except Exception as error:
        print("Error in yoloviolence_detection:", str(error))
        return jsonify({'error': str(error)}), 500

=======
>>>>>>> Stashed changes
#Run the script with $flask --app api run --host=172.31.114.168
if __name__ == '__main__':
  app.run(debug=True)
