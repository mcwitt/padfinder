#!/bin/bash

mkdir /etc/padfinder/
echo $1 > /etc/padfinder/subregion

/etc/init.d/padfinder-crawl start
/etc/init.d/padfinder-commute start

touch /var/log/padfinder-crawl
touch /var/log/padfinder-commute

tail -f /var/log/padfinder-crawl \
     -f /var/log/padfinder-commute
