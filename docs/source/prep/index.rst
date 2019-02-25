Preparation
***********

Docker
======

There is a dockerfile contained in the repository. This allows to run the app
without having to install the dependencies. A docker container is a virtual
machine with a specific state. Such a container is the instanteation of an
image. To build an image from the Dockerfile ::

  $ docker build -t flasker .

The `-t` sets the name flasker.

To then run the container from the image the following command can be used: ::

  $ docker run --rm -v ${PWD}:/app -p 80:80 flasker

The Dockerfile automatically starts the necessary programs to serve the webpage.
The `--rm` deletes the container after it has been closed. If it is not
specified, the container will stay alive and block the port 80, stopping any new
containers from starting. The other options inclue `-v` to dynamically load the
current directory to the /app directory in the container. This is where the
server expects the files to be. `-p` exposes the port 80 of the host to the
containers and links it to its port 80.

To have mor influence on the container, it can be started with a shell command.
To gain a bash shell run the follwing ::

  $ docker run --rm -v ${PWD}:/app -p 80:80 -it flasker bash

Instead of bash other commands can be used, like `ls`. The `-it` flag sets the
connection to be interactive and a terminal. Finally to change the environment,
the `-e` flag can be passed. For example to init the database (**Careful: This
deletes the current database.**) the command is ::

  $ docker run --rm -v ${PWD}:/app -p 80:80 -e 'FLASK_APP=e_class' flasker flask init-db


