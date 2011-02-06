#!/bin/sh -e
#
# Starts the milkywhite update/install process. Only uses "start"

set -e

COMMAND="$1"

case $COMMAND in
start) 
  /usr/bin/python /opt/milkywhite/milkywhite/server.py
;;
esac