FROM python:latest

RUN apt-get update
RUN apt-get install -y supervisor
RUN service supervisor stop

ADD server/ /data
ADD deploy/supervisor.conf /etc/supervisor.conf

RUN pip install -r /data/requirements.txt
RUN pip install gunicorn

EXPOSE 5000

CMD supervisord -c /etc/supervisor.conf -n
