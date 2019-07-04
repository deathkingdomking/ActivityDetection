import time
from datetime import datetime
from capture import Camera
import os
from os import path
from copy_data import SSH_Client

ROOT_FOLDER = '/root/data/'
REMOTE_FOLDER = '/Users/dakanwang/workspace/on_premise'
camera = Camera(resolution=[640, 480])
ssh_client = SSH_Client()

def get_folder_and_file_name():
  start_time = datetime.now().replace(microsecond=0)
  
  (hour, minute, second) = (start_time.hour, start_time.minute, start_time.second)

  img_name = "%s.jpg" % start_time.second # e.g. 20-10-55 instead of 20:10:44

  folder = path.join(ROOT_FOLDER, str(hour), str(minute))

  return (folder, img_name)	


def copy_images(folder):
  ssh_client.copy_to_server(folder, REMOTE_FOLDER) 


current_folder = ''
while True:
  time.sleep(1)

  (folder, file_name) = get_folder_and_file_name()
  if folder != current_folder:
    if current_folder == '':
      current_folder = folder
      os.makedirs(folder)
    if folder != current_folder:
      print ('copy images over')
      copy_images(current_folder)
      os.makedirs(folder)
      current_folder = folder  	  

  print ('capture %s, %s' % (folder, file_name))
  results = {}
  camera.capture(folder, file_name, results)

