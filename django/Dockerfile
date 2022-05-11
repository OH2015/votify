FROM python:3
ENV PYTHONUNBUFFERED 1
WORKDIR /app
RUN mkdir WORKDIR
ADD requirements.txt .
ADD . .
RUN /usr/local/bin/python -m pip install --upgrade pip && pip install -r requirements.txt

