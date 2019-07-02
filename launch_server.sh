#!/bin/bash
  
sudo docker run -v ~/workspace/on_premise/:/root/data/ -v ~/workspace/ActivityDetection/:/root/workspace/cv/ -it activity-detection/cv
