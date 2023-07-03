from flask import Flask, request, jsonify
from flask_cors import CORS
import face_detect
from PIL import Image
import numpy as np
import cv2


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

@app.route('/faical_authentication', methods=['POST'])
def faical_authentication():
  # Read the image from the HTTP request
  print('Processing faical detection')
  imageData = request.form['image']

  try:
    # Perform facial recognition and return the result
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
  
@app.route('/realtime_authenticate', methods=['POST'])
def recognition():
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
    if result:
      print('Status: Access granted')
      return {'auth': result, 'status': 'Access granted'}
    print('Status: Access delined, ')
    return {'auth': result, 'status': 'Access delined'}
  except Exception as error:
    print(str(error))

@app.route('/screenshot_detection', methods=['POST'])
def delection():
  user = request.form['user']
  screenshot_in_base64 = request.form['snapshot']
  # Process the object detection
  return {'p1': 0, 'p2': 0};

#Run the script with $flask run -h {device ip-address}
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')