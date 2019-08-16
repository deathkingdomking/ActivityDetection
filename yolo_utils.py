import numpy as np
import argparse
import cv2 as cv
import subprocess
import datetime
import time
import os

def show_image(img):
    cv.imshow("Image", img)
    cv.waitKey(0)

def get_boxes(img,boxes,idxs, scale):
    height, width = img.shape[:2]
    patches = []
    exp_margin = (scale - 1)/2
    if len(idxs) > 0:
        for i in idxs.flatten():
            # Get the bounding box coordinates
            x, y = boxes[i][0], boxes[i][1]
            w, h = boxes[i][2], boxes[i][3]

            x = int(x - exp_margin*w)
            y = int(y - exp_margin*h)
            w = int(w*scale)
            h = int(h*scale)

            x = max(0,x)
            y = max(0,y)
            w = min(w, width - x)
            h = min(h, height -y)

            img_tmp = img[y:y+h,x:x+w,:].copy()
            patches.append(img_tmp)
            # show_image(img_tmp)
    return patches    

def draw_labels_and_boxes(img, boxes, confidences, classids, idxs, colors, labels):
    # If there are any detections
    json_data = {'result':{'positions':[], 'areas':[], 'behaviors':[]}}
    if len(idxs) > 0:
        for i in idxs.flatten():
            # Get the bounding box coordinates
            x, y = boxes[i][0], boxes[i][1]
            w, h = boxes[i][2], boxes[i][3]
            
            # Get the unique color for this class
            color = [int(c) for c in colors[classids[i]]]

            # Draw the bounding box rectangle and label on the image
            cv.rectangle(img, (x, y), (x+w, y+h), color, 2)
            text = "{}: {:4f}".format(labels[classids[i]], confidences[i])
            cv.putText(img, text, (x, y-5), cv.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)
            json_data['result']['positions'].append({'x': x, 'y':y, 'h':h, 'w':w})
            json_data['result']['behaviors'].append(text)
            json_data['result']['areas'].append('default')

    return img, json_data


def generate_boxes_confidences_classids(outs, height, width, tconf):
    boxes = []
    confidences = []
    classids = []

    for out in outs:
        for detection in out:
            #print (detection)
            #a = input('GO!')
            
            # Get the scores, classid, and the confidence of the prediction
            scores = detection[5:]
            classid = np.argmax(scores)
            confidence = scores[classid]
            
            # Consider only the predictions that are above a certain confidence level
            if confidence > tconf:
                # TODO Check detection
                box = detection[0:4] * np.array([width, height, width, height])
                centerX, centerY, bwidth, bheight = box.astype('int')

                # Using the center x, y coordinates to derive the top
                # and the left corner of the bounding box
                x = int(centerX - (bwidth / 2))
                y = int(centerY - (bheight / 2))

                # Append to list
                boxes.append([x, y, int(bwidth), int(bheight)])
                confidences.append(float(confidence))
                classids.append(classid)

    return boxes, confidences, classids

def infer_image(net, layer_names, height, width, img, colors, labels, FLAGS, 
            boxes=None, confidences=None, classids=None, idxs=None, infer=True):
    
    if infer:
        # Contructing a blob from the input image
        blob = cv.dnn.blobFromImage(img, 1 / 255.0, (416, 416), 
                        swapRB=True, crop=False)

        # Perform a forward pass of the YOLO object detector
        net.setInput(blob)

        # Getting the outputs from the output layers
        start = time.time()
        outs = net.forward(layer_names)
        end = time.time()

        if FLAGS.show_time:
            print ("[INFO] YOLOv3 took {:6f} seconds".format(end - start))

        
        # Generate the boxes, confidences, and classIDs
        boxes, confidences, classids = generate_boxes_confidences_classids(outs, height, width, FLAGS.confidence)
        
        # Apply Non-Maxima Suppression to suppress overlapping bounding boxes
        idxs = cv.dnn.NMSBoxes(boxes, confidences, FLAGS.confidence, FLAGS.threshold)

    if boxes is None or confidences is None or idxs is None or classids is None:
        raise '[ERROR] Required variables are set to None before drawing boxes on images.'
        
    # Draw labels and boxes on the image
    img, json_data = draw_labels_and_boxes(img, boxes, confidences, classids, idxs, colors, labels)

    return img, json_data


def draw_labels_and_boxes_2_stage(img, boxes , idxs , preds , labels):
    # If there are any detections
    json_data = {'result':{'positions':[], 'areas':[], 'behaviors':[]}}

    if len(idxs) > 0:
        idx_cnt = 0
        for i in idxs.flatten():
            # Get the bounding box coordinates
            x, y = boxes[i][0], boxes[i][1]
            w, h = boxes[i][2], boxes[i][3]

            # Get the unique color for this class
            color = [0,255,0]

            # Draw the bounding box rectangle and label on the image
            cv.rectangle(img, (x, y), (x + w, y + h), color, 2)

            pred = preds[idx_cnt]
            names = []
            for i in range(len(pred)):
                if pred[i] > 0:
                    names.append( (pred[i],labels[i]))
            sorted(names,key=lambda s: s[0] , reverse=True)

            str_out = ''
            for i in range(len(names)):
                if i == 3:
                    break
                str_out = str_out + names[i][1] + ';'

            text = "{}".format(str_out)
            # text = "{:d}".format(idx_cnt)
            cv.putText(img, text, (x+5, y + 15), cv.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)

            json_data['result']['positions'].append({'x': x, 'y':y, 'h':h, 'w':w})
            json_data['result']['behaviors'].append(text)
            json_data['result']['areas'].append('default')


            idx_cnt += 1

    return img, json_data    
