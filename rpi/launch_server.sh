#!/bin/bash
  
sudo docker run -v ~/workspace/on_premise/:/root/data/ -v ~/workspace/ActivityDetection/:/root/workspace/cv/ -it cv-rpi


sudo docker run -v /root/data/:/root/data/ -v $PWD:/root/workspace/cv/  --device=/dev/vcsm --device=/dev/vchiq -it cv-rpi
