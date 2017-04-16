#!/bin/bash

while true; do
    python update_commutes.py \
        --destination "120 Kearny St, San Francisco, USA" \
        --destination "Mission Cliffs, San Francisco, USA" \
        --destination "Dogpatch Boulders, San Francisco, USA" \
        --destination "California Academy of Sciences, San Francisco, USA"
    sleep 900
done
