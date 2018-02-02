# STEREO VISION CAMERA DRIVER BASED ON V4L2
## 1. DESCRIPTION
This code set is developed as a complement of the camera control functions in OpenCV. In cv2 package, the camera control functions are not well developed, as a result, many camara control parameter can not be set appropriately via the camera control functions in cv2 package. When builting a stereo vision camera, we need to accurately control the parameters of the two cameras, such as exposure, frame rate, resolution, image format, and so on. However, it always fails when set these parameters via cv2 functions. This code set is based on v4l2 API which is built in almost all Linux OS. It can achieve the fundamental control on the cameras that work with v4l2 standards. This code set is developed in reference to [Linux Media Infrastructure userspace API](https://linuxtv.org/downloads/v4l-dvb-apis/media_uapi.html).

## 2. FUNCTIONS
### 1) v4l2_cam_driver.c
- int open_device\(char \*device_name, bool block\)
- int close_device\(int fd\)
- void get_supported_format(int fd)
- int set_video_format(int fd, int frame_width, int frame_height, unsigned int pixelformat)
- int get_video_format(int fd)
- void enumerate_all_controls(int fd)
- int get_control_parameter(int fd, int control_ID)
- int set_control_parameter(int fd, int control_ID, int control_value)
- int get_supported_frame_size_and_fps(int fd)
