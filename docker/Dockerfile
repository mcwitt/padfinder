FROM amazonlinux:latest
MAINTAINER Matt Wittmann <mcwitt@gmail.com>

RUN yum install -y \
        gcc \
        git \
        openssl-devel \
        python36 \
        python36-devel \
        python36-pip

RUN mkdir -p /usr/local/bin && ln -s /usr/bin/python3 /usr/local/bin/python
RUN pip-3.6 install --upgrade pip

COPY etc/init.d/ /etc/init.d/
COPY etc/profile.d/ /etc/profile.d/

WORKDIR /code
RUN git clone https://github.com/mcwitt/padfinder.git
COPY padfinder/ /code/padfinder/

WORKDIR /code/padfinder/
RUN git checkout tags/v0.3.2
RUN pip install -r requirements.txt

# needed for click to work
ENV LANG en_US.utf-8
ENV LC_ALL en_US.utf-8

WORKDIR /code/padfinder/padfinder
ENTRYPOINT ["./start.sh"]
CMD ["sfbay", "sfc"]
