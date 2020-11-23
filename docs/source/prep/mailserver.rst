Mailserver
==========

For sending emails and reminders a mailserver or, more specifically a
SMTP-server is needed. The ZIM already preinstalled an exim4 server and set it
up to send email (probably relaying them to their own server). But since the
emails are going to be sent from inside the docker container some further setup
is needed.

First of all the server has to be configured to act as a relay for the docker
container. For this the IP of the container has to be known. Docker uses a
'bridge' to transmit network traffic between the host (our server) and the
container. The IP can be found by running ::

  $ ifconfig

The interface corresponding to the bridge is the one called `docker0` and should
have the IP `172.17.0.1`, which can be found at the `inet` entry. This has to be
added to the exim4 configuration. the relevant file is in
`/etc/exim4/update-exim4.conf.conf` First the IP of the bridge has to be added
to the local interfaces to allow relaying, so it has to be added to the line
`dc_local_interfaces` and the relaying has to be enabled by adding the subnet
`172.17.0.0/16` to `dc_relay_nets`. Then exim4 has to be reconfigured by ::

  $ sudo /usr/sbin/update-exim4.conf

and the service restarted ::

  $ service exim4 restart

This information is from
`here <https://gehrcke.de/2014/07/discourse-docker-container-send-mail-through-exim/>`_.

Finally incoming traffic has to be allowed from inside the docker containter
through the firewall. This is done by ::

  $ sudo ufw allow from 172.17.0.2

where `172.17.0.2` is the bridge ip of the container.

Emails can then be send with the `SendEmail` function. It sets all the necessary
met data

.. currentmodule:: geclass.send_email
.. autofunction:: SendEmail(recipient, subject, content)
