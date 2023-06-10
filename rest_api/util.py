import face_recognition as faceRec
import os
import cv2

valid_images = []

valid_face_encodings = []

kingston_face_locations = [(1150, 1682, 2108, 723)]
eva_face_locations = [(650, 1167, 1316, 502)]
ling_face_locations = [(724, 1362, 1682, 404)]
lynn_face_locations = [(247, 675, 632, 290)]
hebby_face_locations = [(461, 718, 846, 332)] 

dirname = os.path.dirname(__file__)

#Load kingston images
valid_images.append(faceRec.load_image_file(os.path.join(dirname, 'image/valid_profile_pic/kingston.jpg')))

#Load eva images
valid_images.append(faceRec.load_image_file(os.path.join(dirname, 'image/valid_profile_pic/eva.jpg')))

#Load ling images
valid_images.append(faceRec.load_image_file(os.path.join(dirname, 'image/valid_profile_pic/ling.jpg')))

#Load lynn images
valid_images.append(faceRec.load_image_file(os.path.join(dirname, 'image/valid_profile_pic/lynn.jpg')))

#Load hebby images
valid_images.append(faceRec.load_image_file(os.path.join(dirname, 'image/valid_profile_pic/hebby.jpg')))

kingston_face_encodings = faceRec.face_encodings(valid_images[0], kingston_face_locations)[0]
eva_face_encodings = faceRec.face_encodings(valid_images[1], eva_face_locations)[0]
ling_face_encodings = faceRec.face_encodings(valid_images[2], ling_face_locations)[0]
lynn_face_encodings = faceRec.face_encodings(valid_images[3], lynn_face_locations)[0]
hebby_face_encodings = faceRec.face_encodings(valid_images[4], hebby_face_locations)[0]

valid_face_encodings.append(kingston_face_encodings)
valid_face_encodings.append(eva_face_encodings)
valid_face_encodings.append(ling_face_encodings)
valid_face_encodings.append(lynn_face_encodings)
valid_face_encodings.append(hebby_face_encodings)

print("Load utility sussessfully.")