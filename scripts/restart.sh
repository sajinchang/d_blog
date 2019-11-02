#!/usr/bin/env bash

PIDFILE='/app/d_blog/logs/gunicorn.pid'

# 暴力重启
#$PORJECT_DIR/scripts/stop.sh
#$PORJECT_DIR/scripts/start.sh

# 平滑重启
# shellcheck disable=SC2046
kill -HUP `cat $PIDFILE`