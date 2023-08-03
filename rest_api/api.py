from flask import Flask, request, jsonify
from flask_cors import CORS
import face_detect
import object_detect
from PIL import Image
import numpy as np
import cv2
import concurrent.futures

app = Flask(__name__)
CORS(app)

@app.route('/', methods=['GET'])
def index():
  return '''<h1>Heelo world</h1>'''

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
  print(imageData[20:])

  try:
    # Perform facial recognition and return the result
    # Replace the facial recognition code with your own implementation
    result = face_detect.detection(imageData)
    print(result)
    user = result[0]
    is_authenticated = result[1]
    status = result[2]
    return {
        "auth": is_authenticated,
        "user": user,
        "status": status
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
    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
      future = executor.submit(face_detect.realtime_detection, userID, formData)
    # Perform facial recognition and return the result as a boolean value
    result = future.result()
    print(type(result))
    if result:
      print('Status: Access granted')
      return {'auth': result, 'status': ''}
    print('Status: Access declined, ')
    return {'auth': result, 'status': ''}
  except Exception as error:
    print(str(error))

@app.route('/screenshot_detection', methods=['POST'])
def screenshot_detection():
  #userID = request.form['user']
  screenshot_in_base64 = request.form['screenshot']
  with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
    future = executor.submit(object_detect.get_coordinates, screenshot_in_base64, user_level = 0)
  result = future.result()
  print(result)
  return jsonify(result)

#Run the script with $flask run -h 172.31.114.168
if __name__ == '__main__':
    app.run(debug=True)