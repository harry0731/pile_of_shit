#!/bin/bash

sudo apt-get -y update
sudo apt-get -y upgrade
sudo apt-get -y dist-upgrade
sudo apt-get -y autoremove

# OpenCV
sudo apt-get install -y build-essential cmake

sudo apt-get install -y qt5-default libvtk6-dev

sudo apt-get install -y zlib1g-dev libjpeg-dev libwebp-dev libpng-dev libtiff5-dev libjasper-dev libopenexr-dev libgdal-dev

sudo apt-get install -y libdc1394-22-dev libavcodec-dev libavformat-dev libswscale-dev libtheora-dev libvorbis-dev libxvidcore-dev libx264-dev yasm libopencore-amrnb-dev libopencore-amrwb-dev libv4l-dev libxine2-dev

sudo apt-get install -y libtbb-dev libeigen3-dev

sudo apt-get install -y python-dev python-tk python-pip python-numpy python3-dev python3-tk python3-numpy

sudo apt-get install -y ant default-jdk

sudo apt-get install -y doxygen

sudo apt-get install -y unzip wget
wget https://github.com/opencv/opencv/archive/3.2.0.zip
unzip 3.2.0.zip
rm 3.2.0.zip
mv opencv-3.2.0 OpenCV
cd OpenCV
mkdir build
cd build
cmake -DWITH_QT=ON -DWITH_OPENGL=ON -DFORCE_VTK=ON -DWITH_TBB=ON -DWITH_GDAL=ON -DWITH_XINE=ON -DBUILD_EXAMPLES=ON -DENABLE_PRECOMPILED_HEADERS=OFF ..
make -j4
sudo make install
sudo ldconfig

# PtQt4
sudo apt-get install python-qt4 -y
sudo apt-get install python-pip python-dev libmysqlclient-dev -y
sudo pip install MySQL-python
sudo apt-get install python-qt4-sql -y
sudo apt-get install libqt4-sql-mysql -y 

# Face Recognition
sudo apt-get install libboost-all-dev -y
sudo pip install dlib
sudo pip install scipy
sudo pip install numpy
sudo pip install Pillow
sudo pip install Click
sudo pip install face_recognition_models

# RS232
sudo apt-get install python-serial -y
