#!/bin/bash
  
sudo docker run -v /root/data/:/root/data/ -v $PWD:/root/workspace/cv/  --device=/dev/vcsm --device=/dev/vchiq -it cv-rpi
