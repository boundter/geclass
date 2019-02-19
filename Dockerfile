FROM tiangolo/uwsgi-nginx-flask:python3.7

RUN pip install pytest

ENV FLASK_APP portal
ENV PYTHONPATH "/app:${PYTHONPATH}"

ENTRYPOINT []

CMD ["pytest"]
