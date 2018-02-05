import numpy as np # version: '1.14.0'
import cv2 # version: '3.1.0'
import glob
import pickle
import os

# Set root directory.
rootDir = os.getcwd()
print('\nrootDir = {}\n'.format(rootDir))
# Set parameter directory.
dir_stereoRemap = rootDir+'/output/computed_calibration_parameters/stereoRemap.p'
# Set original frames directory.
dir_original_L = rootDir+'/original_frames/l/'
dir_original_R = rootDir+'/original_frames/r/'
# Set compare frames directory.
dir_compare_frame_pairs = rootDir+'/output/compare_rectified_frame_pairs/'
# Set rectified frames directory.
dir_rectified_L = rootDir+'/output/rectified_frames/l/'
dir_rectified_R = rootDir+'/output/rectified_frames/r/'

# Load the dictionary back from the pickle file.
stereoRemap = pickle.load( open(dir_stereoRemap, 'rb') )
mapxL = stereoRemap['mapxL']
mapyL = stereoRemap['mapyL']
mapxR = stereoRemap['mapxR']
mapyR = stereoRemap['mapyR']

# Load original frames.
os.chdir(dir_original_L) # Change dir to the path of left frames.
imagesL = glob.glob('*.jpg') # Grab all jpg file names.
imagesL.sort() # Sort frame file names.
os.chdir(dir_original_R) # Change dir to the path of right frames.
imagesR = glob.glob('*.jpg') # Grab all jpg file names.
imagesR.sort() # Sort frame file names.

# Rectify each frame.
for i in range(len(imagesL)):
    print('i = {}'.format(i))
    print('Rectifying {} and {}...\n'.format(imagesL[i], imagesR[i]))
    imgL = cv2.imread(dir_original_L + imagesL[i])
    imgR = cv2.imread(dir_original_R + imagesR[i])
    hL,  wL = imgL.shape[:2]
    hR,  wR = imgR.shape[:2]
    
    # Remap.
    dstL = cv2.remap(imgL, mapxL, mapyL, cv2.INTER_LINEAR)
    dstR = cv2.remap(imgR, mapxR, mapyR, cv2.INTER_LINEAR)
    
    # Combine frame pairs.
    imgTwin = np.hstack((imgL, imgR))
    imgTwin_rect = np.hstack((dstL, dstR))
    compareImg = np.vstack((imgTwin, imgTwin_rect))
    compareImg = cv2.resize(compareImg, (1024,768))
    # Display comparing frame pairs.
    cv2.imshow(imagesL[i]+'_'+imagesR[i], compareImg)
    cv2.waitKey(1)
    cv2.destroyAllWindows()
    # Save comparing frame pairs.
    cv2.imwrite(dir_compare_frame_pairs + imagesL[i][:-6] + '_rectified.jpg', compareImg)
    
    # Save rectified frames.
    cv2.imwrite(dir_rectified_L + imagesL[i][:-4] + '_rectified.jpg', dstL)
    cv2.imwrite(dir_rectified_R + imagesL[i][:-4] + '_rectified.jpg', dstR)
    
exit()






