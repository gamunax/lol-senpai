# Installation server

```shell
#> apt-get -qq -y update
#> apt-get -qq -y upgrade
#> apt-get -qq -y install git htop python3-pip haproxy
#> vim /etc/default/haproxy  # Set the ENABLED option to 1 (ENABLED=1)
#> git clone https://github.com/Stegoo/lol-senpai.git /senpai
#> cp /senpai/deploy/haproxy*.cfg /etc/haproxy/
#> vim /etc/haproxy/haproxy.cfg  # Set user/password (XXXXXXXXXX)
#> /etc/init.d/haproxy start
#> wget -qO- https://get.docker.com/ | sh
#> pip3 install -r /senpai/delivery/requirements.txt
#> docker run --name senpai-redis -d redis
```
