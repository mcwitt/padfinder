#!/bin/bash

crawl-subregion() {
    while true; do
        /usr/local/bin/scrapy crawl craig -a subregion=$1
        sleep 60
    done
}

while true; do
    python update_commutes.py \
        --destination "120 Kearney St, San Francisco, USA" \
        --destination "Mission Cliffs, San Francisco, USA" \
        --destination "Dogpatch Boulders, San Francisco, USA" \
        --destination "California Academy of Sciences, San Francisco, USA"
    sleep 900
done &

crawl-subregion sfc &
crawl-subregion eby &
crawl-subregion nby 
