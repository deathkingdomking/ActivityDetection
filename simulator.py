import os
import shutil
import time
import datetime

DIR = '/Users/dakanwang/workspace/on_premise/rpis/simulation'
RPI_DIR = '/Users/dakanwang/workspace/on_premise/rpis/rpi_0/simulation/'

images = [f for f in os.listdir(DIR) if 'jpg' in f]

i = -1
while True:
    time.sleep(5)
    i = (i + 1) % len(images)
    src_img_path = os.path.join(DIR, images[i])
    ts = int(datetime.datetime.now().timestamp() * 1000)
    dst_img_path = os.path.join(RPI_DIR, str(ts) + '.jpg')
    dst_json_path = os.path.join(RPI_DIR, str(ts) + '.json')
    shutil.copy(src_img_path, dst_img_path)
    print ('copy from %s to %s' % (src_img_path, dst_img_path))
    with open(dst_json_path, 'w') as f:
    	f.write('done\n')
    f.close()


