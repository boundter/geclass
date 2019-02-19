FROM tiangolo/uwsgi-nginx-flask:python3.7

RUN pip install pytest

ENTRYPOINT []

CMD ["pytest"]
