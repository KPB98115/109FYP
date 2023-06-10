FROM python:3.10.3-slim-bullseye

RUN apt-get -y update
RUN apt-get install -y --fix-missing \
    build-essential \
    cmake \
    gfortran \
    git \
    wget \
    curl \
    graphicsmagick \
    libgraphicsmagick1-dev \
    libatlas-base-dev \
    libavcodec-dev \
    libavformat-dev \
    libgtk2.0-dev \
    libjpeg-dev \
    liblapack-dev \
    libswscale-dev \
    pkg-config \
    python3-dev \
    python3-numpy \
    software-properties-common \
    zip \
    && apt-get clean && rm -rf /tmp/* /var/tmp/*

RUN cd ~ && \
    mkdir -p dlib && \
    git clone -b 'v19.9' --single-branch https://github.com/davisking/dlib.git dlib/ && \
    cd dlib/ && \
    python3 setup.py install --yes USE_AVX_INSTRUCTIONS

COPY . /root
RUN cd /root && \
    pip3 install -r requirements.txt
RUN cd ~ && \
    cd dlib && \
    python3 setup.py install

COPY . .

WORKDIR /

CMD [ "python3", "-u", "api.py" ]

# Execute this cmd in terminal to build image with a tag:
# [    docker build -t [tag name of the image] .    ]
# Enter this cmd to construct container.
# [    docker run -p [5001:5000] flask_app    ]
# The cmd above will start the container on vm port: 5000, and mapping to device port: 5001
# The API URL would be "http://localhost:5001"
