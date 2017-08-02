FROM python:3.5
ENV PYTHONUNBUFFERED 1
ENV DEBIAN_FRONTEND noninteractive

ENV BASE_DIR /usr/src/app

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        postgresql-client binutils build-essential \
        python3-dev python3-setuptools python3-pip && \
    apt-get clean && apt-get --purge autoremove -y && rm -rf /var/lib/apt/lists/*

WORKDIR $BASE_DIR/
RUN mkdir $BASE_DIR/logs/

COPY requirements.txt /root/requirements.txt

RUN pip3 install -r /root/requirements.txt
