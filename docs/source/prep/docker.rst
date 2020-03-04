Docker
======

What is Docker?
---------------

Docker is a serive to virtualize software. Very simplified, it starts a new
computer on the current host. This allows first of all for continuity between
the development and production. If the program runs in docker on one machine it
will also run on all others.

Secondly docker makes it easy to start and restart the service. Just stopping
and restarting docker allows the program to start and restart and can be done in
a few seconds.

To discern between different 'computer setups' in docker (for example between
Ubuntu and Windows or so on) there is the concept of images. Images tell docker
how to setup the machine and which program to start. These images can be created
by yourself or downloaded from dockerhub.

Images can be imagined as templates how to setup the machine. The actual running
machine is called a container. In this container you can execute code or
commands. Of every image there can be multiple running containers.

Building the Image
------------------

There is a Dockerfile contained in the repository. From this the image can be
build. It is based on a uswgi, nginx and flask image from dockerhub. This allows
to run the app
without having to install the dependencies on the host. To build an image from the Dockerfile ::

  $ docker build -t geclass .

The `-t` sets the name of the image (geclass in this case) and `.` just means to
use the local Dockerfile.

Starting the Container
----------------------

The container has one property that needs to be always considered, the data in
the container is not persistent. It is possible to mount directories and files
from the host and the read and write on them. So if data has to persist between
different containers (like databases or logs) it has to be written on such a
mount. The best way to handle this is with docker volumes. These are special
directories created and organized by docker. To create such a volume ::

  $ docker volume create volume_name

Here `volume_name` denotes the name the volume should be called. It is most
useful to create two volumes for the application, one for the database and
website data and one for the logs. For the sake of simplicity they are called
`geclass_instance` for the website data and `geclass_log` for the logs.

To simply run a container the following command can be used ::

  $ docker run --rm -it --name geclass geclass:latest /bin/bash

This will start a bash shell (`-it` is needed to use it as a terminal) in the
container named geclass (the `name` option) from the latest geclass (`geclass:latest`) image and delete it
after all connections are closed (denoted by the `rm`). The last command
`/bin/bash` denotes the program that should be started, if none is given the
default given by the Dockerfile will be started, which is the webserver in this
case.

Assuming the webserver was started then the container can be accesed externally
by using the command ::

  $ docker exec -it geclass /bin/bash

Now the webserver may be running, but it cannot be accesed from the outside,
because the traffic is not rerouted from the host to the container. Standard web
traffic uses the port 80, so the corresponding port of the container has to be
exposed. ::

  $ docker run -it --rm -p 80:80 --name geclass geclass:latest

The container is now reachable from the outside (`-it` is not needed because we
do not want to use the server as a terminal but it does not hurt), but the data does not persist.
After the container is closed all users will be deleted. To persist the data the
volumes from earlier have to be mounted. the data should be mounted to
`/app/instance` and the logs to `/var/log/geclass`. The corresponding command
lokks like this ::

  $ docker run -it --rm -v geclass_instance:/app/instance -v geclass_log:/var/log/geclass -p 80:80 --name geclass geclass:latest

Now the webserver is nearly perfectly setup, there are only two steps left. The
flask-server needs a secret key to create the Cookies for the users. No key was
passed in, so it used the default `dev` key which is not very secure. So a key
has to be passed as an enviromental variable ::

  $ docker run -it --rm -v geclass_instance:/app/instance -v geclass_log:/var/log/geclass -p 80:80 -e FLASK_KEY=1234 --name geclass geclass:latest

With the `-e` option the key can be set to anything (in this case 1234). And
finally this container now blocks the terminal, when the terminal closes the
containter will also close. To run it in the background the `-d` option can be
used. The final command to start the server is now ::

  $ docker run -itd --rm -v geclass_instance:/app/instance -v geclass_log:/var/log/geclass -p 80:80 -e FLASK_KEY=1234 --name geclass geclass:latest

Now the webserver is running, accessible, persistent and secure. But to send
daily reminders the program cron has to be started. For this the command
`service cron start` has to be executed in the container. This can be done by ::

  $ docker exec -it geclass /bin/bash -c 'service cron start'

All of this is conveniently written in a short script called `server.sh` and can
be accessed by ::

  $ export FLASK_KEY=1234; ./server.sh

The first part sets the secret key and the second part after the ';' executes
the script.

To stop the webserver it suffices to ::

  $ docker kill geclass

