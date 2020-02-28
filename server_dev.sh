docker run \
  -it \
  --rm \
  -v $PWD:/app \
  -v geclass_instance:/app/instance \
  -v geclass_log:/var/log/geclass\
  -p 80:80 \
  -e FLASK_ENV=development \
  --name geclass_dev \
  geclass:latest \
  /bin/bash -c "flask run --host=0.0.0.0 --port=80"
