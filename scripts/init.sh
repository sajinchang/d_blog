#!/usr/bin/env bash
# PROJECT_DIR='/apps/svr/project/code/HenKe/henke'

# shellcheck disable=SC2164
# cd $PROJECT_DIR

# ENV='/apps/svr/project/code/HenKe/python3.6/bin/python3'
# 初始化数据库

cd ../

mkdir -p /app/d_blog/media/upload
mkdir -p /app/log/d_blog/nginx

python manage.py makemigrations blog
python manage.py makemigrations xmy
python manage.py makemigrations account
python  manage.py migrate


# 创建大类   创建高级管理
python manage.py collectstatic
#$ENV '../manage.py' createsuperuser
