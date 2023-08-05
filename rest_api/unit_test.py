import unittest
from api import app
import base64

class FlaskAppTests(unittest.TestCase):
  def setUp(self):
    self.app = app.test_client()
    self.app.testing = True
    with open('image/test.jpg', 'rb') as img:
      image = img.read()
      base64_image = base64.b64encode(image)
      self.screenshot_base64 = base64_image.decode('utf-8')

  def test_authentication_response(self):
    response = self.app.post('/authentication')

    self.assertEqual(response.status_code, 200)
    self.assertEqual(response.content_type, 'application/json')

  def test_facial_authentication_response(self):
    response = self.app.post('/facial_authentication', data=self.screenshot_base64)

    self.assertEqual(response.status_code, 200)
    self.assertEqual(response.content_type, 'application/json')
  
  def test_realTime_authentication_response(self):
    response = self.app.post('/realtime_authentication', data=self.screenshot_base64)

    self.assertEqual(response.status_code, 200)
    self.assertEqual(response.content_type, 'application/json')

  def test_screen_detection_response(self):
    response = self.app.post('/screenshot_detection', data=self.screenshot_base64)

    self.assertEqual(response.status_code, 200)
    self.assertEqual(response.content_type, 'application/json')

if __name__ == '__main__':
  unittest.main()