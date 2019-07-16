import numpy as np
import argparse
import cv2 as cv
import subprocess
import time
import os
from yolo_utils import infer_image, show_image

class YoloModel:

  def __init__(self, FLAGS):
    self.FLAGS = FLAGS		

		# Get the labels
    self.labels = open(FLAGS.labels).read().strip().split('\n')

    # Intializing colors to represent each label uniquely
    self.colors = np.random.randint(0, 255, size=(len(self.labels), 3), dtype='uint8')

    self.net = cv.dnn.readNetFromDarknet(FLAGS.config, FLAGS.weights)

    # Get the output layer names of the model
    self.layer_names = self.net.getLayerNames()
    self.layer_names = [self.layer_names[i[0] - 1] for i in self.net.getUnconnectedOutLayers()]
	        

  def predict(self, in_path, out_img_path, out_json_path):
    # Read the image
    try:
      print ('read image from %s' % in_path)
      img = cv.imread(in_path)
      height, width = img.shape[:2]
    except:
      raise 'Image cannot be loaded!\n\
                               Please check the path provided!'
    finally:
      img, boxes, confidences, classids, idxs = infer_image(self.net, self.layer_names, height, width, img, self.colors, self.labels, self.FLAGS)
      cv.imwrite(out_img_path, img)
      with open(out_json_path) as json_file:
        json_file.dump({'boxes': boxes, 'confidences': confidences, 'classids': classids, 'idxs': idxs})

      # show_image(img)