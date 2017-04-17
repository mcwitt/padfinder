#!/bin/bash

subregion=$(cat /etc/padfinder/subregion)

while true; do
    scrapy crawl craig -a subregion=$subregion
    sleep 60
done
