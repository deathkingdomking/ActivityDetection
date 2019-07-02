from yolo_model import yolo_model



if __name__ == '__main__':
	parser = argparse.ArgumentParser()	
	parser.add_argument('-m', '--model-path',
		type=str,
		default='./yolov3-coco/',
		help='The directory where the model weights and \
			  configuration files are.')	
	parser.add_argument('-w', '--weights',
		type=str,
		default='./yolov3-coco/yolov3.weights',
		help='Path to the file which contains the weights \
			 	for YOLOv3.')	
	parser.add_argument('-cfg', '--config',
		type=str,
		default='./yolov3-coco/yolov3.cfg',
		help='Path to the configuration file for the YOLOv3 model.')	
	parser.add_argument('-i', '--image-path',
		type=str,
		help='The path to the image file')	
	parser.add_argument('-v', '--video-path',
		type=str,
		help='The path to the video file')	
	parser.add_argument('-vo', '--video-output-path',
		type=str,
   	    default='./output.avi',
		help='The path of the output video file')	
	parser.add_argument('-l', '--labels',
		type=str,
		default='./yolov3-coco/coco-labels',
		help='Path to the file having the \
					labels in a new-line seperated way.')	
	parser.add_argument('-c', '--confidence',
		type=float,
		default=0.5,
		help='The model will reject boundaries which has a \
				probabiity less than the confidence value. \
				default: 0.5')	
	parser.add_argument('-th', '--threshold',
		type=float,
		default=0.3,
		help='The threshold to use when applying the \
				Non-Max Suppresion')	
	parser.add_argument('--download-model',
		type=bool,
		default=False,
		help='Set to True, if the model weights and configurations \
				are not present on your local machine.')	
	parser.add_argument('-t', '--show-time',
		type=bool,
		default=False,
		help='Show the time taken to infer each image.')	
	FLAGS, unparsed = parser.parse_known_args()	

	model = YoloModel(FLAGS)
	