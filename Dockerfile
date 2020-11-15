FROM ecoron/python36-sklearn
FROM ubuntu:14.04
MAINTAINER ecoron

ENV DEBIAN_FRONTEND noninteractive

RUN apt-get update
RUN apt-get install -y curl -o APT::Immediate-Configure=0
RUN apt-get -y install git wget curl sudo
RUN apt-get -y autoremove
RUN apt-get -y autoclean
RUN apt-get install -y \
    php5-mcrypt \
    python-pip
RUN apt-get -y install python-dev
RUN python -m pip install openpyxl==2.6.4
RUN python -m pip install soupsieve==1.2.0
RUN apt-get -y install g++ gcc libxslt-dev libtool libmagic-dev

RUN mkdir serpscrap
COPY install_chrome.sh .install_chrome.sh
RUN sh .install_chrome.sh

RUN pip install SerpScrap==0.13.0

# ENTRYPOINT python
