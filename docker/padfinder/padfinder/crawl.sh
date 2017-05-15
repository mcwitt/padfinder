#!/usr/bin/env bash

set -x

config_dir=$1
subregion=$(cat "$config_dir/subregion")

while true; do
    scrapy crawl craig -a subregion=$subregion
    sleep 60
done
