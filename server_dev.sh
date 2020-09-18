docker run \
  -it \
  --rm \
  -v $PWD:/app \
  -v geclass_log:/var/log/geclass \
  -p 80:80 \
  -e FLASK_ENV=development \
  -e QUAMP_USER=$QUAMP_USER \
  -e QUAMP_PASSWD=$QUAMP_PASSWD \
  --name geclass_dev \
  geclass:latest \
  /bin/bash -c "flask run --host=0.0.0.0 --port=80"
