FROM tiangolo/uwsgi-nginx-flask:python3.7

RUN pip install \
  pytest \
  sphinx \
  requests \
  beautifulsoup4

ENV FLASK_APP="geclass"
ENV STATIC_PATH="/app/geclass/static"
