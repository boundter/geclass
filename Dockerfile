FROM tiangolo/uwsgi-nginx-flask:python3.8

RUN apt update && apt -y install cron

RUN apt -y install \
  libcups2 \
  imagemagick

RUN apt --no-install-recommends -y install \
  texlive-base \
  texlive-extra-utils \
  texlive-generic-recommended \
  texlive-fonts-recommended \
  texlive-font-utils \
  texlive-latex-base \
  texlive-latex-recommended \
  texlive-latex-extra \
  #texlive-math-extra \
  texlive-pictures \
  texlive-pstricks \
  texlive-science \
  perl-tk \
  purifyeps \
  chktex \
  latexmk \
  dvipng \
  dvidvi \
  fragmaster \
  lacheck \
  latexdiff \
  libfile-which-perl \
  dot2tex \
  tipa \
  cm-super \
  #latex-xcolor \
  prosper
  #pgf

RUN apt -y install texlive-lang-german

RUN pip install \
  pytest \
  sphinx \
  requests \
  beautifulsoup4 \
  numpy \
  pandas \
  xlrd \
  matplotlib \
  scipy

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

COPY entrypoint.sh /entrypoint_new.sh
RUN chmod +x /entrypoint_new.sh
ENTRYPOINT ["/entrypoint_new.sh"]

CMD ["/start.sh"]
