#!/usr/bin/env bash
PROJECT_DIR='/apps/svr/project/code/HenKe/henke'
ENV='/apps/svr/project/code/HenKe/python3.6/bin/python3'

# shellcheck disable=SC2164
cd $PROJECT_DIR

$ENV manage.py shell

