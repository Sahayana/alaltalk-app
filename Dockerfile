FROM python:3.8.10
MAINTAINER GEUMSEONG YANG <didrmatjd@gmail.com>

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Working Directory
WORKDIR /app
COPY . /app/

# Dependency
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

ADD https://raw.githubusercontent.com/vishnubob/wait-for-it/master/wait-for-it.sh /
RUN chmod +x /wait-for-it.sh