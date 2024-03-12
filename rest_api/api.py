from flask import Flask, request, jsonify, render_template, send_file
from flask_cors import CORS
import face_detect
import os
from video_detection import create_mosaicvideo
from registration import regist
from pathlib import Path

app = Flask(__name__)
CORS(app)
DIR_NAME = os.path.dirname(__file__)

#Initialize valid user images
initial_users_image = ["kingston.jpg", "eva.jpg", "ling.jpg", "hebby.jpg", "lynn.jpg"]
dir = Path("image/valid_profile_pic")
for file in dir.iterdir():
  if file.is_file() and file.name not in initial_users_image:
    file.unlink()
print("System initialization: initialized all valid profile image")

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
      is_restricted = result[3]
      return {
          "auth": is_authenticated,
          "user": user,
          "status": status,
          "isRestricted": is_restricted,
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
      cachedImagePath = os.path.join(f'{DIR_NAME}/image/cache', f'{userID}.jpg')
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
    video_path = os.path.join(f'{DIR_NAME}/static/videos', uploaded_file.filename)
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
    for filename in os.listdir(f'{DIR_NAME}/static/previews'):
      if filename != '.DS_Store':
        with open(os.path.join(f'{DIR_NAME}/static/previews', filename), 'rb') as file:
          images_response[os.path.basename(file.name)] = f'static/previews/{filename}'
          #images_response[os.path.basename(file.name)] = base64.b64encode(file.read()).decode('utf-8')
          # Output: {'filename': base64_string, ...}
    return jsonify(images_response)
  except Exception as e:
    return jsonify({'error': str(e)}), 500
  
@app.route('/registration', methods=['POST'])
def registration():
  try:
    username = request.form['username']
    password = request.form['password']
    image = request.form['image']
  except Exception as e:
    print("Error: ", e)

  try:
    result = regist(username, password, image)
    if result:
      print("Registration successful")
      return True
    else:
      print("Registration failed")
      return False
  except Exception as e:
    print("Error: ", e)
    return False

#Run the script with $flask --app api run --host=172.31.114.168
if __name__ == '__main__':
  app.run(debug=True, host='0.0.0.0')
