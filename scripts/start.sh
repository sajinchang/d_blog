#!/usr/bin/env bash

# PROJECT_DIR='/opt/d_blog'
# ENV_DIR='/env/django/bin/activate'
# shellcheck disable=SC1090
# source $ENV_DIR
# shellcheck disable=SC2164
# cd $PROJECT_DIR

# gunicorn -c d_blog/gunicorn_config.py d_blog.wsgi

uwsgi --ini ../uwsgi.ini