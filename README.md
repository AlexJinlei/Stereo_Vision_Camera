# Stereo Vision Camera
## 1. DESCRIPTION
Stereo vision camera is widely used in depth detection and 3D reconstruction on a varies of places, such as UAVs and other robotics. In this project, I build a stereo vision camera system using two USB cameras which work with v4l2 standards. The is project contains the hardware built procedure, camera optical axis alignment method, image rectification procedure, and the real time depth map generation method.

## 2. HARDWARE CONFIGURATION
### 1) Board Camera Module
ELP-USBFHD01M-FV board camera.

### 2) Baseline
Baseline = 140mm

### 3) Focal Length
Focal Length = 4.35mm low distortion lens

### 4) Supported Frame Format
Pixel Format : MJPG  
- 1) discrete 1920x1080 ( 30 fps) # Good. FPS=10.24. decode_time=58ms. Full hardward resolution. Largest view angle.
- 2) discrete 1280x1024 ( 30 fps) # Good. FPS=15.66. decode_time=40ms. View angel is slightly larger than 320X240
- 3) discrete 1280x720  ( 60 fps) # Good. FPS=23.23. decode_time=27ms. View angel is equal to 320X240
- 4) discrete 1024x768  ( 30 fps) # Dark. FPS=26.50. decode_time=22ms. View angel is slightly larger than 320X240
- 5) discrete  800x600  ( 60 fps) # Good. FPS=38.64. decode_time=17ms. Very Narrow.
- 6) discrete  640x480  (120 fps) # Dark. FPS=58.74. decode_time=11ms. View angel is equal to 320X240
- 7) discrete  320x240  (120 fps) # Good. FPS=99.14. decode_time= 3ms. 

Pixel Format : YUYV
- 1) discrete 1920x1080 (  6 fps) # FPS= 4.97. decode_time=12 ms.
- 2) discrete 1280x1024 (  6 fps) # FPS= 4.97. decode_time=8.0ms. Narrow.
- 3) discrete 1280x720  (  9 fps) # FPS= 9.21. decode_time=6.5ms.
- 4) discrete 1024x768  (  6 fps) # FPS= 4.96. decode_time=5.5ms. Dark. 
- 5) discrete  800x600  ( 20 fps) # FPS=19.90. decode_time=2.7ms. Narrow.
- 6) discrete  640x480  ( 30 fps) # FPS=29.83. decode_time=1.8ms. View angel is smaller than 320x240.
- 7) discrete  320x240  ( 30 fps) # FPS=29.82. decode_time=0.8ms. View angel is equal to 1920x1080, white ballence differ too much.

## 3. SOFTWARE CONFIGURATION
This project uses two method to build the software of stereo vision camera system. One method is using the builtin functions in opencv to control the camera hardware. However, upon testing, some camera control functions is not well implemented in opencv. I developed a new software stack working around opencv. I use v4l2 API to control camera hardware directly. The code in folder [stereo_cam_opencv](stereo_cam_opencv/) is develped in opencv framework. The code in 
