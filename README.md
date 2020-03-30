# Google-Map-Downloader
![Google-Map-Downloader](https://geospatialmedia.s3.amazonaws.com/wp-content/uploads/2016/07/google-earth.jpg)
## 中文：  
[Downloader_1.1](https://github.com/zhengjie9510/Google-Map-Downloader/blob/master/Downloader_1.1.py)：  
    一个小工具，你只需要输入空间范围、地图缩放等级就可以实现Google地图的下载，并输出为TIFF格式，含空间坐标系。  
[Downloader_1.2](https://github.com/zhengjie9510/Google-Map-Downloader/blob/master/Downloader_1.2.py)：  
    是在1.1版本上的改进。由于python的多线程中存在GIL锁，导致python的多线程不能利用多核，考虑到现在的计算机是多核的，为了充分利用计算机的多核资源，提高下载速度，尝试利用多进程+多线程的方式来实现地图切片下载，最终速度得到极大提高。但该部分还没有实现进度条功能。  
## English:  
[Downloader_1.1](https://github.com/zhengjie9510/Google-Map-Downloader/blob/master/Downloader_1.1.py):  
    A small tool, you only need to input the spatial extent and map zoom level to download Google Maps, and output to TIFF format, including the spatial coordinate system.  
[Downloader_1.2](https://github.com/zhengjie9510/Google-Map-Downloader/blob/master/Downloader_1.2.py):  
    It is an improvement on version 1.1. Due to the existence of GIL locks in python's multi-threading, python's multi-threading cannot use multi-cores. Considering that computers are now multi-core, In order to make full use of the computer's multi-core resources and increase the download speed, try to use multi-process + multi-threaded way to achieve map tile download. The final speed has been greatly improved, but this part has not implemented the progress bar function.