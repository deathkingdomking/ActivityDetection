FROM ubuntu:16.04 

RUN apt-get update &&  \
       apt-get install -y python-pip python-opencv

RUN apt-get install -y git

RUN apt-get install -y python-setuptools

RUN pip install wheel

RUN apt-get install -y python3

RUN apt-get update -y && apt-get dist-upgrade -y && apt-get install -y libhdf5-dev libhdf5-serial-dev \
    && apt-get install -y libqtwebkit4 libqt4-test && apt-get install -y libatlas-base-dev && apt-get install -y libjasper-dev libqtgui4 python3-pyqt5

RUN apt-get install -y wget && wget https://bootstrap.pypa.io/get-pip.py \
    && python3 get-pip.py && pip install opencv-contrib-python && pip install imutils

RUN apt-get install -y vim

RUN pip install watchdog