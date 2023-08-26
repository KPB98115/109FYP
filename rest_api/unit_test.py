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

    self.result.append("Response Data from simple authentication:", response.get_json(), "\n\tResponse time: ", self.start - time())
    self.assertEqual(response.status_code, 200)
    self.assertEqual(response.content_type, 'application/json')

  def test_facial_authentication_response(self):
    response = self.app.post('/facial_authentication', data={'image': self.base64_str, 'username': 'kingston'}, content_type='multipart/form-data')

    self.result.append("Response Data from facial authentication:", response.get_json()['status'], "\n\tResponse time: ", self.start - time())
    self.assertEqual(response.status_code, 200)
    self.assertEqual(response.content_type, 'application/json')
  
  def test_realTime_authentication_response(self):
    response = self.app.post('/realtime_authentication', data={'image': self.base64_str, 'username': 'kingston'}, content_type='multipart/form-data')

    self.result.append("Response Data from real time authentication:", response.get_json()['auth'], "\n\tResponse time: ", self.start - time())
    self.assertEqual(response.status_code, 200)
    self.assertEqual(response.content_type, 'application/json')

  def test_screen_detection_response(self):
    response = self.app.post('/screenshot_detection', data={'screenshot': self.base64_str, 'username': 'kingston'}, content_type='multipart/form-data')

    self.result.append("Response Data from screenshot detection:", int(len(response.get_json()[0])/2), "objects detected.", "\n\tResponse time: ", self.start - time())
    self.assertEqual(response.status_code, 200)
    self.assertEqual(response.content_type, 'application/json')

if __name__ == '__main__':
  unittest.main()