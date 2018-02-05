# STEREO CAMERA CALIBRATION

## DESCRIPTION
This is stereo vision camera calibiration tool. It does not only calibrate each individual camera in stereo vision system, but also calibrate the two cameras as a whole system. The Chessborad method is used to rectify frames captured by stereo vision system. 

## PROCEDURE
### 1) Hardware Alignment
To get best result from stereo vision system, the hardware alignment should be done properly before any software calibration. Please refer to [STEREO VISION CAMERA HARDWARE ALIGNMENT](/stereo_cam_hardware_alignment/README.md) to do hardware alignment before use this calibration tool.

### 2) Capture Synchronized Original Frame Pairs.
Use the code capture_synchronized_frame_pair.py to capture frame pairs. You need about 30 or more frame pairs to do calibration. However, you can not guarantee that all frame pairs are good, so you will need to capture more frame pairs, and then select some of high quality.

### 3) Generate Stereo Calibration Remap Parameters
Run generate_stereo_calibration_remap_parameters.py to get remap parapeters. These parameters will be used in the next step to rectify original frames. They can be also used for realtime rectifying. 

### 4) Apply Remap Parameters to Original Frames to Get Rectified Frames.
