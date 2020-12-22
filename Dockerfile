FROM ubuntu:20.04

WORKDIR /usr/src/app
RUN chmod 777 /usr/src/app
RUN apt-get -qq update && \
    DEBIAN_FRONTEND="noninteractive" apt-get -qq install -y  python3 python3-pip 
RUN apt-get -qq update && \
    DEBIAN_FRONTEND="noninteractive" apt-get -qq install -y  locales
RUN locale-gen en_US.UTF-8
ENV LANG en_US.UTF-8
ENV LANGUAGE en_US:en
ENV LC_ALL en_US.UTF-8
COPY requirements.txt .
RUN pip3 install -r requirements.txt
COPY ./build/aes.py ../../local/lib/python3.8/dist-packages/telethon/crypto/aes.py
RUN mkdir ./uploads
COPY bot.session hello.py downloader.py drive_upload.py service.json  ./



CMD ["python3","hello.py"]