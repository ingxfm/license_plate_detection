**License plate number recognition using Raspberry-Pi 3B plus OpenAlpr**

The aim is to make the code do the following: 

- Function 1: Take images from the live video feed. The live video feed comes from the localhost using the Motion project (https://motion-project.github.io/). 
- Function 2: An image from the live video feed in Function 1 is sent to function 2. Function 2 calls the license plate detection on Function 3. 
- Function 3: This calls OpenAlpr to detect if there is a license plate in the image from Function 2. If there is a license plate the information is saved into a MariaDB local database.

**Dependency installation process for Raspberry Pi 3B with Buster**

For this installation tutorial, it is assumed that the Raspbian is install in the Raspberry Pi 3B.

**Installation, credits to: ([Vinczejanos, 2017](https://blog.vinczejanos.info/2017/05/01/install-openalpr-on-raspberry-pi-3-part-2/)) ([MMattiii, 2019](https://www.reddit.com/r/raspberry_pi/comments/baxwz5/how_to_install_openalpr_on_raspberry_pi/))**

In case, the memory is limited in the Raspberry Pi, run the following commands to uninstall LibreOffice and Wolfram which will not be used.
```
sudo apt-get purge wolfram-engine libreoffice* scratch -y
sudo apt-get clean & autoremove
```
Update your Pi with the following two commands:
```
sudo apt-get update
sudo apt-get upgrade
```
The next command installs packages needed for all the other steps:
```
sudo apt-get install autoconf automake libtool libleptonica-dev libicu-dev libpango1.0-dev libcairo2-dev cmake git libgtk2.0-dev pkg-config libavcodec-dev libavformat-dev libswscale-dev python-dev python-numpy libjpeg-dev libpng-dev libtiff-dev libjasper-dev libdc1394-22-dev virtualenvwrapper liblog4cplus-dev libcurl4-openssl-dev libtiff5-dev gcc make ca-certificates autoconf-archive libgstreamer1.0-dev libgstreamer-plugins-base1.0-dev
```
In some cases, the command above can throw errors in libpng12-dev, in such a case run separately the command:
sudo apt-get install libpng12-dev

Then:
```
sudo apt-get install -y openjdk-8-jdk
sudo apt-get install -y default-jdk
export JAVA_HOME=/usr/lib/jvm/java-8-openjdk-amd64
```
Then:
```
sudo apt install libgtk-3-dev
```
Then:
```
sudo apt-get install libv4l-dev
cd /usr/include/linux
sudo ln -s ../libv4l1-videodev.h videodev.h
```
Or:
```
sudo apt-get install libv4l-dev
cd /usr/include/linux
sudo mv videodev.h. videodev.h
```
The following commands will download, make and install Leptonica. Leptonica is one of the dependencies of OpenALPR.
The making process takes some time. To speed things a little up the -j2 is added.
```
cd /usr/src
sudo wget http://www.leptonica.org/source/leptonica-1.76.0.tar.gz
sudo tar xf leptonica-1.76.0.tar.gz
cd leptonica-1.76.0
sudo ./configure
sudo make -j2
sudo make install
```
The next dependency is Tesseract. Again, -j2 speeds up the making.
```
cd /usr/src
sudo git clone https://github.com/tesseract-ocr/tesseract.git
cd tesseract
sudo git tag
sudo git checkout 3.04.01
sudo ./autogen.sh
sudo ./configure --enable-debug
sudo make -j2
sudo make install
sudo ldconfig
```
To test if it Tesseract was installed correctly, type the following command. This will output the installed version.
```
tesseract -v
```
The last dependency is OpenCV. It may stop during the installation process.
```
cd /usr/src
sudo wget https://github.com/opencv/opencv/archive/4.2.0.zip
sudo mv 4.2.0.zip OpenCV-4.2.0.zip
sudo unzip -q OpenCV-4.2.0.zip
cd opencv-4.2.0
sudo mkdir release
cd cmake
cd release
sudo cmake -D CMAKE_BUILD_TYPE=RELEASE -D CMAKE_INSTALL_PREFIX=/usr/local -D ENABLE_PRECOMPILED_HEADERS=OFF ..
sudo make -j2
sudo make install
```
After installing all dependencies, you can finally install OpenALPR itself:
```
cd /usr/src
sudo git clone https://github.com/openalpr/openalpr.git
cd openalpr/src
sudo mkdir build
cd build
sudo cmake -D CMAKE_INSTALL_PREFIX:PATH=/usr -D CMAKE_INSTALL_SYSCONFDIR:PATH=/etc ..
sudo make -j2
sudo make install
sudo ldconfig
```
To test if OpenALPR is working, you can download one of their licence plate pictures and run the licence plate recognition command:
```
cd ~
wget http://plates.openalpr.com/h786poj.jpg -O lp.jpg
alpr lp.jpg
```
Note: In case, you had installed the OpenCV-2.4.13, like in other tutorials, modifications need to be made for installing OpenCV after unzipping the OpenCV-2.4.13 folder:
```
sudo nano OpenCVDetectCXXCompiler.cmake
```
Then, add the following code into the file before the first “if (NOT...”. This means, when you find that if NOT, just before it, press return to give some spaces to the following code, then copy and paste:
```
#dumpversion prints only major version since gcc7
  if((NOT CMAKE_GCC_REGEX_VERSION) AND (${CMAKE_OPENCV_GCC_VERSION_FULL} GREATER 6))
    execute_process(COMMAND ${CMAKE_CXX_COMPILER} ${CMAKE_CXX_COMPILER_ARG1} -dumpfullversion
                  OUTPUT_VARIABLE CMAKE_OPENCV_GCC_VERSION_FULL
                  OUTPUT_STRIP_TRAILING_WHITESPACE)
    string(REGEX MATCH "[0-9]+\\.[0-9]+\\.[0-9]+" CMAKE_GCC_REGEX_VERSION "${CMAKE_OPENCV_GCC_VERSION_FULL}")
  endif()
```
Then:
```
Ctrl+X in nano and press Enter to save the changes.
cd ..
```
**Set cron job to clean /var/lib/motion files**
In this example we will use the motion detection built in the Motion-project software. Every time a motion is detected, Motion will capture a .jpg and save it in /var/lib/motion. When the file is created, this event will trigger the Python license plate number detection script. After a while this folder may be full. We will set a cron job to clean the folder every hour.

For that purpose, go the terminal and type
```
crontab -e
```
Use your preferred editor (nano, vim, etc). We used nano to add the following command to crontab. This includes the ./path_to_our_cleaning_script.sh.
```
0 * * * * ./path_to_our_cleaning_script.sh
```
This script includes commands to clear to directory of .jpg files every 0 minute of every hour, every day of every month.
