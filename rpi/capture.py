from picamera import PiCamera
from datetime import datetime
from time import mktime
from os import path

class Camera():
    def __init__(self, resolution, dest_folder, ready=None):        
        self._ready = ready
        self._camera = PiCamera()
        self._camera.resolution = resolution
        self._dest_folder = dest_folder
    
    def capture(self, results):                
        start_time = datetime.now().replace(microsecond=0)
        img_name = str(start_time.time()).replace(':', '-') # e.g. 20-10-55 instead of 20:10:44
        
        results['timestamp'] = "%s000" % str(mktime(start_time.timetuple()))[:-2]                
        results['img_path'] = path.join(self._dest_folder, "%s.jpg" % img_name)        
        self._camera.capture(results['img_path'])
        
        # print("Picture taken: %s" % datetime.now().strftime("%I:%M:%S %p on %B %d, %Y"))    
        self._ready.set()