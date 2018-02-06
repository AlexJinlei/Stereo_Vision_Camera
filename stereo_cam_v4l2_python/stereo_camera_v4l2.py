import os
import numpy as np
import threading
import cv2
import time
from collections import deque
from multiprocessing import Process, Pool
from CAMERA_V4L2.v4l2_device import Camera

'''
Pixel Format : MJPG
discrete 1920x1080 ( 30 fps) # Good. FPS=10.24. decode_time=58ms. Full hardward resolution. Largest view angle.
discrete 1280x1024 ( 30 fps) # Good. FPS=15.66. decode_time=40ms. View angel is slightly larger than 320X240
discrete 1280x720  ( 60 fps) # Good. FPS=23.23. decode_time=27ms. View angel is equal to 320X240
discrete 1024x768  ( 30 fps) # Dark. FPS=26.50. decode_time=22ms. View angel is slightly larger than 320X240
discrete  800x600  ( 60 fps) # Good. FPS=38.64. decode_time=17ms. Very Narrow.
discrete  640x480  (120 fps) # Dark. FPS=58.74. decode_time=11ms. View angel is equal to 320X240
discrete  320x240  (120 fps) # Good. FPS=99.14. decode_time= 3ms. 
Pixel Format : YUYV
discrete 1920x1080 (  6 fps) # FPS= 4.97. decode_time=12 ms.
discrete 1280x1024 (  6 fps) # FPS= 4.97. decode_time=8.0ms. Narrow.
discrete 1280x720  (  9 fps) # FPS= 9.21. decode_time=6.5ms.
discrete 1024x768  (  6 fps) # FPS= 4.96. decode_time=5.5ms. Dark. 
discrete  800x600  ( 20 fps) # FPS=19.90. decode_time=2.7ms. Narrow.
discrete  640x480  ( 30 fps) # FPS=29.83. decode_time=1.8ms. View angel is smaller than 320x240.
discrete  320x240  ( 30 fps) # FPS=29.82. decode_time=0.8ms. View angel is equal to 1920x1080, white ballence differ too much.
'''

def calculateDisparity(framePair, isSGBM=False):
    # Disparity map parameters
    min_disp = 0
    num_disp = 5
    block_size = 10
    # Convert BGR to GRAY.
    gray_l = cv2.cvtColor(framePair[0], cv2.COLOR_BGR2GRAY)
    gray_r = cv2.cvtColor(framePair[1], cv2.COLOR_BGR2GRAY)
    # Select disparity computing method.
    if(isSGBM):
        stereo = cv2.StereoSGBM_create(minDisparity=min_disp, numDisparities=16*num_disp,\
        blockSize=2*block_size+1)  
    else:
        stereo = cv2.StereoBM_create(numDisparities=16*num_disp,blockSize=2*block_size+1)
    # Compute disparity.    
    disparity = stereo.compute(gray_l, gray_r)

    if 1: # post process for plot.
        # Convert to plot value.
        disparity = disparity/16 #Scale to (0~255) int16
        #print(disparity.min(), disparity.max())                
        #disparity = disparity.astype(np.float16)/disparity.max().astype(np.float16)*255.0
        disparity = disparity.astype(np.float16)/55.0*255.0
        #print(disparity.min(), disparity.max())                
        disparity = disparity.astype(np.uint8)
        #print(disparity.min(), disparity.max())
        #disparity = cv2.medianBlur(disparity, 5)
    return disparity

# Open camera.
print('\n')
cameraL = Camera('/dev/video1')
cameraR = Camera('/dev/video0')
cameraL.open()
cameraR.open()


# Initialize video device.
resolution = (1920,1080)
pixelformat = 'MJPG'  # 'YUYV' or 'MJPG'.
cameraL.init_device(resolution=resolution, pixel_format=pixelformat, exposure='AUTO', white_balance='AUTO')
cameraR.init_device(resolution=resolution, pixel_format=pixelformat, exposure='AUTO', white_balance='AUTO')

# Initialize memory map.
cameraL.init_mmap()
cameraR.init_mmap()
# Start streaming.
cameraL.stream_on()
cameraR.stream_on()

max_frame = 500
i = 1
while i < max_frame:
    print('Frame Counts = {}'.format(i))
    i += 1
    # Grab frames.
    cameraL.grab()
    cameraR.grab()
    # Get time stamp.
    current_time_in_seconds = time.time()
    ms_str = str(int(current_time_in_seconds*1000%1000))
    while (len(ms_str) < 3):
        ms_str = ms_str + '0'
    time_stamp_save = '{}.{}'.format(time.strftime('%Y%m%d_%H-%M-%S'), ms_str)
    time_stamp_display = '{}.{}'.format(time.strftime('%Y-%m-%d %H:%M:%S'), ms_str)
    # Retrieve.
    raw_frameL = cameraL.retrieve()
    raw_frameR = cameraR.retrieve()
    # Decode.
    #frameL = cameraL.decode_MJPG(raw_frameL, color=1) # Decode raw jpeg image.
    frameL = cameraL.decode_MJPG_downsample(raw_frameL, (480, 270), color=1)
    frameR = cameraR.decode_MJPG_downsample(raw_frameR, (480, 270), color=1) # Decode raw jpeg image.

    # Check if both frames are captured.
    if (frameL is not None) & (frameR is not None):
        frame_pair = np.hstack((frameL, frameR))
        cv2.putText(frame_pair,time_stamp_display,(18,28), 2, 1,(0,0,0),2)
        cv2.putText(frame_pair,time_stamp_display,(18,28), 2, 1,(255,255,255),1)
        cv2.imshow('original', frame_pair)
        cv2.waitKey(1)
        #cv2.imwrite(dir_saved_frames + time_stamp_save+'_original.jpg', frame_pair)
        
        if 1:
            disparity = calculateDisparity((frameL, frameR), isSGBM=True)
            mapcolor = 2
            disp_pseudocolor = cv2.applyColorMap(disparity.astype(np.uint8), mapcolor)
            cv2.imshow('DepthMap', disp_pseudocolor)
            cv2.waitKey(1)

# Close display windows.
cv2.destroyAllWindows()

# Turn off stream.
cameraL.stream_off()
cameraR.stream_off()

# Turn off camera.
cameraL.close()
cameraR.close()








