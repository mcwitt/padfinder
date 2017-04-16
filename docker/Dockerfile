FROM amazonlinux:latest
MAINTAINER Matt Wittmann <mcwitt@gmail.com>

RUN yum install -y \
        gcc \
        git \
        openssl-devel \
        python35 \
        python35-devel \
        python35-pip

RUN mkdir -p /usr/local/bin && ln -s /usr/bin/python3 /usr/local/bin/python
ENV PATH /usr/local/bin:$PATH

RUN pip-3.5 install --upgrade pip

COPY padfinder /etc/init.d/

WORKDIR /code
RUN git clone https://github.com/mcwitt/padfinder.git

WORKDIR /code/padfinder/
COPY requirements.txt ./
RUN pip install -r requirements.txt

WORKDIR /code/padfinder/padfinder
COPY run.sh secret.py settings.py ./

# needed for click to work
ENV LANG en_US.utf-8
ENV LC_ALL en_US.utf-8

