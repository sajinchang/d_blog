#!/usr/bin/env bash

PIDFILE='/app/d_blog/logs/gunicorn.pid'

# shellcheck disable=SC2046
kill `cat $PIDFILE`
