import face_recognition as faceRec
import os
import cv2
import numpy as np
import util
from base64 import b64decode
from io import BytesIO

dirname = os.path.dirname(__file__)
valid_faces_names = list(util.valid_users_info.keys())

def realtime_detection(userID, image: str | bytes):
  try:
    if type(image) is str:
      print('image is str')
      binary_image = b64decode(image)
      with open(os.path.join(f'{dirname}/image/cache', f'{userID}.jpg'), "wb") as file:
        file.write(binary_image)
      file_image = BytesIO(binary_image)
      unknown_img = faceRec.load_image_file(file_image)
    else:
      print('image is bytes')
      unknown_img = faceRec.load_image_file(BytesIO(image))
    #os.remove('temp.jpg')
  except Exception as error:
    print("Failed to save image: ", error)
    return False
  try:
    is_authorized = realtime_compare_faces(unknown_img, userID)
    return is_authorized
  except Exception as error:
    print("Failed to compare with users: ", userID)
    return False
    

def detection(base64_image):
  try:
    # Save the screenshot to dictionary
    #with open(os.path.join(dirname, "image/unknown_profile_pic/unknown_user.jpg"), "wb") as file:
    #  file.write(base64_image)
    #cv2.imwrite("unknown_user.jpeg", jpeg_bytes, [int(cv2.IMWRITE_JPEG_QUALITY), 90])
    binary_data = b64decode(base64_image)
    file_image = BytesIO(binary_data)
  except Exception as error:
    print("Failed to save image: ", error)
    return ["unknown", False, str(error), False]

  # Load the valid image.
  try:
    # Load the unknown image for face recognition testing.
    print("Status: Loading unknown image")
    #unknown_image = faceRec.load_image_file(os.path.join(dirname, "image/unknown_profile_pic/unknown_user.jpg"))
    unknown_image = faceRec.load_image_file(file_image)
  except Exception as error:
    print("Error: Failed to load unknown image")
    return ["unknown", False, str(error), False]
  
  # Using the original image to compare
  print('Status: Comparing with original image...')
  # This result should be a List object
  result = login_compare_faces(unknown_image)
  print(result)
  if result[1] is False:
    increase_brightness_image = increase_brightness(unknown_image)
    second_result = login_compare_faces(increase_brightness_image)
    if second_result[1] is False:
      return login_compare_faces(merge_to_HDR(increase_brightness_image, unknown_image))
  else:
    return result

# The parameters must be numpy array
def increase_brightness(unknown_image):
  # Increase the brightness of the image
  print('Status: Comparing with brightness increased image...')
  for num in range(1, 4, 2):
    brightness = num/10
    brightness_increased_image = cv2.addWeighted(unknown_image, brightness, unknown_image, brightness, 0.0)
    return brightness_increased_image

def merge_to_HDR(brightness_increased_image, unknown_image, original_image_exposure_time=0.0303):
  # Use Merge exposures into HDR image
  print('Status: Comparing with HDR image...')
  img_list = [brightness_increased_image, unknown_image]
  merge_debevec = cv2.createMergeDebevec()
  exposure_times = np.array([original_image_exposure_time, 0.25, 0.5], dtype=np.float32).copy()
  hdr_debevec = merge_debevec.process(img_list, times=exposure_times)
  HDR_image = np.clip(hdr_debevec*255, 0, 255).astype('uint8')
  return HDR_image


def login_compare_faces(unknown_image):
  try:
    unknown_face_encoding = faceRec.face_encodings(unknown_image)[0]
  except IndexError:
    return ["", False, "I wasn't able to locate any faces in at least one of the images. Check the image files. Aborting...", False]

  print("Status: Processing static recognition...")
  # Results is an array of True/False telling if the unknown face matched anyone in the known_faces array
  # Tolerance = 0.37 seems to be proper value to recognize male and female faces.
  valid_users_encodings = []
  for user in util.valid_users_info:
    valid_users_encodings.append(util.valid_users_info[user]['encoding'])
  matches = faceRec.compare_faces(valid_users_encodings, unknown_face_encoding, tolerance=0.37)
  face_distances = faceRec.face_distance(valid_users_encodings, unknown_face_encoding)
  best_match_index = np.argmin(face_distances)
  if matches[best_match_index]:
    name = valid_faces_names[best_match_index]
    if name in util.child_users:
      return [name, True, "", True]
    return [name, True, "", False]

  print("No matching user found.")
  return ["", False, "No valid user found", False]

def realtime_compare_faces(unknown_image, valid_user=None):
  # Get the face encodings for each face in each image file
  # Since there could be more than one face in each image, it returns a list of encodings.
  # But since I know each image only has one face, I only care about the first encoding in each image, so I grab index 0.
  try:
    # Using GPU/CUDE to acclarate the face landmark process
    #batch_of_face_locations = faceRec.batch_face_locations(unknown_image)
    # Encoding the unknown image
    unknown_face_encoding = faceRec.face_encodings(unknown_image)[0]

  except IndexError:
    print("I wasn't able to locate any faces in at least one of the images. Check the image files. Aborting...")
    return False

  print("Status: Comparing...")
  print(f'valid user parameter is:{valid_user}')
  # If the valid_face parameter is not given, use the valid face encoding from util dir.
  # Otherwise use the given valid face image url.
  print("Status: Processing real time recognition...")

  """
  if valid_user == 'Kingston':
    result = faceRec.compare_faces([util.kingston_face_encodings], unknown_face_encoding, tolerance=0.37)[0]
  elif valid_user == 'Eva':
    result = faceRec.compare_faces([util.eva_face_encodings], unknown_face_encoding, tolerance=0.37)[0]
  elif valid_user == 'Ling':
    result = faceRec.compare_faces([util.ling_face_encodings], unknown_face_encoding, tolerance=0.37)[0]
  elif valid_user == 'Lynn':
    result = faceRec.compare_faces([util.lynn_face_encodings], unknown_face_encoding, tolerance=0.37)[0]
  elif valid_user == 'Hebby':
    result = faceRec.compare_faces([util.hebby_face_encodings], unknown_face_encoding, tolerance=0.37)[0]
  """
  if valid_user in util.valid_usernames:
    result = faceRec.compare_faces([util.valid_users_info[valid_user]], unknown_face_encoding, tolerance=0.37)[0]
  else:
    print("No valid user detected")
    return False
  # To convert numpy.bool_ to boolean
  print("Detected valid user")
  return bool(result)

  # This a copy from original

  # Remark(2023/03/13): it can recognize kingston face but not the girls.
  # Not test other male face yet. compare_faces function as parameter 'tolerance=0.54',
  # lower number makes face recognition more strict.

  # Remark(2023/03/17): add face location parameter to speed up the recognition process.
  # Set tolerance = 0.37 seems to be proper value for male and female face recognition.

  # Remark(2023/05/04): By increasing the image brightness or merge to HDR image to improve performance of recognition

  # Remark(2023/06/12): Added the real time faical recognition fucntion, 
  # and modified the compare_face function to accept different purposes of face recognition

  # Remark(2023/06/12): modified the compare_face to accept unknown user image and userID parameter,
  # and make deteciton function more clean and easy to read.
  # Unit test for realtime recognition has finished. 

  # Remark(2023/06/29): Changed the face detection to receive JPEG image format, 
  # but should send base64 encoded string as response in object detection.

  # Remark(2023/07/03): Fixed the bug were related to cv2.MergeDebevec: 
  #   1. Using original image and 3 image with different brightness in previous process, merge to HDR.
  #   2. In MergeDebevec.process(), the exposure times are required to every given image, 
  #      the api should provide the exposure time for original image, otherwise 0.03 will be default value.
  #   3. The exposure time sequence will be 0.03, 0.25, 0.5 as default(to be confirm)
  #   4. In cv2.addWeighted(), we set 0.1 and 0.3 as the alpha and beta values, 
  #      seems like perform well with these settings.

  # Remark(2023/08/01): Added batch_face_locations() function to acclerate the face landmark locate process by access to the GPU.
  # However the Nvidia Container Toolkit not ready yet.
  # (Update 2023/08/04) The WSL environment is all set, however still not able to access to the GPU.

  # Remark(2023/08/08): The module can now receive binary as parameter, no further more to decode base64 string to image.
  # Remaek(2023/08/14): Although the module can receive binary data, there still have issues in client side.
  # Change back to receiving base64 string as parameter.