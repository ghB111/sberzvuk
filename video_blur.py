
# !pip install mtcnn
# !pip install tensorflow==2.5
# !pip install keras==2.4.3
# !pip install opencv-python
# !pip install pillow
# !pip install keras_applications
# !pip install keras_vggface

from mtcnn.mtcnn import MTCNN
from keras_vggface.vggface import VGGFace
from keras_vggface.utils import preprocess_input
from keras_vggface.utils import decode_predictions
import glob
import os
import re
import PIL
from urllib import request
import numpy as np
import cv2


def get_img(url):
  res = request.urlopen(url)
  img = np.asarray(bytearray(res.read()), dtype='uint8')
  img = cv2.imdecode(img, cv2.IMREAD_COLOR)
  return img

def find_face(img, frame_num):
  global size
  detector = MTCNN()
  target_size = (224,224) # output image size
  border_rel = 0 # increase or decrease zoom on image
  # detect faces in the image
  size = (img.shape[0], img.shape[1])
  detections = detector.detect_faces(img)

  for detection in detections:
    x1, y1, width, height = detection['box']
    size = (width,height)
    dw = round(width * border_rel)
    dh = round(height * border_rel)
    x2, y2 = x1 + width + dw, y1 + height + dh
    face = img[y1:y2, x1:x2]

    face = PIL.Image.fromarray(face)
    face = face.resize((224, 224))
    face = np.asarray(face)

    face_pp = preprocess_face(face)
    prediction = predict(face_pp)
    if detect_blur(prediction):
      img[y1:y2, x1:x2] = 0

  cv2.imwrite("images/" + '/image_' + str(frame_num) + '.jpg', img)


def preprocess_face(face):
  # convert to float32
  face_pp = face.astype('float32')
  face_pp = np.expand_dims(face_pp, axis = 0)
  face_pp = preprocess_input(face_pp, version = 2)
  return face_pp

def predict(face_pp, model=None):
  model = VGGFace(model= 'resnet50') if model is None else model
  return model.predict(face_pp)

def detect_blur(prediction):
  results = decode_predictions(prediction)

  need_blur = False

  for result in results[0]:
    if result[1]*100 > 80:
      need_blur = True
  return need_blur

def predict_from_videopath(video_path, handled_images):
  vidcap = cv2.VideoCapture(video_path)

  has_frames = True
  frame_num = 0
  skip_frames = 0
  while has_frames:
    has_frames, img = vidcap.read()
    if skip_frames > 0:
      skip_frames -= 1
      continue
    else:
      skip_frames = 25

    handled_images.append(img)
      
    find_face(img, frame_num)
    frame_num += 1

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


# recognize('hackathon_part_1.mp4', "video_hehe.avi")
def recognize(video_path, output_videopath):
  make_a_dir('images/')

  handled_images = []
  predict_from_videopath(video_path, handled_images)

  out = cv2.VideoWriter(output_videopath,cv2.VideoWriter_fourcc(*'MJPG'), 3., size)
  for filename in sorted_alphanumeric(glob.glob('images/*.jpg')):
      img = cv2.imread(filename)
      out.write(img)
  out.release()
