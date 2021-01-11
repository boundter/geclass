docker run \
  -it \
  --rm \
  -v $PWD:/app \
  -v geclass_log:/var/log/geclass\
  -p 80:80 \
  -e FLASK_KEY=${FLASK_KEY} \
  -e QUAMP_USER=$QUAMP_USER \
  -e QUAMP_PASSWD=$QUAMP_PASSWD \
  --name geclass \
  geclass:latest

docker exec -it geclass /bin/bash -c 'service cron start'
