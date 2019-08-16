import argparse
import json
import numpy as np
import cv2 as cv
import os
import yolo_utils


model_root = '/models/model/'
det_config = model_root + 'yolov3_person.cfg'
det_weights = model_root + 'yolov3_person_16000.weights'

cls_config = model_root + 'wwdarknet53v2.cfg'
cls_weights = model_root + 'wwdarknet53v2_50000.weights'
labelFile = model_root + 'activity_wework.names'


prob_thresh = 0.15
cls_thresh = 0.3
nms_threh = 0.45


class TwoStageModel:

  def __init__(self):

    self.det_net = cv.dnn.readNetFromDarknet(det_config,det_weights)
    self.det_layer_names = self.det_net.getLayerNames()
    self.det_layer_names = [self.det_layer_names[i[0] - 1] for i in self.det_net.getUnconnectedOutLayers()]

    self.cls_net = cv.dnn.readNetFromDarknet(cls_config, cls_weights)
    self.cls_layer_names = self.cls_net.getLayerNames()
    self.cls_layer_names = [self.cls_layer_names[i[0] - 1] for i in self.cls_net.getUnconnectedOutLayers()]

    self.labels = open(labelFile).read().strip().split('\n')

    for i in range(len(self.labels)):
        if (self.labels[i] == 'talking'): 
            print ('started engagemen t report')
            self.labels[i] = 'engaging'               

    print ('two stage model loaded!')



  def predict(self, in_path, out_img_path, out_json_path):  

    colors = [[0,255,0]]

    print ('inpath = %s' % in_path)
    img = cv.imread(in_path, cv.IMREAD_COLOR)

    height, width = img.shape[:2]

    blob = cv.dnn.blobFromImage(img, 1 / 255.0, (704, 704),
        swapRB=True, crop=False)

    self.det_net.setInput(blob)

    # Getting the outputs from the output layers
    det_outs = self.det_net.forward(self.det_layer_names)
    det_boxes, det_confidences, det_classids = yolo_utils.generate_boxes_confidences_classids(det_outs, height, width, 0.15)

    # Apply Non-Maxima Suppression to suppress overlapping bounding boxes
    det_idxs = cv.dnn.NMSBoxes(det_boxes, det_confidences, prob_thresh, nms_threh)

    patches = yolo_utils.get_boxes(img,det_boxes,det_idxs,1.4)

    preds = []
    for patch in patches:
        cls_blob = cv.dnn.blobFromImage(patch, 1 / 255.0, (256, 256),
                                    swapRB=True, crop=False)
        self.cls_net.setInput(cls_blob)
        cls_outs = self.cls_net.forward(self.cls_layer_names)
        pred = cls_outs[0].squeeze()
        pred[pred<cls_thresh] = 0
        preds.append(pred)

    img, json_data = yolo_utils.draw_labels_and_boxes_2_stage(img,det_boxes,det_idxs,preds,self.labels)

    cv.imwrite(out_img_path,img)

    with open(out_json_path, "w") as json_file:
        json.dump(json_data, json_file)


if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument('--input',
        type=str,
        help='The directory where the model weights and \
              configuration files are.')
    parser.add_argument('--output',
        type=str,
        help='The directory where the model weights and \
              configuration files are.')

    FLAGS, unparsed = parser.parse_known_args()    

    model = TwoStageModel()
    print ('flags = %s' % FLAGS)
    model.predict(FLAGS.input, FLAGS.output, '')





