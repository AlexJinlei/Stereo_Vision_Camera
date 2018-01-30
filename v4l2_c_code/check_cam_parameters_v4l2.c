#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <assert.h>

#include <getopt.h>             /* getopt_long() */

#include <fcntl.h>              /* low-level i/o */
#include <unistd.h>
#include <errno.h>
#include <sys/stat.h>
#include <sys/types.h>
#include <sys/time.h>
#include <sys/mman.h>
#include <sys/ioctl.h>

#include <linux/videodev2.h>

#define CLEAR(x) memset(&(x), 0, sizeof(x))

typedef enum {false, true} bool;
//typedef enum {MJPG, YUYV} pixelformat;

struct buffer {
        void   *start;
        size_t  length;
};

static int xioctl(int fd, int request, void *arg)
{   
    // xioctl is a wrapper of ioctl. For some control IDs, the return value of ioctl is not -1
    // when operation fails. xioctl fix this issue. xioctl return 0 when succeeds, -1 when fails.
        int r;
        do r = ioctl (fd, request, arg);
        while (-1 == r && EINTR == errno);
        return r;
}

void get_v4l2_ctrl_type_string(int enum_type, char *type_string)
{   
    // The length of type_string must be no less than 27 (The longest returned string).
    switch(enum_type){
        case 1:
            strcpy(type_string, "V4L2_CTRL_TYPE_INTEGER");
            break;
        case 2:
            strcpy(type_string, "V4L2_CTRL_TYPE_BOOLEAN");
            break;
        case 3:
            strcpy(type_string, "V4L2_CTRL_TYPE_MENU");
            break;
        case 4:
            strcpy(type_string, "V4L2_CTRL_TYPE_BUTTON");
            break;
        case 5:
            strcpy(type_string, "V4L2_CTRL_TYPE_INTEGER64");
            break;
        case 6:
            strcpy(type_string, "V4L2_CTRL_TYPE_CTRL_CLASS");
            break;
        case 7:
            strcpy(type_string, "V4L2_CTRL_TYPE_BITMASK");
            break;
        case 8:
            strcpy(type_string, "V4L2_CTRL_TYPE_INTEGER_MENU");
            break;
        case 0x0100:
            strcpy(type_string, "V4L2_CTRL_TYPE_U8");
            break;
        case 0x0101:
            strcpy(type_string, "V4L2_CTRL_TYPE_U16");
            break;
        case 0x0102:
            strcpy(type_string, "V4L2_CTRL_TYPE_U32");
            break;
        default:
            strcpy(type_string, "Error: Invalid Input.");
            break; 
    }       
}


void get_v4l2_ctrl_flags_string(int enum_flags, char *flags_string)
{
    // The length of flags_string must be no less than 31 (The longest returned string).
    switch(enum_flags){
        case 0x0000:
            strcpy(flags_string, "NONE");
            break;
        case 0x0001:
            strcpy(flags_string, "V4L2_CTRL_FLAG_DISABLED");
            break;
        case 0x0002:
            strcpy(flags_string, "V4L2_CTRL_FLAG_GRABBED");
            break;
        case 0x0004:
            strcpy(flags_string, "V4L2_CTRL_FLAG_READ_ONLY");
            break;
        case 0x0008:
            strcpy(flags_string, "V4L2_CTRL_FLAG_UPDATE");
            break;
        case 0x0010:
            strcpy(flags_string, "V4L2_CTRL_FLAG_INACTIVE");
            break;
        case 0x0020:
            strcpy(flags_string, "V4L2_CTRL_FLAG_SLIDER");
            break;
        case 0x0040:
            strcpy(flags_string, "V4L2_CTRL_FLAG_WRITE_ONLY");
            break;
        case 0x0080:
            strcpy(flags_string, "V4L2_CTRL_FLAG_VOLATILE");
            break;
        case 0x0100:
            strcpy(flags_string, "V4L2_CTRL_FLAG_HAS_PAYLOAD");
            break;
        case 0x0200:
            strcpy(flags_string, "V4L2_CTRL_FLAG_EXECUTE_ON_WRITE");
            break;
        case 0x0400:
            strcpy(flags_string, "V4L2_CTRL_FLAG_MODIFY_LAYOUT");
            break;
        case 0x80000000:
            strcpy(flags_string, "V4L2_CTRL_FLAG_NEXT_CTRL");
            break;
        case 0x40000000:
            strcpy(flags_string, "V4L2_CTRL_FLAG_NEXT_COMPOUND");
            break;
        default:
            strcpy(flags_string, "Error: Invalid Input.");
            break;
    }
}


void get_v4l2_control_ID_string(int control_ID, char *control_ID_string)
{
    //The following control_ID is supported by ELP-USBFHD01M-FV board camera.
    switch(control_ID){
        case V4L2_CID_BRIGHTNESS:
            strcpy(control_ID_string, "V4L2_CID_BRIGHTNESS");
            break;
        case V4L2_CID_CONTRAST:
            strcpy(control_ID_string, "V4L2_CID_CONTRAST");
            break;
        case V4L2_CID_SATURATION:
            strcpy(control_ID_string, "V4L2_CID_SATURATION");
            break;
        case V4L2_CID_HUE:
            strcpy(control_ID_string, "V4L2_CID_HUE");
            break;           
        case V4L2_CID_AUTO_WHITE_BALANCE:
            strcpy(control_ID_string, "V4L2_CID_AUTO_WHITE_BALANCE");
            break;
        case V4L2_CID_GAMMA:
            strcpy(control_ID_string, "V4L2_CID_GAMMA");
            break;
        case V4L2_CID_GAIN:
            strcpy(control_ID_string, "V4L2_CID_GAIN");
            break;
        case V4L2_CID_POWER_LINE_FREQUENCY:
            strcpy(control_ID_string, "V4L2_CID_POWER_LINE_FREQUENCY");
            break;           
        case V4L2_CID_WHITE_BALANCE_TEMPERATURE:
            strcpy(control_ID_string, "V4L2_CID_WHITE_BALANCE_TEMPERATURE");
            break;
        case V4L2_CID_SHARPNESS:
            strcpy(control_ID_string, "V4L2_CID_SHARPNESS");
            break;
        case V4L2_CID_BACKLIGHT_COMPENSATION:
            strcpy(control_ID_string, "V4L2_CID_BACKLIGHT_COMPENSATION");
            break;
        case V4L2_CID_EXPOSURE_AUTO:
            strcpy(control_ID_string, "V4L2_CID_EXPOSURE_AUTO");
            break;           
        case V4L2_CID_EXPOSURE_ABSOLUTE:
            strcpy(control_ID_string, "V4L2_CID_EXPOSURE_ABSOLUTE");
            break;
        case V4L2_CID_EXPOSURE_AUTO_PRIORITY:
            strcpy(control_ID_string, "V4L2_CID_EXPOSURE_AUTO_PRIORITY");
            break;
        default:
            strcpy(control_ID_string, "Error: Invalid Input.");
            break;    
    }
}


int open_device(char *device_name, bool block)
{   /*
    1) This function return a int type file descriptor (fd). When close device, just call close(fd).
    2) Access mode must be O_RDWR.
    3) When the O_NONBLOCK flag is given, the read() function and the VIDIOC_DQBUF ioctl will return
    the EAGAIN error code when no data is available or no buffer is in the driver outgoing queue,
    otherwise these functions block until data becomes available.
    */
    int fd;
    if (block){
        //printf("\n");
        printf("Opening device %s in blocking mode...\n", device_name);
        fd = open(device_name, O_RDWR, 0); //Block mode. Wait until buffer is filled.
        if (-1==fd){
        printf("Failed to open device %s.\n", device_name);
        }
        else{
        printf("Device %s is opened successfully, fd=%d.\n", device_name, fd);
        }
    }
    else{
        printf("Opening device %s in nonblocking mode...\n", device_name);
        fd = open(device_name, O_RDWR | O_NONBLOCK, 0); //Nonblock mode.
        if (-1==fd){
        printf("Failed to open device %s.\n", device_name);
        }
        else{
        printf("Device %s is opened successfully, fd=%d.\n", device_name, fd);
        }
    }
    printf("\n");
    return fd;
}


int close_device(int fd)
{
    printf("Closeing device with fd=%d...\n", fd);
    if(0 == close(fd)){
        printf("Device (fd=%d) is closed successfully.\n", fd);
    }
    else{
        printf("Failed to close device (fd=%d).\n", fd);
    }
    printf("\n");
}


void get_supported_format(int fd)
{
    struct v4l2_fmtdesc fmtdesc;
    memset(&fmtdesc, 0, sizeof(fmtdesc));
    fmtdesc.index=0;  
    fmtdesc.type = V4L2_BUF_TYPE_VIDEO_CAPTURE;
    printf("The supported pixel formats on device (fd=%d) are:\n",fd); 
    while (0 == xioctl(fd, VIDIOC_ENUM_FMT, &fmtdesc)){  
        printf("{ pixelformat = '%c%c%c%c', description = '%s' }\n",
        fmtdesc.pixelformat & 0xFF,
        (fmtdesc.pixelformat>> 8) & 0xFF,
        (fmtdesc.pixelformat>>16) & 0xFF,
        (fmtdesc.pixelformat>>24) & 0xFF,
        fmtdesc.description);
        
        fmtdesc.index++;
    }
    printf("\n");
}

int set_video_format(int fd, int frame_width, int frame_height, unsigned int pixelformat)
{   
    // The following pixel formats are supported by ELP-USBFHD01M-FV board camera.
    // MJPG: V4L2_PIX_FMT_MJPEG
    // YUYV: V4L2_PIX_FMT_YUYV.
    // Only V4L2_PIX_FMT_MJPEG and V4L2_PIX_FMT_YUYV are accepted by unsigned int pixelformat.
    
    struct v4l2_format fmt;
    memset(&fmt, 0, sizeof(fmt));
    fmt.type                = V4L2_BUF_TYPE_VIDEO_CAPTURE;
    fmt.fmt.pix.width       = frame_width;  
    fmt.fmt.pix.height      = frame_height;  
    fmt.fmt.pix.pixelformat = pixelformat;  
    fmt.fmt.pix.field       = V4L2_FIELD_NONE;  
    if(-1 == xioctl(fd, VIDIOC_S_FMT, &fmt)){
        printf("Failed to set format on device (fd=%d).\n", fd);
    }  
 
    printf("Video Format of device (fd=%d) is set to:\n", fd);
    char fmtstr[5];  
    memset(fmtstr, 0, 5);
    memcpy(fmtstr, &fmt.fmt.pix.pixelformat, 4);
    printf("resolution   : %dX%d.\n", frame_width, frame_height);
    printf("pixelformat  : %s\n", fmtstr);  
    printf("\n");
    return 0; 
}

int get_video_format(int fd)
{
    struct v4l2_format fmt;
    fmt.type = V4L2_BUF_TYPE_VIDEO_CAPTURE; // Must set fmt.type before receive format info.
    if (-1 == xioctl(fd, VIDIOC_G_FMT, &fmt)){
        printf("Failed to get video format for device (fd=%d).\n", fd);
        printf("\n");
        return -1;
    }
    
    // Cast unsigned int to char.
    char fmtstr[5];  
    memset(fmtstr, 0, 5);
    memcpy(fmtstr, &fmt.fmt.pix.pixelformat, 4);
    
    printf("Current video format for device (fd=%d) is:\n", fd);
    printf("resolution   : %dX%d\n", fmt.fmt.pix.width, fmt.fmt.pix.height);
    printf("pixelformat  : %s\n", fmtstr);
    // The following shift bits method is equivalent to memcpy to char.
    /*printf("pixelformat = '%c%c%c%c'\n",
        fmt.fmt.pix.pixelformat & 0xFF,
        (fmt.fmt.pix.pixelformat>> 8) & 0xFF,
        (fmt.fmt.pix.pixelformat>>16) & 0xFF,
        (fmt.fmt.pix.pixelformat>>24) & 0xFF);*/
    printf("field        : %d\n", fmt.fmt.pix.field);  
    printf("bytesperline : %d\n", fmt.fmt.pix.bytesperline);  
    printf("sizeimage    : %d\n", fmt.fmt.pix.sizeimage);  
    printf("colorspace   : %d\n", fmt.fmt.pix.colorspace);  
    printf("\n");
}


void enumerate_all_controls(int fd)
{   
    printf("\nEnumerating all controls for device (fd=%d):\n", fd);
    // Clear querymenu variable.
    struct v4l2_queryctrl queryctrl;
    struct v4l2_querymenu querymenu;
    
    memset(&queryctrl, 0, sizeof(queryctrl));
    memset(&querymenu, 0, sizeof(querymenu));
    queryctrl.id = V4L2_CTRL_FLAG_NEXT_CTRL;
    //printf("queryctrl.id = %d\n", queryctrl.id);
    while (0 == ioctl(fd, VIDIOC_QUERYCTRL, &queryctrl)){
        if (!(queryctrl.flags & V4L2_CTRL_FLAG_DISABLED)){
            printf("Control item: %s\n", queryctrl.name);
            // If control ID has a type menu, print this menu.
            if (queryctrl.type == V4L2_CTRL_TYPE_MENU){
                // Clear querymenu variable.
                //memset(&querymenu, 0, sizeof(querymenu));
                querymenu.id = queryctrl.id;
                printf("        menu: \n");
                for (querymenu.index = queryctrl.minimum;
                    querymenu.index <= queryctrl.maximum;
                    querymenu.index++){
                    if (0 == ioctl(fd, VIDIOC_QUERYMENU, &querymenu)){
                        printf("              %d. %s\n", querymenu.index, querymenu.name);
                    }
                }
            }
        }
        //printf("\n");
        // Get next control ID.
        queryctrl.id |= V4L2_CTRL_FLAG_NEXT_CTRL;
        //printf("queryctrl.id = %d\n", queryctrl.id);
    }
    
    if (errno != EINVAL){
        perror("VIDIOC_QUERYCTRL");
        exit(EXIT_FAILURE);
    }
    printf("\n");
}


int get_control_parameter(int fd, int control_ID)
{   
    // Get info of given contro ID, and get current control setting.
    
    int rtv_VIDIOC_QUERYCTRL;
    int rtv_VIDIOC_G_CTRL;
    char type_string[64];
    char flags_string[64];
    char control_ID_string[64];
    struct v4l2_queryctrl queryctrl;
    struct v4l2_control control;
    struct v4l2_querymenu querymenu;
    memset(&queryctrl, 0, sizeof(queryctrl));
    memset(&control, 0, sizeof(control));
    memset(&querymenu, 0, sizeof(querymenu));
    
    //The following control_ID is supported by ELP-USBFHD01M-FV board camera.
    //queryctrl.id = V4L2_CID_BRIGHTNESS;
    //queryctrl.id = V4L2_CID_CONTRAST;
    //queryctrl.id = V4L2_CID_SATURATION;
    //queryctrl.id = V4L2_CID_HUE;
    //queryctrl.id = V4L2_CID_AUTO_WHITE_BALANCE;
    //queryctrl.id = V4L2_CID_GAMMA;
    //queryctrl.id = V4L2_CID_GAIN;
    //queryctrl.id = V4L2_CID_POWER_LINE_FREQUENCY;
    //queryctrl.id = V4L2_CID_WHITE_BALANCE_TEMPERATURE;
    //queryctrl.id = V4L2_CID_SHARPNESS;
    //queryctrl.id = V4L2_CID_BACKLIGHT_COMPENSATION;
    //queryctrl.id = V4L2_CID_EXPOSURE_AUTO;
    //queryctrl.id = V4L2_CID_EXPOSURE_ABSOLUTE;
    //queryctrl.id = V4L2_CID_EXPOSURE_AUTO_PRIORITY;
    
    queryctrl.id = control_ID;
    control.id = control_ID;
    rtv_VIDIOC_QUERYCTRL = xioctl(fd, VIDIOC_QUERYCTRL, &queryctrl);
    rtv_VIDIOC_G_CTRL = xioctl(fd, VIDIOC_G_CTRL, &control);
    
    if(-1 == rtv_VIDIOC_QUERYCTRL){
        printf("Failed to query control parameter for device (fd=%d).\n", fd);
        get_v4l2_control_ID_string(control_ID, control_ID_string);
        printf("control_ID    = %s\n", control_ID_string);
        printf("\n");
        return -1;
    }
    else if(-1 == rtv_VIDIOC_G_CTRL){
        printf("Failed to get control parameter for device (fd=%d).\n", fd);
        get_v4l2_control_ID_string(control_ID, control_ID_string);
        printf("control_ID    = %s\n", control_ID_string);
        printf("\n");
        return -1;
    }
    else{
        printf("Get control parameter for device (fd=%d) successfully.\n", fd);
        get_v4l2_control_ID_string(control_ID, control_ID_string);
        printf("control_ID    = %s\n", control_ID_string);
        printf("name          = %s\n", queryctrl.name);
        printf("minimum       = %d\n", queryctrl.minimum);
        printf("maximum       = %d\n", queryctrl.maximum);
        printf("step          = %d\n", queryctrl.step);
        printf("default_value = %d\n", queryctrl.default_value);
        printf("current_value = %d\n", control.value);
        get_v4l2_ctrl_flags_string(queryctrl.flags, flags_string); // Convert flags to string.
        printf("flags         = %s\n", flags_string);
        get_v4l2_ctrl_type_string(queryctrl.type, type_string); // Convert enum to string.
        printf("type          = %s\n", type_string);
        // If control ID has a type menu, print this menu.
        if (queryctrl.type == V4L2_CTRL_TYPE_MENU){
            // Clear querymenu variable.
            //memset(&querymenu, 0, sizeof(querymenu));
            querymenu.id = queryctrl.id;
            printf("menu: \n");
            for (querymenu.index = queryctrl.minimum;
                querymenu.index <= queryctrl.maximum;
                querymenu.index++){
                if (0 == xioctl(fd, VIDIOC_QUERYMENU, &querymenu)){
                    printf("     %d. %s\n", querymenu.index, querymenu.name);
                }
            }
        }
    }
    
    printf("\n");
    return 0;
}


int set_control_parameter(int fd, int control_ID, int control_value)
{   
    // Set control parameters.
    
    int rtv_VIDIOC_G_CTRL;
    int rtv_VIDIOC_S_CTRL;
    int rtv_VIDIOC_QUERYCTRL;
    char type_string[64];
    char flags_string[64];
    char control_ID_string[64];
    struct v4l2_queryctrl queryctrl;
    struct v4l2_control old_setting;
    struct v4l2_control new_setting;
    struct v4l2_querymenu querymenu;
    memset(&queryctrl, 0, sizeof(queryctrl));
    memset(&old_setting, 0, sizeof(old_setting));
    memset(&new_setting, 0, sizeof(new_setting));
    memset(&querymenu, 0, sizeof(querymenu));
    
    //The following control_ID is supported by ELP-USBFHD01M-FV board camera.
    //queryctrl.id = V4L2_CID_BRIGHTNESS;
    //queryctrl.id = V4L2_CID_CONTRAST;
    //queryctrl.id = V4L2_CID_SATURATION;
    //queryctrl.id = V4L2_CID_HUE;
    //queryctrl.id = V4L2_CID_AUTO_WHITE_BALANCE;
    //queryctrl.id = V4L2_CID_GAMMA;
    //queryctrl.id = V4L2_CID_GAIN;
    //queryctrl.id = V4L2_CID_POWER_LINE_FREQUENCY;
    //queryctrl.id = V4L2_CID_WHITE_BALANCE_TEMPERATURE;
    //queryctrl.id = V4L2_CID_SHARPNESS;
    //queryctrl.id = V4L2_CID_BACKLIGHT_COMPENSATION;
    //queryctrl.id = V4L2_CID_EXPOSURE_AUTO;
    //queryctrl.id = V4L2_CID_EXPOSURE_ABSOLUTE;
    //queryctrl.id = V4L2_CID_EXPOSURE_AUTO_PRIORITY;
    
    queryctrl.id = control_ID;
    old_setting.id = control_ID;
    new_setting.id = control_ID;
    new_setting.value = control_value;
    
    // Query current setting.
    rtv_VIDIOC_QUERYCTRL = xioctl(fd, VIDIOC_QUERYCTRL, &queryctrl);
    rtv_VIDIOC_G_CTRL = xioctl(fd, VIDIOC_G_CTRL, &old_setting);
    
    if(-1 == rtv_VIDIOC_QUERYCTRL){
        printf("Before setting, failed to query control parameter for device (fd=%d).\n", fd);
        get_v4l2_control_ID_string(control_ID, control_ID_string);
        printf("control_ID    = %s\n", control_ID_string);
        printf("\n");
        return -1;
    }
    else if(-1 == rtv_VIDIOC_G_CTRL){
        printf("Before setting, failed to get control parameter for device (fd=%d).\n", fd);
        get_v4l2_control_ID_string(control_ID, control_ID_string);
        printf("control_ID    = %s\n", control_ID_string);
        printf("\n");
        return -1;
    }
    else{
        // Set new_setting value.
        rtv_VIDIOC_S_CTRL = xioctl(fd, VIDIOC_S_CTRL, &new_setting);
        if(-1 == rtv_VIDIOC_S_CTRL){
            printf("Failed to set control parameter for device (fd=%d).\n", fd);
        }
        else{
            printf("Set control parameter for device (fd=%d) successfully.\n", fd);
        }
        // Query new setting.
        rtv_VIDIOC_QUERYCTRL = xioctl(fd, VIDIOC_QUERYCTRL, &queryctrl);
        rtv_VIDIOC_G_CTRL = xioctl(fd, VIDIOC_G_CTRL, &new_setting);
        if(-1 == rtv_VIDIOC_QUERYCTRL){
            printf("After setting, failed to query control parameter for device (fd=%d).\n", fd);
            get_v4l2_control_ID_string(control_ID, control_ID_string);
            printf("control_ID    = %s\n", control_ID_string);
            printf("\n");
            return -1;
        }
        else if(-1 == rtv_VIDIOC_G_CTRL){
            printf("After setting, failed to get control parameter for device (fd=%d).\n", fd);
            get_v4l2_control_ID_string(control_ID, control_ID_string);
            printf("control_ID    = %s\n", control_ID_string);
            printf("\n");
            return -1;
        }
        else{
            get_v4l2_control_ID_string(control_ID, control_ID_string);
            printf("control_ID    = %s\n", control_ID_string);
            printf("name          = %s\n", queryctrl.name);
            printf("minimum       = %d\n", queryctrl.minimum);
            printf("maximum       = %d\n", queryctrl.maximum);
            printf("step          = %d\n", queryctrl.step);
            printf("default_value = %d\n", queryctrl.default_value);
            printf("current_value = %d (old value = %d)\n", new_setting.value, old_setting.value);
            get_v4l2_ctrl_flags_string(queryctrl.flags, flags_string); // Convert flags to string.
            printf("flags         = %s\n", flags_string);
            get_v4l2_ctrl_type_string(queryctrl.type, type_string); // Convert enum to string.
            printf("type          = %s\n", type_string);
            // If control ID has a type menu, print this menu.
            if (queryctrl.type == V4L2_CTRL_TYPE_MENU){
                // Clear querymenu variable.
                //memset(&querymenu, 0, sizeof(querymenu));
                querymenu.id = queryctrl.id;
                printf("menu: \n");
                for (querymenu.index = queryctrl.minimum;
                    querymenu.index <= queryctrl.maximum;
                    querymenu.index++){
                    if (0 == xioctl(fd, VIDIOC_QUERYMENU, &querymenu)){
                        printf("     %d. %s\n", querymenu.index, querymenu.name);
                    }
                }
            }
        }
    }
    printf("\n");
    return 0;
}


int get_supported_frame_size_and_fps(int fd)
{   
    printf("Supported frame size and fps by device (fd=%d):\n", fd);
    struct v4l2_fmtdesc fmtdesc; // Must fill .index and .type before use.
    struct v4l2_frmsizeenum frmsize; // Must fill .index and .pixel_format before use.
    struct v4l2_frmivalenum frmival; // Must fill .index, .pixel_format, .width, and .height before use.
    memset(&fmtdesc, 0, sizeof(fmtdesc));
    memset(&frmsize, 0, sizeof(frmsize));
    memset(&frmival, 0, sizeof(frmival));
    
    fmtdesc.index = 0;
    fmtdesc.type = V4L2_BUF_TYPE_VIDEO_CAPTURE;
    while(0 == xioctl(fd, VIDIOC_ENUM_FMT, &fmtdesc)){
        /* 
        // Cast unsigned int to char. Equivalent to bit shift.
        char fmtstr[5];  
        memset(fmtstr, 0, 5);
        memcpy(fmtstr, &fmtdesc.pixelformat, 4);
        fmtstr[4] = '\0';
        printf("Pixel Format: %s\n", fmtstr);
        */
        
        printf("Pixel Format : '%c%c%c%c'\n",
        fmtdesc.pixelformat & 0xFF,
        (fmtdesc.pixelformat>> 8) & 0xFF,
        (fmtdesc.pixelformat>>16) & 0xFF,
        (fmtdesc.pixelformat>>24) & 0xFF);
        
        frmsize.index = 0;
        frmsize.pixel_format = fmtdesc.pixelformat;
        while((0 == xioctl(fd, VIDIOC_ENUM_FRAMESIZES, &frmsize))){
            if(frmsize.type == V4L2_FRMSIZE_TYPE_DISCRETE){
                //printf("Frame size type is discrete.\n");
                printf("    %-4dx%4d",frmsize.discrete.width, frmsize.discrete.height);
                
                // Fill frmival to check fps.
                frmival.index = 0;
                frmival.pixel_format = fmtdesc.pixelformat;
                frmival.width = frmsize.discrete.width;
                frmival.height = frmsize.discrete.height;
                while(0 == xioctl(fd, VIDIOC_ENUM_FRAMEINTERVALS, &frmival)){
                    //printf("denominator = %d\n", frmival.discrete.denominator);
                    //printf("numerator = %d\n", frmival.discrete.numerator);
                    printf(" (%3d fps)\n", frmival.discrete.denominator/frmival.discrete.numerator);
                    frmival.index++; // Get next fps.
                }
            }
            else if(frmsize.type == V4L2_FRMSIZE_TYPE_STEPWISE){
                printf("Frame size type is stepwise.\n");
                printf("%dx%d ",frmsize.stepwise.min_width, frmsize.stepwise.min_height);
                printf("min_width = %d\n", frmsize.stepwise.min_width);
                printf("max_width = %d\n", frmsize.stepwise.max_width);
                printf("step_width = %d\n", frmsize.stepwise.step_width);
                printf("min_height = %d\n", frmsize.stepwise.min_height);
                printf("max_height = %d\n", frmsize.stepwise.max_height);
                printf("step_height = %d\n", frmsize.stepwise.step_height);
            }
            frmsize.index++; // Get next frame size.
        }
        fmtdesc.index++; // Get next video format.
        //printf("\n");
    }
    printf("\n");
    return 0;
}

    //The following control_ID is supported by ELP-USBFHD01M-FV board camera.
    //queryctrl.id = V4L2_CID_BRIGHTNESS;
    //queryctrl.id = V4L2_CID_CONTRAST;
    //queryctrl.id = V4L2_CID_SATURATION;
    //queryctrl.id = V4L2_CID_HUE;
    //queryctrl.id = V4L2_CID_AUTO_WHITE_BALANCE;
    //queryctrl.id = V4L2_CID_GAMMA;
    //queryctrl.id = V4L2_CID_GAIN;
    //queryctrl.id = V4L2_CID_POWER_LINE_FREQUENCY;
    //queryctrl.id = V4L2_CID_WHITE_BALANCE_TEMPERATURE;
    //queryctrl.id = V4L2_CID_SHARPNESS;
    //queryctrl.id = V4L2_CID_BACKLIGHT_COMPENSATION;
    //queryctrl.id = V4L2_CID_EXPOSURE_AUTO;
    //queryctrl.id = V4L2_CID_EXPOSURE_ABSOLUTE;
    //queryctrl.id = V4L2_CID_EXPOSURE_AUTO_PRIORITY;
    
int main(){

    printf("\n");
    
    char *cameraL = "/dev/video0";
    char *cameraR = "/dev/video1";
    int fd_cameraL;
    int fd_cameraR;
    int int_temp;
    
    fd_cameraL = open_device(cameraL, true);
    fd_cameraR = open_device(cameraR, true);
    
    //get_supported_format(fd_cameraL);
    
    //get_video_format(fd_cameraL);
    //get_video_format(fd_cameraR);
    
    int width = 640;
    int height = 480;
    
    set_video_format(fd_cameraL, width, height, V4L2_PIX_FMT_MJPEG);//V4L2_PIX_FMT_MJPEG or V4L2_PIX_FMT_YUYV.
    set_video_format(fd_cameraR, width, height, V4L2_PIX_FMT_MJPEG);//V4L2_PIX_FMT_MJPEG or V4L2_PIX_FMT_YUYV.
    
    get_video_format(fd_cameraL);
    get_video_format(fd_cameraR);
    
    enumerate_all_controls(fd_cameraR);
    

    //get_control_parameter(fd_cameraL, V4L2_CID_BRIGHTNESS);
    //get_control_parameter(fd_cameraL, V4L2_CID_CONTRAST);
    //get_control_parameter(fd_cameraL, V4L2_CID_SATURATION);
    //get_control_parameter(fd_cameraL, V4L2_CID_HUE);
    //get_control_parameter(fd_cameraL, V4L2_CID_AUTO_WHITE_BALANCE);
    //get_control_parameter(fd_cameraL, V4L2_CID_GAMMA);
    //get_control_parameter(fd_cameraL, V4L2_CID_GAIN);
    //get_control_parameter(fd_cameraL, V4L2_CID_POWER_LINE_FREQUENCY);
    get_control_parameter(fd_cameraL, V4L2_CID_WHITE_BALANCE_TEMPERATURE);
    //get_control_parameter(fd_cameraL, V4L2_CID_SHARPNESS);
    //get_control_parameter(fd_cameraL, V4L2_CID_BACKLIGHT_COMPENSATION);
    //get_control_parameter(fd_cameraL, V4L2_CID_EXPOSURE_AUTO);
    //get_control_parameter(fd_cameraL, V4L2_CID_EXPOSURE_ABSOLUTE);
    //get_control_parameter(fd_cameraL, V4L2_CID_EXPOSURE_AUTO_PRIORITY);
   
    
    //get_control_parameter(fd_cameraL, V4L2_CID_EXPOSURE_AUTO);
    set_control_parameter(fd_cameraL, V4L2_CID_EXPOSURE_AUTO, 1);
    set_control_parameter(fd_cameraL, V4L2_CID_EXPOSURE_ABSOLUTE, 200);
    set_control_parameter(fd_cameraR, V4L2_CID_EXPOSURE_AUTO, 1);
    set_control_parameter(fd_cameraR, V4L2_CID_EXPOSURE_ABSOLUTE, 200);
    
    //get_supported_frame_size_and_fps(fd_cameraL);
    //get_supported_frame_size_and_fps(fd_cameraR);

    
    struct v4l2_cropcap cropcap;
    memset (&cropcap, 0, sizeof (cropcap));
    cropcap.type = V4L2_BUF_TYPE_VIDEO_CAPTURE;

    if (-1 == xioctl (fd_cameraL, VIDIOC_CROPCAP, &cropcap)) {
        perror ("VIDIOC_CROPCAP");
        exit (EXIT_FAILURE);
    }
    
    printf("cropcap.type = %d\n\n", cropcap.type);
    
    printf("cropcap.bounds.left = %d\n", cropcap.bounds.left);
    printf("cropcap.bounds.top = %d\n", cropcap.bounds.top);
    printf("cropcap.bounds.width = %d\n", cropcap.bounds.width);
    printf("cropcap.bounds.height = %d\n\n", cropcap.bounds.height);
    
    printf("cropcap.defrect.left = %d\n", cropcap.defrect.left);
    printf("cropcap.defrect.top = %d\n", cropcap.defrect.top);
    printf("cropcap.defrect.width = %d\n", cropcap.defrect.width);
    printf("cropcap.defrect.height = %d\n\n", cropcap.defrect.height);
    
    printf("cropcap.pixelaspect.numerator = %d\n", cropcap.pixelaspect.numerator);
    printf("cropcap.pixelaspect.denominator = %d\n\n", cropcap.pixelaspect.denominator);
    
    
    struct v4l2_crop crop;
    memset (&crop, 0, sizeof (crop));
    crop.type = V4L2_BUF_TYPE_VIDEO_CAPTURE;
    crop.c = cropcap.defrect;
    
    printf("crop.c.left = %d\n", crop.c.left);
    printf("crop.c.top = %d\n", crop.c.top);
    printf("crop.c.width = %d\n", crop.c.width);
    printf("crop.c.height = %d\n\n", crop.c.height);

    /* Ignore if cropping is not supported (EINVAL). */
    if (-1 == xioctl(fd_cameraL, VIDIOC_G_CROP, &crop)
        && errno != EINVAL) {
        perror ("VIDIOC_S_CROP");
        exit (EXIT_FAILURE);
    }
    
    printf("crop.type = %d\n\n", crop.type);
    
    printf("crop.c.left = %d\n", crop.c.left);
    printf("crop.c.top = %d\n", crop.c.top);
    printf("crop.c.width = %d\n", crop.c.width);
    printf("crop.c.height = %d\n\n", crop.c.height);
    
    /*
    crop.c.left = 0;
    crop.c.top = 0;
    crop.c.width = 640;
    crop.c.height = 480;
    */
    
    
    memset (&crop, 0, sizeof (crop));
    crop.type = V4L2_BUF_TYPE_VIDEO_CAPTURE;
    crop.c = cropcap.defrect;
    
    /* Ignore if cropping is not supported (EINVAL). */
    if (-1 == xioctl(fd_cameraL, VIDIOC_S_CROP, &crop)
        && errno != EINVAL) {
        perror ("VIDIOC_S_CROP");
        exit (EXIT_FAILURE);
    }
    
    printf("crop.type = %d\n\n", crop.type);
    
    printf("crop.c.left = %d\n", crop.c.left);
    printf("crop.c.top = %d\n", crop.c.top);
    printf("crop.c.width = %d\n", crop.c.width);
    printf("crop.c.height = %d\n\n", crop.c.height);


    close_device(fd_cameraL);
    close_device(fd_cameraR);
    
    return 0;

}



































