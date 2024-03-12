import os
from base64 import b64decode
from io import BytesIO
import face_recognition as faceRec
import util

DIR_NAME = os.path.dirname(__file__)

def regist(username: str, password: str, image: str) -> bool:
  b64_image = b64decode(image)
  file_image = BytesIO(b64_image)
  with open(os.path.join(f'{DIR_NAME}/image/valid_profile_pic', f'{username}.jpg'), "wb") as file:
    file.write(b64_image)
  image_path = f'{DIR_NAME}/image/valid_profile_pic/{username}.jpg'
  np_image = faceRec.load_image_file(file_image)
  landmarks = faceRec.face_landmarks(np_image)
  result = util.addUser(username, image_path, np_image, landmarks)
  return result