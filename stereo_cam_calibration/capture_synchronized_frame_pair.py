import time
from datetime import datetime
import cv2 # import opencv

# Set the number of frames to be captured.
numFrames = 500

# Set dir to save frames.
rootDir = './'
dir_left_frame = rootDir + 'left/'
dir_right_frame = rootDir + 'right/'

# set video format.
camera_l = 0
camera_r = 1
widthPixel = 800
heightPixel = 600
exposure = 0.5
#framerate = 120
pixelformat = 0 # 0 is MJPEG, 1 is YUYV

# Initialize two cameras.
img_l = cv2.VideoCapture(camera_l)
img_r = cv2.VideoCapture(camera_r)
print(img_l.isOpened() and img_r.isOpened())
if (img_l.isOpened() and img_r.isOpened())==False:
    exit()

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
retl_w = img_l.set(3, widthPixel) # Set resolution width
retl_h = img_l.set(4, heightPixel) # Set resolution height
#retl_e = img_l.set(15, exposure) # Set exposure.
retr_w = img_r.set(3, widthPixel) # Set resolution width
retr_h = img_r.set(4, heightPixel) # Set resolution hight
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

print(img_l.get(8))

# Starting capture.
i = numFrames
n = 1

startTime = datetime.now()
while(i > 0):
    frameStart = datetime.now() 
    t1 = time.time()
    t_start = t1    
    img_r.grab()
    t2 = time.time()
    print('Grab 1: {} ms'.format((t2 - t1)*1000.0))
    cv2.waitKey(1)
    t1 = time.time()        
    img_l.grab()
    t2 = time.time()
    t_end = t2
    print('Grab 1: {} ms'.format((t2 - t1)*1000.0))
    #cv2.waitKey(waitTime) # if don't wait, time to grab 1 and 2 will be much different.
    
    print('Total : {} ms'.format((t_end - t_start)*1000.0))
    #if ((time2 - time1).total_seconds() < 0.1):
    
    t1 = time.time()
    ret_l, frame_l = img_l.retrieve()
    t2 = time.time()
    print('time to retrieve L: {} ms'.format((t2-t1)*1000.0))
    
    t1 = time.time()
    ret_r, frame_r = img_r.retrieve()
    t2 = time.time()
    print('time to retrieve R: {} ms'.format((t2-t1)*1000.0))
    
    # Resize images.
    #frame_l = cv2.resize(frame_l, (320,240))
    #frame_r = cv2.resize(frame_r, (320,240))
    
    cv2.imwrite(dir_left_frame+'/frame' + str(n) + '_l.jpg', frame_l)
    cv2.imwrite(dir_right_frame+'/frame' + str(n) + '_r.jpg', frame_r)
    n += 1
                
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

exit()

