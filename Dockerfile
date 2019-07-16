FROM ubuntu:16.04 

RUN apt-get update &&  \
       apt-get install -y python-pip python-opencv

RUN apt-get install -y git

RUN apt-get install -y python-setuptools

RUN pip install wheel

RUN pip install --upgrade git+https://github.com/Maratyszcza/PeachPy

RUN pip install --upgrade git+https://github.com/Maratyszcza/confu

RUN git clone https://github.com/ninja-build/ninja.git

RUN apt-get install -y build-essential g++

RUN cd ninja && git checkout release && ./configure.py --bootstrap
RUN export NINJA_PATH=$PWD
RUN cd

RUN apt-get install -y python3

RUN apt-get install -y curl && \
    curl https://www.amazontrust.com/repository/AmazonRootCA1.pem > root-CA.crt

RUN git clone https://github.com/aws/aws-iot-device-sdk-python.git && \
    cd aws-iot-device-sdk-python && \
    python setup.py install && \
    cd ..

RUN apt-get update -y && apt-get dist-upgrade -y && apt-get install -y libhdf5-dev libhdf5-serial-dev \
    && apt-get install -y libqtwebkit4 libqt4-test && apt-get install -y libatlas-base-dev && apt-get install -y libjasper-dev libqtgui4 python3-pyqt5

RUN apt-get install -y wget && wget https://bootstrap.pypa.io/get-pip.py \
    && python3 get-pip.py && pip install opencv-contrib-python && pip install imutils

RUN apt-get install -y vim

RUN mkdir -p /root/workspace/CV/
RUN cd /root/workspace/CV/ && git clone https://github.com/iArunava/YOLOv3-Object-Detection-with-OpenCV.git
#COPY model/activity_wework.names /root/workspace/CV/YOLOv3-Object-Detection-with-OpenCV/yolov3-coco/coco.names
#COPY model/activity_wework.weights /root/workspace/CV/YOLOv3-Object-Detection-with-OpenCV/yolov3-coco/yolov3.weights
#COPY model/activity_wework.cfg /root/workspace/CV/YOLOv3-Object-Detection-with-OpenCV/yolov3-coco/yolov3.cfg

COPY kinetics /root/workspace/kinetics
RUN wget https://yt-dl.org/downloads/latest/youtube-dl -O /usr/bin/youtube-dl

RUN cd /root/workspace/  && git clone https://deathkingdomking:f1f24b5cefbf4534d94338388da086e88450e16d@github.com/WeConnect/cn-eventcollector-python 
RUN cd /root/workspace/cn-eventcollector-python && python3 setup.py install

RUN pip install watchdog

