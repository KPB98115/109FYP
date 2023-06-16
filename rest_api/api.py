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
  # Read the image from the HTTP request
  if 'image' not in request.form:
    return {
       'auth': False,
       'user': "",
       'status': 'No image found'
    }
  formData = request.form['image']

  try:
    # Perform facial recognition and return the result
    result = face_detect.detection(formData)
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
  
@app.route('/face_recognition', methods=['POST'])
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
      return {'auth': result, 'Status': 'Access granted'}
    print('Status: Access delined, ')
    return {'auth': result, 'Status': 'Access delined'}
  except Exception as error:
    print(str(error))

@app.route('/screenshot_detection', methods=['POST'])
def delection():
   return 0;

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')