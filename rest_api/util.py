import face_recognition as faceRec
import os
import cv2

valid_images = []

valid_face_encodings = []

valid_usernames = ["kingston", "eva", "ling", "hebby", "lynn"]

valid_users_info: dict = {
  "kingston": {
    "path": "image/valid_profile_pic/kingston.jpg",
    "location": [(1150, 1682, 2108, 723)],
  },
  "eva": {
    "path": "image/valid_profile_pic/eva.jpg",
    "location": [(650, 1167, 1316, 502)],
  },
  "ling": {
    "path": "image/valid_profile_pic/ling.jpg",
    "location": [(724, 1362, 1682, 404)],
  },
  "lynn": {
    "path": "image/valid_profile_pic/lynn.jpg",
    "location": [(247, 675, 632, 290)],
  },
  "hebby": {
    "path": "image/valid_profile_pic/hebby.jpg",
    "location": [(461, 718, 846, 332)],
  },
}

DIR_NAME = os.path.dirname(__file__)

#Load kingston images
valid_images.append(faceRec.load_image_file(os.path.join(DIR_NAME, 'image/valid_profile_pic/kingston.jpg')))

#Load eva images
valid_images.append(faceRec.load_image_file(os.path.join(DIR_NAME, 'image/valid_profile_pic/eva.jpg')))

#Load ling images
valid_images.append(faceRec.load_image_file(os.path.join(DIR_NAME, 'image/valid_profile_pic/ling.jpg')))

#Load lynn images
valid_images.append(faceRec.load_image_file(os.path.join(DIR_NAME, 'image/valid_profile_pic/lynn.jpg')))

#Load hebby images
valid_images.append(faceRec.load_image_file(os.path.join(DIR_NAME, 'image/valid_profile_pic/hebby.jpg')))

valid_users_info["kingston"]["encoding"] = faceRec.face_encodings(valid_images[0], valid_users_info["kingston"]["location"])[0]
valid_users_info["eva"]["encoding"] = faceRec.face_encodings(valid_images[1], valid_users_info["eva"]["location"])[0]
valid_users_info["ling"]["encoding"] = faceRec.face_encodings(valid_images[2], valid_users_info["ling"]["location"])[0]
valid_users_info["lynn"]["encoding"] = faceRec.face_encodings(valid_images[3], valid_users_info["lynn"]["location"])[0]
valid_users_info["hebby"]["encoding"] = faceRec.face_encodings(valid_images[4], valid_users_info["hebby"]["location"])[0]

"""
kingston_face_encodings = faceRec.face_encodings(valid_images[0], valid_users_info["kingston"]["location"])[0]
eva_face_encodings = faceRec.face_encodings(valid_images[1], valid_users_info["eva"]["location"])[0]
ling_face_encodings = faceRec.face_encodings(valid_images[2], valid_users_info["ling"]["location"])[0]
lynn_face_encodings = faceRec.face_encodings(valid_images[3], valid_users_info["lynn"]["location"])[0]
hebby_face_encodings = faceRec.face_encodings(valid_images[4], valid_users_info["hebby"]["location"])[0]

valid_face_encodings.append(kingston_face_encodings)
valid_face_encodings.append(eva_face_encodings)
valid_face_encodings.append(ling_face_encodings)
valid_face_encodings.append(lynn_face_encodings)
valid_face_encodings.append(hebby_face_encodings)
"""

def addUser(username: str, image_path: str, np_image: list, landmarks: list) -> bool:
  if username != "" and image_path != "" and landmarks != "":
    new_user_encodings = faceRec.face_encodings(np_image, landmarks)[0]
    valid_users_info[username] = {"path": image_path, "location": landmarks, "encoding": new_user_encodings}
    valid_usernames.append(username)
    return True
  else:
    return False

print("Load utility sussessfully.")