import numpy as np
import cv2
import serial
import time

arduino = serial.Serial("COM4",9600)


def check(cnt):
	perimeter = cv2.arcLength(cnt, True)
	area = cv2.contourArea(cnt)
	circularity = 4*math.pi*(area/perimeter*perimeter)
	if 0.8 < circularity < 1.2:
		return 1
	else:
		return 0


def read():
	global arg 
	frames = []
	cap = cv2.VideoCapture(1)
	i=1
	while True:
		_,frame = cap.read()
		cv2.imshow('frame',frame)
		k = cv2.waitKey(5) & 0xFF
		if(k == 27):
			break
		
	img = frame
	cap.release()

	x,y,z = img.shape
	gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
	ret,thresh = cv2.threshold(gray,150,255,cv2.THRESH_BINARY_INV)

	cnt = []
	final = cv2.morphologyEx(thresh,cv2.MORPH_OPEN,(7,7))
	_,contours,hierarchy = cv2.findContours(final, cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)#finding contours 
	for i in range(len(contours)):
		if len(contours[i]) > len(cnt):
			cnt = contours[i]
	x,y,w,h = cv2.boundingRect(cnt)
	cv2.rectangle(img,(x,y),(x+w,y+h),(0,255,0),2)
	epsilon = 0.01*cv2.arcLength(cnt,True)
	approx = cv2.approxPolyDP(cnt,epsilon,True)

	
	print(approx)
	arg = len(approx)
	print(arg)

	



def decide():
	global arg
	frames = []
	cap = cv2.VideoCapture(1)
	i=1
	while True:
		_,frame = cap.read()
		if i <= 50:
			frames.append(frame)
			i += 1
		if i > 50:
			break
	cap.release()
	img = frames[25]
	
	x,y,z = img.shape
	gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
	ret,thresh = cv2.threshold(gray,150,255,cv2.THRESH_BINARY_INV)

	cnt = []
	final = cv2.morphologyEx(thresh,cv2.MORPH_OPEN,(7,7))
	_,contours,hierarchy = cv2.findContours(final, cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)#finding contours 
	for i in range(len(contours)):
		if len(contours[i]) > len(cnt):
			cnt = contours[i]
	x,y,w,h = cv2.boundingRect(cnt)
	cv2.rectangle(img,(x,y),(x+w,y+h),(0,255,0),2)
	epsilon = 0.01*cv2.arcLength(cnt,True)
	approx = cv2.approxPolyDP(cnt,epsilon,True)
	
	print(len(approx))
	if(len(approx)==arg or (arg>12 and len(approx)>12)):
		print("found")
		cap.release()
		if(len(approx)==3 and arg<13 ):
			print("triangle")
			k = check(cnt)
			print(k)
			serial.write(b'c')
			
		elif(len(approx)==4 and arg<13):
			print("rectangle")
			k = check(cnt)
			print(k)
			serial.write(b'c')
			
		elif(len(approx)==5 and arg<13):
			print("pentagon")
			k = check(cnt)
			print(k)
			serial.write(b'c')
			
		elif(len(approx)==12 and arg<13):
			print("star")
			k = check(cnt)
			print(k)
			serial.write(b'c')

		elif(arg>12 and len(approx)>12):
			print("circle")
			k = check(cnt)
			print(k)
			serial.write(b'c')
			
	else:
		print("turn right")
		serial.write(b'g')
		#decide(arg)	
			



read()
cv2.waitKey(3000)
decide()