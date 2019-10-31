#!/usr/bin/env bash
PROJECT_DIR='/apps/svr/project/code/HenKe/henke
'

cd $PROJECT_DIR

ENV='/apps/svr/project/code/HenKe/python3.6/bin/python3'
# 初始化数据库
bash scripts/migrate.sh

# 创建大类   创建高级管理
$ENV manage.py collectstatic
#$ENV '../manage.py' createsuperuser
