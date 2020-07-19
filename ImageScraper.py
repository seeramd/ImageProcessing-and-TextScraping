import pytesseract as tess
tess.pytesseract.tesseract_cmd = r'C:\Users\dseer\AppData\Local\Tesseract-OCR\tesseract.exe'
import os
import cv2
import csv

#Insert your directory here
img_dir = 'D:\\Projects\\Collision Batch 1'

file_list = os.listdir(img_dir)
companies = []

for file in file_list:
	print('.',end = '')

	img = cv2.imread(f'{img_dir}\\{file}')
	
	#There are two main varieties of images: images with 9 companies in a 3x3 grid,
	#and images with 3 companies in a 1x3 grid. CROP_H and CROP_W represent the number
	#of pieces to be made vertically and horizontally, respectively

	#The goal in processing is to split grids into individual tiles, and then crop
	#out the company logo before passing each to tesseract
	height, width, _ = img.shape
	CROP_W = 3
	#3x3 grid images are all taller than 300px
	if height > 300:
		CROP_H = 3
	else:
		CROP_H = 1

	for ih in range(CROP_H):
		for iw in range(CROP_W):

			#Define dimensions of a given grid sector on the image
			x = int(width / CROP_W * iw)
			y = int(height / CROP_H * ih)
			h = int(height / CROP_H)
			w = int(width / CROP_W)
			
			#select the desired tile from the grid
			img2 = img[y:y+h, x:x+w]
			
			#now we slice an additional 50% off the top of each processed tile, to
			#exclude the company logo. The logos can be erroneously read by pytesseact
			height2, width2, _ = img2.shape

			#different rows have varying logospace to be croped
			if ih == 0:
				K = 0.4
			elif ih == 1:
				K = 0.5
			else:
				K = 0.66
			img2 = img2[int(height2*K):height2,0:width2]

			#IMAGE INSPECTION DEBUG
			#cv2.imshow('window',img2)
			#cv2.waitKey(0)
			#cv2.destroyAllWindows()

			#pytesseract to scrape text and add to list
			text = tess.image_to_string(img2)
			companies += [text.split('\n')]

with open("companies.csv","w", newline = '') as f:
	writer = csv.writer(f)
	writer.writerows(companies)




	

