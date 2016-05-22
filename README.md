[![Docker Stars](https://img.shields.io/docker/stars/frankie567/twitterautoreplybot.svg?style=flat-square)](https://hub.docker.com/r/frankie567/twitterautoreplybot/) [![Docker Pulls](https://img.shields.io/docker/pulls/frankie567/twitterautoreplybot.svg?style=flat-square)](https://hub.docker.com/r/frankie567/twitterautoreplybot/)

# Twitter Auto-Reply Bot

A simple bot that provides a clean web interface to configure and track auto-reply campaigns to tweets matching your queries. Useful for marketing or customer support purposes.

## Warning about Twitter terms of service

This kind of bot is **COMPLETELY FORBIDDEN** by Twitter terms of service. I cannot be held responsible for anything that would happen to you or your Twitter account.

## Installation

Installation has been made very easy thanks to [Docker](https://www.docker.com/). If you don't have Docker already installed, just follow the [getting started tutorial](https://docs.docker.com/mac/).

1. Once Docker in installed, we just need to pull the container :
`docker pull frankie567/twitterautoreplybot`

2. Docker will now do the hard work. Let's build the system :
`docker-compose build`

3. We now need to run a few Django commands to create the database structure and load some necessary fixtures :
    1. `docker-compose run django python manage.py syncdb`
    At the end of this command, the prompt will ask you to create a super-user account. You will use it to login to the web interface.
    2. `docker-compose run django python manage.py makemigrations`
    3. `docker-compose run django python manage.py loaddata initial_data`

4. The last thing to do is setup the environnement variables containing the Twitter and Bitly credentials :
    1. Copy the `.env.dist` file to `.env` file. This file contains the environnement variables used by Docker :
    `cp .env.dist .env`
    2. Fill in the required Twitter credentials, including your username and password (more informations about this in the next sections).
    3. Fill in the required Bitly API credentials.

5. Yes, I told that the previous step was the last one. Once issue [#1](https://github.com/frankie567/twitterautoreplybot/issues/1) is resolved, this step will not be necessary anymore. We need to set the Docker machine IP in the `ningx/nginx.conf` file.
    1. Use this command to know your Docker machine IP :
    `docker-machine ip`
    2. Copy and paste your IP at line 13 in `ningx/nginx.conf` file. Like this :
    `server_name 192.168.99.100;`
    
Twitter Auto-Reply Bot should now be up and running. Type your Docker machine IP in a browser to access the web interface.
