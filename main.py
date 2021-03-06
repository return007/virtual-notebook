import numpy as np
import cv2

def nothing():
	pass

cap = cv2.VideoCapture(0)

# cv2.namedWindow('Colorbars')
# hh='Hue High'
# hl='Hue Low'
# sh='Saturation High'
# sl='Saturation Low'
# vh='Value High'
# vl='Value Low'
# wnd = 'Colorbars'
# #Begin Creating trackbars for each
# cv2.createTrackbar(hl, wnd,0,179,nothing)
# cv2.createTrackbar(hh, wnd,0,179,nothing)
# cv2.createTrackbar(sl, wnd,0,255,nothing)
# cv2.createTrackbar(sh, wnd,0,255,nothing)
# cv2.createTrackbar(vl, wnd,0,255,nothing)
# cv2.createTrackbar(vh, wnd,0,255,nothing)

drawing = np.ndarray((cap.get(4), cap.get(3), 3))
drawing.fill(255)
color_tuple = (0,0,0) # defines color of ink, by default its black

while True:
	_, frame = cap.read()
	frame = cv2.flip(frame, 1)
	
	frame_hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)	
	#read trackbar positions for each trackbar
	# hul=cv2.getTrackbarPos(hl, wnd)
	# huh=cv2.getTrackbarPos(hh, wnd)
	# sal=cv2.getTrackbarPos(sl, wnd)
	# sah=cv2.getTrackbarPos(sh, wnd)
	# val=cv2.getTrackbarPos(vl, wnd)
	# vah=cv2.getTrackbarPos(vh, wnd)

	# #make array for final values
	# HSVLOW=np.array([hul,sal,val])
	# HSVHIGH=np.array([huh,sah,vah])

	HSVLOW = np.array([39, 65, 0])
	HSVHIGH = np.array([92, 255, 255])
 
	#create a mask for that range
	mask = cv2.inRange(frame_hsv,HSVLOW, HSVHIGH)
	img = cv2.bitwise_and(frame, frame, mask = mask)
	blur = cv2.GaussianBlur(img, (5,5), 0)
	
	kernal = np.ones((9,9), np.uint8)
	erosion = cv2.erode(blur, kernal, iterations = 1)
	dilation = cv2.dilate(erosion, kernal, iterations = 2)

	dilation2gray = cv2.cvtColor(dilation, cv2.COLOR_BGR2GRAY)
	_, threshold1 = cv2.threshold(dilation2gray, 5, 255, cv2.THRESH_BINARY)

	contours, hierarchy = cv2.findContours(threshold1,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE) # get contours
	
	for contour in contours:
    	# get rectangle bounding contour
		x,y,w,h = cv2.boundingRect(contour)
    	# discard areas that are too large
		if h>200 and w>200:
			continue
		# discard areas that are too small
		if h<10 or w<10:
			continue
    	# draw rectangle around contour on original image
		# cv2.rectangle(frame,(x,y),(x+w,y+h),(0,0,0),4)
		# drawing[y-2:y+2,x-2:x+2] = 0
		cv2.circle(drawing, (x,y), 5, color_tuple, -1)

	# cv2.imshow('img',img)
	# cv2.imshow('blur',blur)
	# cv2.imshow('erosion',erosion)
	#  cv2.imshow('dilation',threshold1)
	# cv2.imshow('frame',frame)
	cv2.imshow('Virtual Notebook',drawing)

	k = cv2.waitKey(1) & 0xFF
	if k == ord('q') :
		break
	elif k == ord('g') or k == ord('G') :
		color_tuple = (0, 255, 0)
	elif k == ord('r') or k == ord('R') :
		color_tuple = (0, 0, 255)
	elif k == ord('b') or k == ord('B') :
		color_tuple = (255, 0, 0)
	
cv2.destroyAllWindows()
cap.release()