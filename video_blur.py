import cv2
import glob
import os
import re
import PIL
import numpy as np

from mtcnn.mtcnn import MTCNN
from keras_vggface.vggface import VGGFace
from keras_vggface.utils import preprocess_input
from keras_vggface.utils import decode_predictions


def preprocess_face(face):
  face_pp = face.astype('float32')
  face_pp = np.expand_dims(face_pp, axis = 0)
  face_pp = preprocess_input(face_pp, version = 2)
  return face_pp


def detect_blur(prediction):
  results = decode_predictions(prediction)
  need_blur = False
  for result in results[0]:
    if result[1]*100 > 80:
      need_blur = True
  return need_blur


def process_banch(banch, model, detector, force_blur): 
  detections = detector.detect_faces(banch[len(banch)-1])
  blur_founded = []

  for detection in detections:
    x1, y1, width, height = detection['box']
    x2, y2 = x1 + width, y1 + height
    face = banch[len(banch)-1][y1:y2, x1:x2]

    face = PIL.Image.fromarray(face)
    face = face.resize((224, 224))
    face = np.asarray(face)

    face_pp = preprocess_face(face)
    prediction = model.predict_on_batch(face_pp)
    if detect_blur(prediction):
      for index, img in enumerate(banch):
        img[y1:y2, x1:x2] = 0
        banch[index] = img
      blur_founded.append((y1,y2, x1,x2))

  if len(force_blur) > 0:
    for y1,y2,x1,x2 in force_blur:
      for index, img in enumerate(banch):
        img[y1:y2, x1:x2] = 0
        banch[index] = img

  return banch, blur_founded


def CreateVideo(video_path, model, detector, output_videopath):
  try:
    vidcap = cv2.VideoCapture(video_path)
  except Exception as e:
    print(e)
    return None
  
  GRID_SIZE = round(vidcap.get(cv2.cv.CV_CAP_PROP_FPS), 0)

  if vidcap is not None:
    has_frames, img = vidcap.read()
    size = (img.shape[1], img.shape[0])
    out = cv2.VideoWriter(output_videopath,cv2.VideoWriter_fourcc(*'MJPG'), 25., size)
    
    blur_founded = []
    iteration = 0
    imArr = []
    while has_frames:
      has_frames, img = vidcap.read()
      if has_frames:
        imArr.append(img)

        if len(imArr) == GRID_SIZE:
          print(iteration)
          iteration += 1
          imArr, blur_founded = process_banch(imArr, model, detector, blur_founded)

          for im in imArr:
            out.write(im)

          imArr = []

    out.release()

def recognize(video_path, output_videopath):
  model = VGGFace(model='resnet50')
  detector = MTCNN()
  CreateVideo(video_path, model, detector, output_videopath)

# recognize('hackathon_part_1.mp4', "video_out.avi")