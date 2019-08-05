import argparse
import numpy as np
import cv2 as cv
import subprocess
import time
import os
from yolo_utils import infer_image, show_image
from yolo_model import YoloModel
from two_stage_model import TwoStageModel
import logging
import shutil
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

FLAGS = []


ROOT_DIR = "/root/data/"
# ACTVITIT_DIR = os.path.join(ROOT_DIR, 'activity')
ACTVITIT_DIR = os.path.join(ROOT_DIR, 'activity_2stage')
ACTIVITY_DIR_IN = os.path.join(ACTVITIT_DIR, 'in')
ACTIVITY_DIR_OUT = os.path.join(ACTVITIT_DIR, 'out')
IMG_SUFFIX = ".jpeg"
JSON_SUFFIX = ".json"

class Watcher:
    DIRECTORY_TO_WATCH = ACTVITIT_DIR

    def __init__(self):
        self.observer = Observer()
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.WARNING)
        self.model = self.init_model()

    def init_model(self):
        FLAGS.root_path = ACTVITIT_DIR
        FLAGS.model_path = '/'.join([FLAGS.root_path, 'model'])
        FLAGS.weights = '/'.join([FLAGS.model_path, 'weight.weights'])
        FLAGS.config = '/'.join([FLAGS.model_path, 'config.cfg'])
        FLAGS.labels = '/'.join([FLAGS.model_path, 'name.names'])
        print ('flags=%s' % FLAGS)
        # model = YoloModel(FLAGS)
        model = TwoStageModel()
        Handler.model = model
        print ('intialzied model to be: %s', model)

        return model

    def run(self, FLAGS):
        event_handler = Handler()
        self.observer.schedule(event_handler, ACTIVITY_DIR_IN, recursive=True)
        self.observer.start()
        try:
            while True:
                time.sleep(5)
        except:
            self.observer.stop()
            print ("Error")

        self.observer.join()


class Handler(FileSystemEventHandler):

    model = None

    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.WARNING) 
        super(Handler, self).__init__()   

    @staticmethod
    def on_any_event(event):

        print (event)   
        if event.is_directory:
            return None
        elif event.event_type == 'created':
            # Take any action here when a file is first created.
            print ("Received created event - %s." % event.src_path)
            Handler.call_service(event.src_path, Handler.model)
        else:
        	return None


    @staticmethod 
    def call_service(in_path, model):
        file_name = os.path.basename(in_path).rstrip(IMG_SUFFIX)
        predicted_img_name = 'predicted-' + file_name + IMG_SUFFIX
        predicted_json_name = 'predicted-' + file_name + JSON_SUFFIX
        out_img_path = os.path.join(ACTIVITY_DIR_OUT, predicted_img_name)
        out_json_path = os.path.join(ACTIVITY_DIR_OUT, predicted_json_name)

        model.predict(in_path, out_img_path, out_json_path)


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

	w = Watcher()
	w.run(FLAGS)




		
