docker run \
  -itd \
  --rm \
  -v geclass_instance:/app/instance \
  -v geclass_log:/var/log/geclass\
  -p 80:80 \
  -e FLASK_KEY=${FLASK_KEY} \
  --name geclass \
  geclass:latest

docker exec -it geclass /bin/bash -c 'service cron start'
