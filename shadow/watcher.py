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
import schema.activity_chn as activity_chn


ROOT_DIR = "/root/data/"
ACTVITIT_DIR = os.path.join(ROOT_DIR, 'activity_2stage')
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
        self.observer.schedule(event_handler, os.path.join(self.DIRECTORY_TO_WATCH, 'rpis', 'rpi_0'), recursive = True)
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
            if ('jpg' in event.src_path):
                print ("Received created event - %s." % event.src_path)
                Handler.call_service(event.src_path)
        elif event.event_type == 'modified':
            # Taken any action here when a file is modified.
            if ('jpg' in event.src_path):
                print ("Received modified event - %s." % event.src_path)
                Handler.call_service(event.src_path)


    @staticmethod 
    def call_service(src_path):

        # calling the service asyncly
        file_name = os.path.basename(src_path).rstrip(IMG_SUFFIX)
        shutil.move(src_path, os.path.join(ACTVITIT_DIR, 'in'))
        with open(os.path.join(ACTVITIT_DIR, 'in', file_name + JSON_SUFFIX), 'w') as f:
            f.write('done\n')
        f.close()    

        model_output_dir = os.path.join(ACTVITIT_DIR, 'out')

        predicted_img_name = 'predicted-' + file_name + IMG_SUFFIX
        predicted_json_name = 'predicted-' + file_name + JSON_SUFFIX

        tmp_kafka_json_name = 'tmp-' + file_name + JSON_SUFFIX
        tmp_data_path = os.path.join(model_output_dir, tmp_kafka_json_name)

        kakfa_json_name = 'kafka-' + file_name + JSON_SUFFIX
        kafka_data_path = os.path.join(model_output_dir, kakfa_json_name)

        json_data_path = os.path.join(model_output_dir, predicted_json_name)
        print ('json_data_path = %s' % json_data_path)

        while (True):
            if (os.path.exists(json_data_path)):  
                with open(json_data_path, 'r') as json_file:  
                    data = json.load(json_file)

                    data['actor'] = {"type": "Camera", "displayName": "Raspberry Pi Version 4", "id": "camera01", "mac": "38:f9:d3:27:fe:c3"}
                    data["verb"] = "recognize"
                    data["object"] =  {"type": "Location",  "displayName": "China Oversea", \
                                        "area": {"displayName": "Third floor elevator", "id": "areaA3B4"}, \
                                        "id": "232"}   
                    data["publish"] = "2019-09-11 19:00:12Z"
                    data['description'] = 'action_recognition'
                    data['ec_event_time'] = time.time()
                    data["ec_event_id"] = "this-is-a-unique-id"

                    data['result']['source'] = predicted_img_name
                    data['result']['count'] = 2
                    data['result']['type'] = 'Person'


                with open(tmp_data_path, 'w') as kafka_file:
                    json.dump(data, kafka_file)
                    print ('sending the kafka data')
                    KAFKA_CLIENT.send_data(activity_chn.sample_activity_chn_data)
                kafka_file.close()
                shutil.move(tmp_data_path, kafka_data_path)                       
                return
            else:
                print ("the preidiction is not done yet, go back to sleep for 1 sec")
                time.sleep(1)           


if __name__ == '__main__':
    w = Watcher()
    w.run()