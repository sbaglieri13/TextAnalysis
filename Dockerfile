FROM python:3
ENV PYTHONUNBUFFERED=1
WORKDIR /code
COPY requirements.txt /code/
RUN apt-get update
RUN apt-get install -qq python python-dev build-essential swig git libpulse-dev libasound2-dev
RUN pip install --upgrade pocketsphinx
RUN pip install -r requirements.txt
COPY . /code/