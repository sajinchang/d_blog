#!/usr/bin/env bash

PIDFILE='/app/d_blog/logs/gunicorn.pid'

kill `cat $PIDFILE`
