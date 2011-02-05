#!/bin/sh -e
#
# Starts the milkywhite update/install process. Only uses "start"

set -e

COMMAND="$1"

case $COMMAND in
start)
  rm -rf /opt/milkywhite/milkywhite/
  mkdir -p /opt/milkywhite/milkywhite/
  
  wget -dump_source " # # # where is milkywhite?? # # # /milkywhite.tar.bz2" <<<<<<<<-----------------<<<<<<<<<<-------------
    
  cd /opt/milkywhite/milkywhite/
  tar -jxvf milkywhite.tar.bz2
  rm milkywhite.tar.bz2
  
  python /opt/milkywhite/milkywhite/server.py
;;
esac