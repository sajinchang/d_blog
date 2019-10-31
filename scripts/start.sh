#!/usr/bin/env bash

PROJECT_DIR='/opt/d_blog'
ENV_DIR='/env/django/bin/activate'
source $ENV_DIR
cd $PROJECT_DIR

gunicorn -c d_blog/gunicorn_config.py d_blog.wsgi

