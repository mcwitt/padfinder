#!/bin/bash

while true; do
    python update_commutes.py \
           --destination "Mission Cliffs, San Francisco, USA" \
           --destination "California Academy of Sciences, San Francisco, USA" \
           --transit-mode walking \
           --transit-mode bicycling \
           --transit-mode transit \
	         --transit-mode driving \
           --download-delay 10
    sleep 900
done
