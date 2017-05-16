#!/usr/bin/env bash

set -x

config_dir=$1
args=$(cat "$config_dir/args")

while true; do
    scrapy crawl craig $args
    sleep 60
done
