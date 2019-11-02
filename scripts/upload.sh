#!/usr/bin/env bash

LOCAL_DIR='../'
REMOTE_DIR='/opt/d_blog'
#/apps/svr/project/code

USER='root'
HOST='samsa.club'

rsync -crvP --exclude={migrations,static/uploads/,.vscode/,.git/,.vev,logs/,__pycache__,.ieda/,media/,medias/,db.sqlite3} $LOCAL_DIR $USER@$HOST:$REMOTE_DIR

# 远程重启
 # shellcheck disable=SC2029
 ssh $USER@$HOST  bash "$REMOTE_DIR/scripts/restart.sh"

