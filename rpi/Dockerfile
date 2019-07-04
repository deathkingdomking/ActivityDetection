FROM resin/rpi-raspbian:stretch

RUN apt-get update

RUN apt-get install \
    apt-utils \
    python3 \
    python3-dev \
    python3-pip \
    python3-pyqt5 \
    build-essential \
    wget \
    curl \
    git \
    g++ \
    libatlas-base-dev \
    libcurl4-openssl-dev \
    libboost-python1.62.0 \
    libopenjp2-7-dev \
    libwebp-dev \
    ibgstreamer1.0-dev \
    zlib1g-dev \
    vim \
    htop

RUN apt-get install python3-picamera

# Required for OpenCV
RUN apt-get install \
    libhdf5-dev \
    libhdf5-serial-dev \
    libjpeg-dev \ 
    libtiff5-dev \ 
    libjasper-dev \ 
    libpng-dev \
    libavcodec-dev \
    libavformat-dev \
    libswscale-dev \
    libv4l-dev \
    libqt4-test \
    libqtgui4 \
    libqtwebkit4 \
    libgtk2.0-dev \
    libilmbase-dev \
    libopenexr-dev

# Install Python 3 packages
COPY ./requirements_raspbian.txt /requirements_raspbian.txt
RUN pip3 install --upgrade pip
RUN pip3 install --upgrade setuptools
RUN pip3 install --upgrade six
RUN pip3 install "picamera[array]"
RUN pip3 install paramiko
RUN pip3 install scp


