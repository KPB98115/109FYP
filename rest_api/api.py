from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import face_detect
import object_detect
from PIL import Image
import numpy as np
import cv2
import yoloviolencedetection

app = Flask(__name__)
CORS(app)

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

@app.route('/yoloviolencedetection', methods=['POST'])
def yoloviolence_detection():
  try:
    #userID = request.form['user']
    screenshot_in_base64: str = request.form['screenshot']
    result = yoloviolencedetection.get_coordinates(screenshot_in_base64, user_level=0)
    #result = object_detect.get_coordinates(screenshot_in_base64, user_level=0)
    print(result)
    return jsonify(result)
  except Exception as error:
      print("Error in yoloviolence_detection:", str(error))
      return jsonify({'error': str(error)}), 500
    
#Run the script with $flask run -h 172.31.114.168
if __name__ == '__main__':
    app.run(debug=True)
