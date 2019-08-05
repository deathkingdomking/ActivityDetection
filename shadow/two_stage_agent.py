import argparse
import datetime
import sys
sys.path.append("..")

import os
import json
import logging
import shutil
import time
import kafka_client
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler


ROOT_DIR = "/root/data/"
ACTVITIT_DIR = os.path.join(ROOT_DIR, 'activity')
IMG_SUFFIX = ".jpeg"
JSON_SUFFIX = ".json"

KAFKA_CLIENT = kafka_client.Kafka_Client()


class Watcher:
    DIRECTORY_TO_WATCH = "/root/data/"

    def __init__(self):
        self.observer = Observer()
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.WARNING)

    def run(self):
        event_handler = Handler()
        self.observer.schedule(event_handler, os.path.join(self.DIRECTORY_TO_WATCH, 'rpis', 'rpi_0'), recursive=True)
        self.observer.start()
        try:
            while True:
                time.sleep(5)
        except:
            self.observer.stop()
            print ("Error")

        self.observer.join()


class Handler(FileSystemEventHandler):

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
            Handler.call_service(event.src_path)
        elif event.event_type == 'modified':
            # Taken any action here when a file is modified.
            print ("Received modified event - %s." % event.src_path)

    @staticmethod 
    def call_service(src_path):

        # calling the service asyncly
        file_name = os.path.basename(src_path).rstrip(IMG_SUFFIX)
        shutil.copy(src_path, os.path.join(ACTVITIT_DIR, 'in'))

        predicted_img_name = 'predicted-' + file_name + IMG_SUFFIX
        predicted_json_name = 'predicted-' + file_name + JSON_SUFFIX
        kakfa_json_name = 'kafka-' + file_name + JSON_SUFFIX
        model_output_dir = os.path.join(ACTVITIT_DIR, 'out')
        json_data_path = os.path.join(model_output_dir, predicted_json_name)
        kafka_data_path = os.path.join(model_output_dir, kakfa_json_name)
        print ('json_data_path = %s' % json_data_path)

        while (True):
            if (os.path.exists(json_data_path)):  
                with open(json_data_path, 'r') as json_file:  
                    data = json.load(json_file)
                    print (data)
                    data['result']['source'] = predicted_img_name
                    data['ec_event_time'] = time.time()
                    data['object'] = {'Displayname' : '', 'area' : {'displayName': ''}}
                    data['description'] = 'action_recognition'


                with open(kafka_data_path, 'w') as kafka_file:
                    json.dump(data, kafka_file)
                    KAFKA_CLIENT.send_data(data)                        
                print ("the preidiction is done: %s" % data)
                break
            else:
                print ("the preidiction is not done yet, go back to sleep for 0.5sec")
                time.sleep(0.5)           


if __name__ == '__main__':
    w = Watcher()
    w.run()