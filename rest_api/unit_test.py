import unittest
from api import app
import base64
from time import time

class FlaskAppTests(unittest.TestCase):
  def setUp(self):
    self.app = app.test_client()
    self.app.testing = True
    with open('image/test.jpg', 'rb') as img:
      image = img.read()
      base64_image = base64.b64encode(image)
      self.base64_str = base64_image.decode('utf-8')
    self.start = time()
    self.result = []

  def test_authentication_response(self):
    response = self.app.post('/authentication')

    result = "Response Data from simple authentication:" + str(response.get_json()['auth']) + "\n\tResponse time: " + str(self.start - time())
    self.result.append(result)
    self.assertEqual(response.status_code, 200)
    self.assertEqual(response.content_type, 'application/json')

  def test_facial_authentication_response(self):
    response = self.app.post('/facial_authentication', data={'image': self.base64_str, 'username': 'kingston'}, content_type='multipart/form-data')

    result = "Response Data from facial authentication:" + str(response.get_json()['status']) + "\n\tResponse time: " + str(self.start - time())
    self.result.append(result)
    self.assertEqual(response.status_code, 200)
    self.assertEqual(response.content_type, 'application/json')
  
  def test_realTime_authentication_response(self):
    response = self.app.post('/realtime_authentication', data={'image': self.base64_str, 'username': 'kingston'}, content_type='multipart/form-data')

    result = "Response Data from real time authentication:" + str(response.get_json()['auth']) + "\n\tResponse time: " + str(self.start - time())
    self.result.append(result)
    self.assertEqual(response.status_code, 200)
    self.assertEqual(response.content_type, 'application/json')
    
  #def test_screen_detection_response(self):
    #response = self.app.post('/screenshot_detection', data={'screenshot': self.base64_str, 'username': 'kingston'}, content_type='multipart/form-data')

    #result = "Response Data from screenshot detection:" + str(len(response.get_json())) + "\n\tResponse time: " + str(self.start - time())
    #self.result.append(result)
    #self.assertEqual(response.status_code, 200)
    #self.assertEqual(response.content_type, 'application/json')

  def test_create_mosaic_response(self):
    with open('violencetest1.mp4', 'rb') as video_file:
        response = self.app.post('/create_mosaic', data={'user_permission': 'admin', 'video_file': (video_file, 'violencetest1.mp4')}, content_type='multipart/form-data')
    
    result = "Response Data from create mosaic:" + str(response.headers['Content-Disposition'].split('filename=')[1].strip('"')) + "\n\tResponse time: " + str(self.start - time())
    self.result.append(result)
    self.assertEqual(response.status_code, 200)
    self.assertEqual(response.content_type, 'application/octet-stream') 
    
  def show_results(self):
    for res in self.result:
       print(res)

if __name__ == '__main__':
  unittest.main()
