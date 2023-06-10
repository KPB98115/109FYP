import face_recognition as faceRec
import os
import cv2
import numpy as np
import util
import base64

valid_images = []
valid_image_encodings = []
dirname = os.path.dirname(__file__)
valid_faces_names = [
  "Kingston",
  "Eva",
  "Ling",
  "Lynn",
  "Hebby"
]

def detection(base64_str):
  try:
    # Remove the data attribute from the string
    index = base64_str.find(',') + 1
    base64_str = base64_str[index:]
    # Convert the WebP file to a JPEG file
    decoded_img = base64.b64decode(base64_str)
    # Save the screenshot to dictionary
    with open(os.path.join(dirname, "image/unknown_profile_pic/unknown_user.jpg"), "wb") as file:
      file.write(decoded_img)

    #cv2.imwrite("unknown_user.jpeg", jpeg_bytes, [int(cv2.IMWRITE_JPEG_QUALITY), 90])
  except Exception as error:
    print("Failed to convert image.")
    return ["unknown", False, str(error)]

  # Load the valid image.
  try:
    if "unknown_user.jpg" in os.listdir(os.path.join(dirname, "image/unknown_profile_pic")):
      # Load the unknown image for face recognition testing.
      print("Loading unknown image")
      unknown_image = faceRec.load_image_file(os.path.join(dirname, "image/unknown_profile_pic/unknown_user.jpg"))
  except Exception as error:
    print("Failed to load unknown image")
    return ["unknown", False, str(error)]
  
  # Using the original image to compare
  result = compare_faces(unknown_image)
  if result[1]:
    return result

  # Increase the brightness of the image
  for brightness in range(1, 4, 2):
    unknown_image = cv2.addWeighted(unknown_image, 5, unknown_image, brightness)
    result = compare_faces(unknown_image)
    if result[1]:
      return result
    
  # Use Merge exposures into HDR image
  merge_debevec = cv2.createMergeDebevce()
  hdr_debevec = merge_debevec.process(unknown_image, times=np.array([15.0, 2.5, 0.25, 0.0333], dtype=np.float32).copy())
  unknown_image = np.clip(hdr_debevec*255, 0, 255).astype('uint8')
  result = compare_faces(unknown_image)
  if result[1]:
    return result

def compare_faces(unknown_image):
  # Get the face encodings for each face in each image file
  # Since there could be more than one face in each image, it returns a list of encodings.
  # But since I know each image only has one face, I only care about the first encoding in each image, so I grab index 0.
  try:
    # Encoding the unknown image 
    unknown_face_encoding = faceRec.face_encodings(unknown_image)[0]

  except IndexError:
      print("I wasn't able to locate any faces in at least one of the images. Check the image files. Aborting...")
      return ["unknown", False, "Error occurred: No faces located."]

  # Results is an array of True/False telling if the unknown face matched anyone in the known_faces array
  print("comparing...")
  # Tolerance = 0.37 seems to be proper value to recognize male and female faces.
  matches = faceRec.compare_faces(util.valid_face_encodings, unknown_face_encoding, tolerance=0.37)
  face_distances = faceRec.face_distance(util.valid_face_encodings, unknown_face_encoding)
  best_match_index = np.argmin(face_distances)
  if matches[best_match_index]:
    name = valid_faces_names[best_match_index]
    return [name, True, ""]
  
  print("No matching user found.")
  return ["", False, "No valid user found"]

  
  """
  if faceRec.compare_faces([util.kingston_face_encodings], unknown_face_encoding, tolerance=0.37)[0] == True:
    print("User: kingston has login successfully.")
    return ["Kingston", True, ""]
  elif faceRec.compare_faces([util.eva_face_encodings], unknown_face_encoding, tolerance=0.37)[0] == True:
    print("User: eva has login successfully.")
    return ["Eva", True, ""]
  elif faceRec.compare_faces([util.ling_face_encodings], unknown_face_encoding, tolerance=0.37)[0] == True:
    print("User: ling has login successfully.")
    return ["Ling", True, ""]
  elif faceRec.compare_faces([util.lynn_face_encodings], unknown_face_encoding, tolerance=0.37)[0] == True:
    print("User: lynn has login successfully.")
    return ["Lynn", True, ""]
  elif faceRec.compare_faces([util.hebby_face_encodings], unknown_face_encoding, tolerance=0.37)[0] == True:
    print("User: hebby has login successfully.")
    return ["Hebby", True, ""]
  else:
    print("No matching user found.")
    return ["", False, "No valid user found"]
  """



  # Remark(2023/03/13): it can recognize kingston face but not the girls.
  # Not test other male face yet. compare_faces function as parameter 'tolerance=0.54',
  # lower number makes face recognition more strict.

  # Remark(2023/03/17): add face location parameter to speed up the recognition process.
  # Set tolerance = 0.37 seems to be proper value for male and female face recognition.

  # Remark(2023/05/04: By increasing the image brightness or merge to HDR image to improve performance of recognition