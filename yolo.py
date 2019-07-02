import numpy as np
import argparse
import cv2 as cv
import subprocess
import time
import os
from yolo_utils import infer_image, show_image
from yolo_model import YoloModel

FLAGS = []

if __name__ == '__main__':
	parser = argparse.ArgumentParser()


	parser.add_argument('-m', '--root-path',
		type=str,
		default='./yolov3-coco/',
		help='The directory where the model weights and \
			  configuration files are.')

	parser.add_argument('-w', '--weights',
		type=str,
		default='./yolov3-coco/yolov3.weights',
		help='Path to the file which contains the weights \
			 	for YOLOv3.')

	parser.add_argument('-cfg', '--config',
		type=str,
		default='./yolov3-coco/yolov3.cfg',
		help='Path to the configuration file for the YOLOv3 model.')

	parser.add_argument('-l', '--labels',
		type=str,
		default='./yolov3-coco/coco-labels',
		help='Path to the file having the \
					labels in a new-line seperated way.')

	parser.add_argument('-c', '--confidence',
		type=float,
		default=0.5,
		help='The model will reject boundaries which has a \
				probabiity less than the confidence value. \
				default: 0.5')

	parser.add_argument('-th', '--threshold',
		type=float,
		default=0.3,
		help='The threshold to use when applying the \
				Non-Max Suppresion')

	parser.add_argument('-t', '--show-time',
		type=bool,
		default=False,
		help='Show the time taken to infer each image.')	

	FLAGS, unparsed = parser.parse_known_args()

	FLAGS.root_path = '/root/data/activity/'
	FLAGS.model_path = '/'.join([FLAGS.root_path, 'model'])


	FLAGS.weights = '/'.join([FLAGS.model_path, 'weight.weights'])
	FLAGS.config = '/'.join([FLAGS.model_path, 'config.cfg'])
	FLAGS.labels = '/'.join([FLAGS.model_path, 'name.names'])

	print ('flags=%s' % FLAGS)

	model = YoloModel(FLAGS)

	in_path = '/'.join([FLAGS.root_path,  'in', '1.jpg'])
	out_path = '/'.join([FLAGS.root_path,  'out', '1.jpg'])

	model.predict(in_path, out_path)




		
