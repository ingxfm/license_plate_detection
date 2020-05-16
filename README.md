# license-plate-detection-raspberry-pi-3B-plus-OpenAlpr
The aim is to make the code do the following: 
- Function 1: Take images from the live video feed. The live video feed comes from the localhost using the Motion project (https://motion-project.github.io/). 
- Function 2: When the PIR motion sensor senses movement, an image from the live video feed in Function 1 is sent to function 2. Function 2 calls the license plate detection on Function 3. 
- Function 3: This calls OpenAlpr to detect if there is a license plate in the image from Function 2. If there is a license plate the information is saved into a MariaDB local database.

Dependency installation process for Raspberry Pi 3B with Buster

For this installation tutorial, it is assumed that the Raspbian is install in the Raspberry Pi 3B.

Installation (Vinczejanos, 2017) (MMattiii, 2019)

In case, the memory is limited in the Raspberry Pi, run the following commands to uninstall LibreOffice and Wolfram which will not be used.

sudo apt-get purge wolfram-engine libreoffice* scratch -y
sudo apt-get clean & autoremove

First of all you should update your Pi with the following two commands:

sudo apt-get update
sudo apt-get upgrade
The next command installs all packages needed for all the other steps:
sudo apt-get install autoconf automake libtool libleptonica-dev libicu-dev libpango1.0-dev libcairo2-dev cmake git libgtk2.0-dev pkg-config libavcodec-dev libavformat-dev libswscale-dev python-dev python-numpy libjpeg-dev libpng-dev libtiff-dev libjasper-dev libdc1394-22-dev virtualenvwrapper liblog4cplus-dev libcurl4-openssl-dev libtiff5-dev gcc make ca-certificates autoconf-archive libgstreamer1.0-dev libgstreamer-plugins-base1.0-dev

Then:
sudo apt-get install -y openjdk-8-jdk
sudo apt-get install -y default-jdk
export JAVA_HOME=/usr/lib/jvm/java-8-openjdk-amd64

Then:
sudo apt install libgtk-3-dev

Then:
sudo apt-get install libv4l-dev
cd /usr/include/linux
sudo ln -s ../libv4l1-videodev.h videodev.h

Or:
sudo apt-get install libv4l-dev
cd /usr/include/linux
sudo mv videodev.h. videodev.h
In some cases, the package can throw errors, in such a case run separately the command:
sudo apt-get install libpng12-dev

The following commands will download, make and install Leptonica. Leptonica is one of the dependencies of OpenALPR.
The making process takes some time. To speed things a little up the -j2 is added.

cd /usr/src
sudo wget http://www.leptonica.org/source/leptonica-1.76.0.tar.gz
sudo tar xf leptonica-1.76.0.tar.gz
cd leptonica-1.76.0
sudo ./configure
sudo make -j2
sudo make install

The next dependency is Tesseract. Again, -j2 speeds up the making.

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

To test if it Tesseract was installed correctly, type the following command. This will output the installed version.
tesseract -v
