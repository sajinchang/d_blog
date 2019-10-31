#!/usr/bin/env bash
#/usr/bin/env bash
#PROJECT_DIR='/apps/svr/project/code/HenKe/henke'
PROJECT_DIR='/home/sam/work/yishan'
#ENV='/apps/svr/project/code/HenKe/python3.6/bin/python3'
ENV='/home/sam/.env/python3.6/bin/python3'

cd $PROJECT_DIR

$ENV manage.py runserver 0.0.0.0:8000

