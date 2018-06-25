#!/usr/bin/env bash

set -x

mkdir /etc/padfinder/
echo "$@" > /etc/padfinder/args

/etc/init.d/padfinder-crawl start
/etc/init.d/padfinder-commute start

touch /var/log/padfinder-crawl.log
touch /var/log/padfinder-commute.log

tail -f /var/log/padfinder-crawl.log \
     -f /var/log/padfinder-commute.log
