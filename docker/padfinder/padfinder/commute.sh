#!/usr/bin/env bash

while true; do
    python update_commutes.py \
           --destination "University of Washington Station, Seattle, USA" \
           --destination "Capitol Hill Station, Seattle, USA" \
           --destination "Westlake Station, Seattle, USA" \
           --destination "University Street Station, Seattle, USA" \
           --destination "Pioneer Square Station, Seattle, USA" \
           --destination "Intl. District/Chinatown Station, Seattle, USA" \
           --destination "Stadium Station, Seattle, USA" \
           --destination "SODO Station, Seattle, USA" \
           --destination "Beacon Hill Station, Seattle, USA" \
           --destination "Mount Baker Station, Seattle, USA" \
           --destination "Columbia City Station, Seattle, USA" \
           --destination "Othello Station, Seattle, USA" \
           --destination "Rainier Beach Station, Seattle, USA" \
           --destination "Stone Gardens Seattle, Seattle, USA" \
           --destination "Seattle Bouldering Project, Seattle, USA" \
           --transit-mode walking \
           --transit-mode bicycling \
           --download-delay 10
    sleep 900
done
