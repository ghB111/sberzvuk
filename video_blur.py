
# !pip install mtcnn
# !pip install tensorflow==2.5
# !pip install keras==2.4.3
# !pip install opencv-python
# !pip install pillow
# !pip install keras_applications
# !pip install keras_vggface

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


def get_files(dirpath):
		return [s for s in os.listdir(dirpath) if os.path.isfile(os.path.join(dirpath, s))]


def make_a_dir(folder):
	if os.path.exists(folder):
		os.system('rm -rf ' + folder)
	os.mkdir(folder)


def sorted_alphanumeric(data):
    convert = lambda text: int(text) if text.isdigit() else text.lower()
    alphanum_key = lambda key: [ convert(c) for c in re.split('([0-9]+)', key) ] 
    return sorted(data, key=alphanum_key)


def preprocess_face(face):
  face_pp = face.astype('float32')
  face_pp = np.expand_dims(face_pp, axis = 0)
  face_pp = preprocess_input(face_pp, version = 2)
  return face_pp


def detect_blur(prediction):
  results = decode_predictions(prediction)
  need_blur = False
  for result in results[0]:
    if result[1]*100 > 70:
      need_blur = True
  return need_blur


def find_face(img, model,detector):
  #TODO relocate detector
  border_rel = 0
  detections = detector.detect_faces(img)

  for detection in detections:
    x1, y1, width, height = detection['box']
    dw = round(width * border_rel)
    dh = round(height * border_rel)
    x2, y2 = x1 + width + dw, y1 + height + dh
    face = img[y1:y2, x1:x2]

    face = PIL.Image.fromarray(face)
    face = face.resize((224, 224))
    face = np.asarray(face)

    face_pp = preprocess_face(face)
    prediction = model.predict(face_pp)
    if detect_blur(prediction):
      img[y1:y2, x1:x2] = 0
    return 
  

def deframe_Video(video_path):
  try:
    vidcap = cv2.VideoCapture(video_path)
  except Exception as e:
    print(e)
    return None

  has_frames = True
  frame_num = 0
  skip_frames = 0
  size = None

  while True:
    '''
    if skip_frames > 0:
      has_frames, _ = vidcap.read()
      skip_frames -= 1
      continue
    else:
      skip_frames = 25
    '''
    has_frames, img = vidcap.read()
    if has_frames:
      cv2.imwrite("images/" + '/image_' + str(frame_num) + '.jpg', img)
      size = (img.shape[1], img.shape[0])
      frame_num += 1
    else:
      break
      
  return size

def process_banch(banch , model, detector):

  border_rel = 0
  detections = detector.detect_faces(banch[0])

  for detection in detections:
    x1, y1, width, height = detection['box']
    dw = round(width * border_rel)
    dh = round(height * border_rel)
    x2, y2 = x1 + width + dw, y1 + height + dh
    face = banch[0][y1:y2, x1:x2]

    face = PIL.Image.fromarray(face)
    face = face.resize((224, 224))
    face = np.asarray(face)

    face_pp = preprocess_face(face)
    prediction = model.predict(face_pp)
    
    if detect_blur(prediction):
      for index, img in enumerate(banch):
        img[y1:y2, x1:x2] = 0
        banch[index] = img

  return banch


  


def CreateVideo(size, model, detector, output_videopath, gridSize):

  if size is not None:
    out = cv2.VideoWriter(output_videopath,cv2.VideoWriter_fourcc(*'MJPG'), 25., size)
    
    
    for filename in sorted_alphanumeric(glob.glob('images/*.jpg')):
        imArr = []
        for i in range(gridSize):
          imArr.append( cv2.imread(filename))
        
        imArr = process_banch(imArr, model, detector)
        for im in imArr:
          out.write(im)
    out.release()




def predict_from_videopath(video_path, model):
  try:
    vidcap = cv2.VideoCapture(video_path)
  except Exception as e:
    print(e)
    return None

  has_frames = True
  frame_num = 0
  skip_frames = 0
  size = None

  while has_frames:
    '''
    if skip_frames > 0:
      has_frames, _ = vidcap.read()
      skip_frames -= 1
      continue
    else:
      skip_frames = 25
    '''
    has_frames, img = vidcap.read()
    find_face(img, frame_num, model)
    size = (img.shape[1], img.shape[0])
    frame_num += 1
    
  return size


def recognize(video_path, output_videopath):
  make_a_dir('images/')
  model = VGGFace(model='resnet50')
  detector = MTCNN()
  gridSize = 25
  
  # shitting in directory with frames from video
  #size = (1920, 1080)
  size = deframe_Video(video_path)
  print(size)
  #size = predict_from_videopath(video_path, model)
  
  #creating a video 

  CreateVideo(size, model, detector, output_videopath, gridSize)
'''
  if size is not None:
    out = cv2.VideoWriter(output_videopath,cv2.VideoWriter_fourcc(*'MJPG'), 3., size)
    for filename in sorted_alphanumeric(glob.glob('images/*.jpg')):
        img = cv2.imread(filename)
        out.write(img)
    out.release()
'''
recognize('./video.mp4', "video_hehe.avi")