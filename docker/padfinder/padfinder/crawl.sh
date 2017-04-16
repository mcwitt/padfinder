#!/bin/bash

subregion=$(cat /etc/padfinder/subregion)

while true; do
    /usr/local/bin/scrapy crawl craig -a subregion=$subregion
    sleep 60
done
