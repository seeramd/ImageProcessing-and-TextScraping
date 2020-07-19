import numpy as np
import os
import cv2

#SOURCE: https://stackoverflow.com/questions/49907382/how-to-remove-whitespace-from-an-image-in-opencv

img_dir = 'D:\\Projects\\Collision Batch 1'
file_list = os.listdir(img_dir)
for file in file_list:
	img = cv2.imread(f'{img_dir}\\{file}') # Read in the image and convert to grayscale
	gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
	gray = 255*(gray < 128).astype(np.uint8) # To invert the text to white
	coords = cv2.findNonZero(gray) # Find all non-zero points (text)
	x, y, w, h = cv2.boundingRect(coords) # Find minimum spanning bounding box
	rect = img[y:y+h, x:x+w] # Crop the image - note we do this on the original image
	#cv2.imshow("Cropped", rect) # Show it
	#cv2.waitKey(0)
	#cv2.destroyAllWindows()
	cv2.imwrite(f'{img_dir}\\{file}', rect)