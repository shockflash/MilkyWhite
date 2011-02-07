#!/bin/sh -e
#
# Starts the milkywhite update/install process. Only uses "start"

set -e

COMMAND="$1"

case $COMMAND in
start) 
  /opt/milkywhite/env/bin/python /opt/milkywhite/milkywhite/server.py
;;
esac