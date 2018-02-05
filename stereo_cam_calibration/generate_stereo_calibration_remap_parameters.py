import numpy as np # version: '1.14.0'
import cv2 # version: '3.1.0'
import glob
import pickle
import os

# Set root directory.
rootDir = os.getcwd()
print('\nrootDir = {}\n'.format(rootDir))
# Set parameter directory.
dir_calib_parameter = rootDir+'/output/computed_calibration_parameters/'
# Set original frames directory.
dir_original_L = rootDir+'/original_frames/l/'
dir_original_R = rootDir+'/original_frames/r/'
# Set calibration process frames directory.
dir_calib_process = rootDir+'/output/calibration_process_frames/'

# Frames resolution.
widthPixel = 800
heightPixel = 600

# The inner corner numbers of calibration chessboard.
Nx = 10
Ny = 7

# termination criteria
criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 50, 1e-6)

# prepare object points, like (0,0,0), (1,0,0), (2,0,0) ....,(6,5,0)
objp = np.zeros((Nx*Ny,3), np.float32)
objp[:,:2] = np.mgrid[0:Ny,0:Nx].T.reshape(-1,2)

# Arrays to store object points and image points from all the images.
objpoints = [] # 3d point in real world space
imgpointsL = [] # 2d points in image plane.
imgpointsR = [] # 2d points in image plane.

# Load original frames.
os.chdir(dir_original_L) # Change dir to the path of left frames.
imagesL = glob.glob('*.jpg') # Grab all jpg file names.
imagesL.sort() # Sort frame file names.
os.chdir(dir_original_R) # Change dir to the path of right frames.
imagesR = glob.glob('*.jpg') # Grab all jpg file names.
imagesR.sort() # Sort frame file names.

# Check if the number of images in two folders are same.
if len(imagesL) != len(imagesR):
    print('Error: the image numbers of left and right cameras must be the same!')
    exit()

n = 0
for i in range(len(imagesL)):
    imgL = cv2.imread(dir_original_L + imagesL[i])
    imgR = cv2.imread(dir_original_R + imagesR[i])
    grayL = cv2.cvtColor(imgL,cv2.COLOR_BGR2GRAY)
    grayR = cv2.cvtColor(imgR,cv2.COLOR_BGR2GRAY)
    
    # Find the chess board corners for left camera.
    retL, cornersL = cv2.findChessboardCorners(grayL,(Ny,Nx),None)
    # Find the chess board corners for right camera.
    retR, cornersR = cv2.findChessboardCorners(grayR,(Ny,Nx),None)
    
    # If both are found, add object points, image points (after refining them)
    if (retL and retR) == True:
        n += 1
        print('n = {}'.format(n))
        objpoints.append(objp)
        
        cornersL2 = cv2.cornerSubPix(grayL,cornersL,(11,11),(-1,-1),criteria)
        imgpointsL.append(cornersL2)
        
        cornersR2 = cv2.cornerSubPix(grayR,cornersR,(11,11),(-1,-1),criteria)
        imgpointsR.append(cornersR2)
        
        # Draw and display the corners
        imgL = cv2.drawChessboardCorners(imgL, (Ny,Nx), cornersL2, retL)
        imgR = cv2.drawChessboardCorners(imgR, (Ny,Nx), cornersR2, retR)
        imgTwin = np.hstack((imgL, imgR))
        cv2.imshow(imagesL[i] + '_' + imagesR[i], imgTwin)
        cv2.waitKey(1)
        cv2.destroyAllWindows()
        # Save frame pairs.
        cv2.imwrite(dir_calib_process + imagesL[i][:-6] + '_corners.jpg', imgTwin)
        
cv2.waitKey(1) # Wait program to close the last window.
# Calculate the camera matrix, distortion coefficients, rotation and translation vectors etc.
print('Calculating the camera matrix, distortion coefficients, rotation and translation vectors...')
retL, mtxL, distL, rvecsL, tvecsL = cv2.calibrateCamera(objpoints, imgpointsL, grayL.shape[::-1],None,None)
retR, mtxR, distR, rvecsR, tvecsR = cv2.calibrateCamera(objpoints, imgpointsR, grayR.shape[::-1],None,None)
print('Done.\n')

# Calculate reprojection errors.
print('Calculating reprojection errors...')
tot_errorL = 0
tot_errorR = 0
errorL = 0
errorR = 0
for i in xrange(len(objpoints)):
    imgpointsL2, _ = cv2.projectPoints(objpoints[i], rvecsL[i], tvecsL[i], mtxL, distL)
    imgpointsR2, _ = cv2.projectPoints(objpoints[i], rvecsR[i], tvecsR[i], mtxR, distR)
    errorL = cv2.norm(imgpointsL[i],imgpointsL2, cv2.NORM_L2)/len(imgpointsL2)
    errorR = cv2.norm(imgpointsR[i],imgpointsR2, cv2.NORM_L2)/len(imgpointsR2)
    tot_errorL += errorL
    tot_errorR += errorR
print 'mean error L: ', tot_errorL/len(objpoints)
print 'mean error R: ', tot_errorR/len(objpoints)

CamParasL = {'mtxL':mtxL, 'distL':distL, 'rvecsL':rvecsL, 'tvecsL':tvecsL}
CamParasR = {'mtxR':mtxR, 'distR':distR, 'rvecsR':rvecsR, 'tvecsR':tvecsR}

# Save calibration parameters.
print('Saving calibration parameters...')
pickle.dump(CamParasL, open(dir_calib_parameter+'CamParasL.p', 'wb') )
pickle.dump(CamParasR, open(dir_calib_parameter+'CamParasR.p', 'wb') )
print('Done.\n')

# Load the dictionary back from the pickle file.
#CamParasStereo = pickle.load( open( 'CamParasStereo.p', 'rb' ) )
CamParasL = pickle.load( open(dir_calib_parameter+'CamParasL.p', 'rb' ) )
CamParasR = pickle.load( open(dir_calib_parameter+'CamParasR.p', 'rb' ) )
CamParasL.viewkeys()
CamParasR.viewkeys()

# Restore calibration parameters from loaded dictionary.
mtxL = CamParasL['mtxL']
distL = CamParasL['distL']
rvecsL = CamParasL['rvecsL']
tvecsL = CamParasL['tvecsL']
mtxR = CamParasR['mtxR']
distR = CamParasR['distR']
rvecsR = CamParasR['rvecsR']
tvecsR = CamParasR['tvecsR']

# Stereo Calibration.
# cv2.stereoCalibrate Calculate the rectify parameters for stereo cameras.
print('Cacluating the rectify parameters for stereo cameras...')
retval, cameraMatrixL, distCoeffsL, cameraMatrixR, distCoeffsR, rotationMatrix, translationVector, essentialMatrix, fundamentalMatrix = cv2.stereoCalibrate(objpoints,imgpointsL, imgpointsR, mtxL, distL, mtxR, distR, (widthPixel,heightPixel), criteria, flags=cv2.CALIB_FIX_INTRINSIC)

# cv2.stereoRectify Computes the rotation matrices for each camera that(virtually) make both image planes the same plane. The function takes the matrices computed by stereoCalibrate() as imput.
'''
Usage:
rotationMatrixL, rotationMatrixR, projectionMatrixL, projectionMatrixR, disp2depthMappingMatrix, validPixROI1, validPixROI2 = cv2.stereoRectify(cameraMatrixL, distCoeffsL, cameraMatrixR, distCoeffsR, (widthPixel,heightPixel), rotationMatrix, translationVector, alpha=1, newImageSize=(0,0))
'''
rotationMatrixL, rotationMatrixR, projectionMatrixL, projectionMatrixR, disp2depthMappingMatrix, validPixROI1, validPixROI2 = cv2.stereoRectify(cameraMatrixL, distCoeffsL, cameraMatrixR, distCoeffsR, (widthPixel,heightPixel), rotationMatrix, translationVector, flags=cv2.CALIB_ZERO_DISPARITY, alpha=1, newImageSize=(0,0))

print('CALIB_ZERO_DISPARITY = ', cv2.CALIB_ZERO_DISPARITY)
print('rotationMatrixL = ')
print(rotationMatrixL)
print('rotationMatrixR = ')
print(rotationMatrixR)
print('projectionMatrixL = ')
print(projectionMatrixL)
print('projectionMatrixR = ')
print(projectionMatrixR)
print('disp2depthMappingMatrix = ')
print(disp2depthMappingMatrix)
print('validPixROI1 = ')
print(validPixROI1)
print('validPixROI2 = ')
print(validPixROI2)

# initUndistortRectifyMap
# cv2.CV_32FC1 is floating-point format map.
# cv2.CV_16SC2 is fixed-point format map, more compact and much faster.
'''
Usage:
initUndistortRectifyMap(...)
    initUndistortRectifyMap(cameraMatrix, distCoeffs, R, newCameraMatrix, size, m1type[, map1[, map2]]) -> map1, map2
'''
mapxL, mapyL = cv2.initUndistortRectifyMap(mtxL, distL, rotationMatrixL, projectionMatrixL, (widthPixel,heightPixel), cv2.CV_32FC1)
mapxR, mapyR = cv2.initUndistortRectifyMap(mtxR, distR, rotationMatrixR, projectionMatrixR, (widthPixel,heightPixel), cv2.CV_32FC1)

print(mapxL.shape)
print(mapyR.shape)

stereoRemap = {'mapxL':mapxL, 'mapyL':mapyL, 'mapxR':mapxR, 'mapyR':mapyR}
# Save calibration parameters.
print('Saving stereo remap matrices...')
pickle.dump(stereoRemap, open(dir_calib_parameter+'stereoRemap.p', 'wb' ) )
pickle.dump(disp2depthMappingMatrix, open(dir_calib_parameter+'disp2depth.p', 'wb'))
print('Done.\n')

exit()



