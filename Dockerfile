FROM tiangolo/uwsgi-nginx-flask:python3.7

RUN apt update && apt -y install cron

RUN pip install \
  pytest \
  sphinx \
  requests \
  beautifulsoup4 \
  numpy \
  pandas

ENV FLASK_APP="geclass"
ENV STATIC_PATH="/app/geclass/static"

RUN rm /app/main.py
RUN rm /app/prestart.sh

COPY reminder_cron /etc/cron.d/
RUN chmod 0644 /etc/cron.d/reminder_cron
RUN crontab /etc/cron.d/reminder_cron
RUN touch /var/log/cron.log

COPY uwsgi.ini .
COPY geclass geclass
COPY scripts scripts
COPY tests tests
