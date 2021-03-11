FROM ubuntu:bionic
EXPOSE 80

RUN apt-get update --fix-missing
RUN apt install -y python3.7 python3-pip nginx uwsgi vim

ENV PYTHONUNBUFFERED 1

COPY ./requirements.txt /requirements.txt
RUN pip3 install -r /requirements.txt



COPY ./mysite_nginx.conf /etc/nginx/sites-available/mysite_nginx.conf

WORKDIR /etc/nginx/sites-enabled

RUN ln -s ../sites-available/mysite_nginx.conf
RUN rm default

RUN pwd

RUN mkdir /src
WORKDIR /src
COPY ./start.sh /start.sh
COPY ./src .

# RUN /etc/init.d/nginx restart

# RUN uwsgi --socket src.sock --module SababaBeach.wsgi --chmod-socket=666