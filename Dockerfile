# The base image to start from. A image hash can be used here to pick some
# intermediate image.
FROM ubuntu:xenial
#FROM a2799408863


RUN apt-get update && apt-get install -y \
    autoconf automake libtool libleptonica-dev libicu-dev libpango1.0-dev libcairo2-dev cmake git libgtk2.0-dev pkg-config libavcodec-dev libavformat-dev libswscale-dev python-dev python-numpy libjpeg-dev libpng-dev libtiff-dev libjasper-dev libdc1394-22-dev virtualenvwrapper liblog4cplus-dev libcurl4-openssl-dev libtiff5-dev gcc make ca-certificates autoconf-archive libgstreamer1.0-dev libgstreamer-plugins-base1.0-dev \
    wget unzip python3-pip python3-mysql.connector libtesseract3 #libopencv-dev
RUN apt-get install -y openjdk-8-jdk default-jdk
RUN apt-get install -y libgtk-3-dev libv4l-dev
#RUN cd /usr/include/linux && ln -s ../libv4l1-videodev.h videodev.h

# Download the leptonica if not already present.
RUN test -f /tmp/leptonica-1.76.0.tar.gz || wget http://www.leptonica.org/source/leptonica-1.76.0.tar.gz -O /tmp/leptonica-1.76.0.tar.gz

RUN cd /tmp/ && tar xvf leptonica-1.76.0.tar.gz --no-same-owner && cd leptonica-1.76.0 && \
    ./configure && \
    make -j2 && \
    make install

#RUN cd /usr/src && git clone https://github.com/tesseract-ocr/tesseract.git && \
#    cd tesseract && git checkout 3.04.01 && ./autogen.sh && ./configure --enable-debug && make -j2 && make install && ldconfig

#RUN wget https://github.com/opencv/opencv/archive/4.2.0.zip -O /tmp/OpenCV-4.2.0.zip && cd /usr/src/ && unzip -q /tmp/OpenCV-4.2.0.zip && \
#    cd opencv-4.2.0 && mkdir build && cd build \
#    cmake -D CMAKE_BUILD_TYPE=RELEASE -D CMAKE_INSTALL_PREFIX=/usr/local -D ENABLE_PRECOMPILED_HEADERS=OFF .. && \
#    make -j2 && make install

#RUN git clone https://github.com/openalpr/openalpr.git /usr/src/openalpr && mkdir /usr/src/openalpr/build && cd /usr/src/openalpr/build && \
#    cmake -D CMAKE_INSTALL_PREFIX:PATH=/usr -D CMAKE_INSTALL_SYSCONFDIR:PATH=/etc ../src && \
#    make -j2 &&  make install && ldconfig

RUN pip3 install --upgrade pip && pip3 install opencv-python

CMD ["/usr/bin/python3", "/tmp/code/lpnr.py"]
