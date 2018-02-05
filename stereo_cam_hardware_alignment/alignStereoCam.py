'''
0 CV_CAP_PROP_POS_MSEC Current position of the video file in milliseconds.
1	CV_CAP_PROP_POS_FRAMES 0-based index of the frame to be decoded/captured next.
2	CV_CAP_PROP_POS_AVI_RATIO Relative position of the video file
3	CV_CAP_PROP_FRAME_WIDTH Width of the frames in the video stream.
4	CV_CAP_PROP_FRAME_HEIGHT Height of the frames in the video stream.
5	CV_CAP_PROP_FPS Frame rate.
6	CV_CAP_PROP_FOURCC 4-character code of codec.
7	CV_CAP_PROP_FRAME_COUNT Number of frames in the video file.
8	CV_CAP_PROP_FORMAT Format of the Mat objects returned by retrieve() .
9	CV_CAP_PROP_MODE Backend-specific value indicating the current capture mode.
10	CV_CAP_PROP_BRIGHTNESS Brightness of the image (only for cameras).
11	CV_CAP_PROP_CONTRAST Contrast of the image (only for cameras).
12	CV_CAP_PROP_SATURATION Saturation of the image (only for cameras).
13	CV_CAP_PROP_HUE Hue of the image (only for cameras).
14	CV_CAP_PROP_GAIN Gain of the image (only for cameras).
15	CV_CAP_PROP_EXPOSURE Exposure (only for cameras).
16	CV_CAP_PROP_CONVERT_RGB Boolean flags indicating whether images should be converted to RGB.
17	CV_CAP_PROP_WHITE_BALANCE Currently unsupported
18	CV_CAP_PROP_RECTIFICATION Rectification flag for stereo cameras (note: only supported by DC1394 v 2.x backend currently)

COLORMAP_AUTUMN = 0
COLORMAP_BONE = 1
COLORMAP_COOL = 8
COLORMAP_HOT = 11
COLORMAP_HSV = 9
COLORMAP_JET = 2
COLORMAP_OCEAN = 5
COLORMAP_PINK = 10
COLORMAP_RAINBOW = 4
COLORMAP_SPRING = 7
COLORMAP_SUMMER = 6
COLORMAP_WINTER = 3
'''

import numpy as np
import time
from datetime import datetime
import cv2
from cv2 import *
import os
import sys
import pickle
#import scipy.io
#from matplotlib import pyplot as plt



isSave = 0
isBlend = 1
addCross = 1
isSep = 0
isDisparity = 0
isSGBM = 0
isRemap = 0
isDisplay = 1
isShow = 1
numFrames = 30*60*20
isMedian = 0
median = 9

#Disparity map parameters
min_disp = 0
num_disp = 4
block_size = 10
mapcolor = 2

# set video format.
camera_l = 1
camera_r = 0
width = 1280
height = 800

FPS = 30
exposure = 0.5
#framerate = 120
pixelformat = 0 # 0 is MJPEG, 1 is YUYV


            
'''
for device in [camera_l,camera_r]:
     os.system("v4l2-ctl -d {} --set-fmt-video=width={},height={},pixelformat={}".format(device,width,height,pixelformat)) 
     os.system("v4l2-ctl -d {} --set-parm={}".format(device,FPS))
     os.system("v4l2-ctl -d {} -V".format(device))
'''

'''
# Load the dictionary back from the pickle file.
stereoRemap = pickle.load( open( 'stereoRemap.p', 'rb' ) )
mapxL = stereoRemap['mapxL']
mapyL = stereoRemap['mapyL']
mapxR = stereoRemap['mapxR']
mapyR = stereoRemap['mapyR']
'''


'''
# Load the dictionary back from the pickle file.
CamParasStereo = pickle.load( open( "CamParasStereo.p", "rb" ) )
CamParasL = pickle.load( open( "CamParasL.p", "rb" ) )
CamParasR = pickle.load( open( "CamParasR.p", "rb" ) )
#CamParasL.viewkeys()
CamParasR.viewkeys()
print(CamParasStereo.viewkeys())
mtxL = CamParasL['mtxL']
distL = CamParasL['distL']
rvecsL = CamParasL['rvecsL']
tvecsL = CamParasL['tvecsL']
mtxR = CamParasR['mtxR']
distR = CamParasR['distR']
rvecsR = CamParasR['rvecsR']
tvecsR = CamParasR['tvecsR']
'''
widthPixel = width
heightPixel = height

img_l = cv2.VideoCapture(camera_l)
img_r = cv2.VideoCapture(camera_r)
print(img_l.isOpened() and img_r.isOpened())
if (img_l.isOpened() and img_r.isOpened())==False:
    exit()

#retl_FPS = img_l.set(5, FPS)
#retr_FPS = img_l.set(5, FPS)
#print 'Left camera FPS is set:', retl_FPS
#print 'Left camera FPS is set:', retr_FPS

#Check the camera initial setting
print('The default setting is: ')
fps_l = img_l.get(5)
fps_r = img_r.get(5)
print "FPS_l: {0}".format(fps_l)
print "FPS_r: {0}".format(fps_r)
width_l = img_l.get(3)
hight_l = img_l.get(4)
print('Resolution of left camera: ({}X{})'.format(width_l, hight_l))
width_r = img_l.get(3)
hight_r = img_l.get(4)
print('Resolution of right camera: ({}X{})\n'.format(width_r, hight_r))

#User set camera
retl_w = img_l.set(3, width) # Set resolution width
retl_h = img_l.set(4, height) # Set resolution height
#retl_e = img_l.set(15, exposure) # Set exposure.
retr_w = img_r.set(3, width) # Set resolution width
retr_h = img_r.set(4, height) # Set resolution hight
#retr_e = img_r.set(15, exposure) # Set exposure.
print 'Left camera resolution width is set:', retl_w
print 'Left camera resolution height is set:', retl_h
print 'Right camera resolution width is set:', retr_w
print 'Right camera resolution height is set:', retr_h

width_l = img_l.get(3)
hight_l = img_l.get(4)
print('Resolution of left camera: ({}X{})'.format(width_l, hight_l))
width_r = img_l.get(3)
hight_r = img_l.get(4)
print('Resolution of right camera: ({}X{})'.format(width_r, hight_r))

fps_l = img_l.get(5)
fps_r = img_r.get(5)
print "FPS of the  left camera: {0}".format(fps_l)
print "FPS of the right camera: {0}".format(fps_r)

#exit()

i = numFrames
n = 1
realFPS = 20
startTime = datetime.now()
while(i > 0):
    frameStart = datetime.now() 
    time0 = datetime.now()    
    img_r.grab()
    time1 = datetime.now()    
    img_l.grab()
    time2 = datetime.now()
    #cv2.waitKey(waitTime) # if don't wait, time to grab 1 and 2 will be much different.
    
    print('Grab 1: ',(time1 - time0).total_seconds())
    print('Grab 2: ',(time2 - time1).total_seconds())
    print('Total : ',(time2 - time0).total_seconds())
    #if ((time2 - time1).total_seconds() < 0.1):
    ret_l, frame_l = img_l.retrieve()
    ret_r, frame_r = img_r.retrieve()

    if(isSave):
        cv2.imwrite('/home/zhengj/Desktop/left/frame' + str(n) + '_l.jpg', frame_l)
        cv2.imwrite('/home/zhengj/Desktop/right/frame' + str(n) + '_r.jpg', frame_r)
        n += 1
    
    if(isDisplay):
        if(isRemap):
            '''
            frame_l = cv2.undistort(frame_l, mtxL, distL, rotationMatrixL, newmtxL)
            frame_r = cv2.undistort(frame_r, mtxR, distR, rotationMatrixR, newmtxR)
            '''
            # remap
            frame_l = cv2.remap(frame_l, mapxL, mapyL, cv2.INTER_LINEAR)
            frame_r = cv2.remap(frame_r, mapxR, mapyR, cv2.INTER_LINEAR)
    
        if(isBlend):
            blended = cv2.addWeighted(frame_l, 0.7, frame_r, 0.5, 0)
            #blended = cv2.resize(blended, (1024,768))
	    if addCross:
		# Add a blue horizontal line in center.
		blended = cv2.line(blended, (0, height/2), (width, height/2), (255,0,0), 1)
		# Add a blue verticle line in center.
                blended = cv2.line(blended, (width/4, 0), (width/4, height), (255,0,0), 1)

		blended = cv2.line(blended, (0, height/4), (width, height/4), (255,0,0), 1)
                blended = cv2.line(blended, (width/2, 0), (width/2, height), (255,0,0), 1)
		blended = cv2.line(blended, (0, height/4 * 3), (width, height/4 * 3), (255,0,0), 1)
                blended = cv2.line(blended, (width/4 * 3, 0), (width/4 * 3, height), (255,0,0), 1)
		
            cv2.imshow('blended',blended)
            
        elif(isSep):
            #gray_l = cv2.cvtColor(frame_l,cv2.COLOR_BGR2GRAY)
            #gray_r = cv2.cvtColor(frame_r,cv2.COLOR_BGR2GRAY)
            #imgTwin = np.hstack((gray_l, gray_r))
	    imgTwin = np.hstack((frame_l, frame_r))
            cv2.imshow('frame_l  frame_r',imgTwin)

        elif(isDisparity):
            gray_l = cv2.cvtColor(frame_l,cv2.COLOR_BGR2GRAY)
            gray_r = cv2.cvtColor(frame_r,cv2.COLOR_BGR2GRAY)

            '''
            imgTwin = np.hstack((frame_l, frame_r))
            imgTwin = cv2.resize(imgTwin,(800,300))
            cv2.imshow('frame_l  frame_r',imgTwin)
            '''

            if(isSGBM):
                stereo = cv2.StereoSGBM_create(minDisparity=min_disp, numDisparities=16*num_disp,\
                blockSize=2*block_size+1)
            else:
                stereo = cv2.StereoBM_create(numDisparities=16*num_disp,blockSize=2*block_size+1)
            
            disparity = stereo.compute(gray_l, gray_r)

            if 1: # post process for plot.
                #print(type(disparity[0,0]))
                disparity = disparity/16 #Scale to (0~255) int16
                #print(disparity.min(), disparity.max())
            
                disparity = disparity.astype(np.float16)/disparity.max().astype(np.float16)*255.0
                #print(type(disparity[0,0]))
                #print(disparity.min(), disparity.max())
            
                disparity = disparity.astype(np.uint8)
                #print(type(disparity[0,0]))
                #print(disparity.min(), disparity.max())
            
            #disparity = cv2.resize(disparity,(80,60))
	    if isMedian:
            	disparity = cv2.medianBlur(disparity, median)
            #disparity = cv2.resize(disparity,(320,240),interpolation = cv2.INTER_AREA)
            
	    if isShow:
            	disp_pseudocolor = cv2.applyColorMap(disparity.astype(np.uint8), mapcolor)
            	#disp_pseudocolor = cv2.resize(disp_pseudocolor, (800,600))
            	#dispAndLeft = np.hstack((frame_l, disp_pseudocolor))
            	cv2.imshow('DepthMap', disp_pseudocolor)
            

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    i = i - 1

    frameEnd = datetime.now()
    elapsedTime = int((frameEnd - frameStart).total_seconds()*1000)
    print('Elapsed Time : ', elapsedTime, 'ms')
    waitTime = 1000//realFPS - elapsedTime - 4
    if (waitTime > 0):        
        cv2.waitKey(waitTime)
        print('Wait ', waitTime, 'ms')
        
endTime = datetime.now()     
print('FPS : ',numFrames/(endTime - startTime).total_seconds())
  
img_l.release()
img_r.release()
cv2.destroyAllWindows()
