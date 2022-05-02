FROM ubuntu:20.04
MAINTAINER  Prabu "<prabum1985@gmail.com>"
ENV TZ=America/Los_Angeles

COPY requirements.txt .
ENV FLASK_APP=app.py
ENV FLASK_ENV=development

RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone
RUN apt-get update -y
RUN apt-get install libzbar0 -y
RUN apt-get install -y python3-pip python3-dev build-essential
RUN apt update && apt install -y libsm6 libxext6
RUN apt-get -y install libmysqlclient-dev
RUN apt-get -y install gcc
RUN apt install -y git
RUN apt install -y cmake
RUN pip3 install -r requirements.txt
COPY .env .env
COPY . /app
WORKDIR /app
RUN pip install python-dotenv

RUN pip3 install requests
RUN pip3 install Flask-Session
RUN pip3 install flask flask-jsonpify flask-sqlalchemy flask-restful
RUN pip3 freeze
RUN pip3 install mysqlclient

EXPOSE 9000
HEALTHCHECK --interval=30s --timeout=30s --start-period=30s --retries=5 \
    CMD curl -f http://localhost/health || exit 1
ENTRYPOINT ["python3", "app.py"]