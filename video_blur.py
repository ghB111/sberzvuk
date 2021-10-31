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
    if result[1]*100 > 85:
      need_blur = True
  return need_blur


def process_banch(batch, batch_index, model, detector, force_blur): 
  detections = detector.detect_faces(batch[len(batch)-1])
  
  blur_founded = []
  blur_drawed = []

  for detection in detections:
    x1, y1, width, height = detection['box']
    x2, y2 = x1 + width, y1 + height
    face = batch[len(batch)-1][y1:y2, x1:x2]

    face = PIL.Image.fromarray(face)
    face = face.resize((224, 224))
    face = np.asarray(face)

    face_pp = preprocess_face(face)
    prediction = model.predict_on_batch(face_pp)
    if detect_blur(prediction):
      for index, img in enumerate(batch):
        img[y1:y2, x1:x2] = 0
        batch[index] = img
        blur_drawed.append((index + batch_index * len(batch), (x1, y1), (x2, y2)))
      blur_founded.append((y1,y2, x1,x2))

  if len(force_blur) > 0:
    for y1,y2,x1,x2 in force_blur:
      for index, img in enumerate(batch):
        img[y1:y2, x1:x2] = 0
        batch[index] = img
        blur_drawed.append((index + batch_index * len(batch), (x1, y1), (x2, y2)))

  return batch, blur_founded, blur_drawed


def CreateVideo(video_path, model, detector, output_videopath):
  try:
    vidcap = cv2.VideoCapture(video_path)
  except Exception as e:
    print(e)
    return None
  
  FPS = round(vidcap.get(cv2.CAP_PROP_FPS), 0)

  if vidcap is not None:
    has_frames, img = vidcap.read()
    if not has_frames:
      return None
    size = (img.shape[1], img.shape[0])
    out = cv2.VideoWriter(output_videopath,cv2.VideoWriter_fourcc(*'MP4V'), 25., size)
    
    blur_founded = []
    blur_drawed = []
    batch_index = 0
    imArr = []
    while has_frames:
      has_frames, img = vidcap.read()
      if has_frames:
        imArr.append(img)

        if len(imArr) == GRID_SIZE:
          print("Batch:", batch_index)
          batch_index += 1
          imArr, blur_founded, blur_drawed_batch = process_banch(imArr, batch_index, model, detector, blur_founded)
          blur_drawed += blur_drawed_batch
          for im in imArr:
            out.write(im)

          imArr = []

    out.release()

  return FPS, blur_drawed

def recognize(video_path, output_videopath):
  model = VGGFace(model='resnet50')
  detector = MTCNN()
  return CreateVideo(video_path, model, detector, output_videopath)

# fps, res = recognize('video.mp4', "video_out.mp4")
# print(fps)
# print(res[0][0])
# print(res[0][1])
# print(res[0][2])