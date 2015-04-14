FROM python:latest

ADD server/ /data
ADD deploy/supervisor.conf /etc/supervisor.conf

RUN pip install supervisor --pre
RUN pip install gunicorn
RUN pip install -r /data/requirements.txt
RUN pybabel compile -d /data/translations

EXPOSE 5000

CMD supervisord -c /etc/supervisor.conf -n
