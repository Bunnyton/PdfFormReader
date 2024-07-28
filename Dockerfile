FROM python:3.9

RUN mkdir -p /usr/src/
#COPY . /usr/src/
WORKDIR /usr/src/

RUN python -m pip install --upgrade pip
RUN pip3 install --no-cache-dir -r requirments.txt