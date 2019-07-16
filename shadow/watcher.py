import logging
import shutil
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler


ROOT_DIR = "/root/data/"
ACTVITIT_DIR = os.path.join(ROOT_DIR, 'activity')

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


        elif event.event_type == 'modified':
            # Taken any action here when a file is modified.
            print ("Received modified event - %s." % event.src_path)


    @staticmethod 
    def call_service(src_path):
        path_name = os.path.basename(src_path)
        shutil.copy(src_path, os.path.join(ACTVITIT_DIR, 'in'))
        while ()                     



if __name__ == '__main__':
    w = Watcher()
    w.run()