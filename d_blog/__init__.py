import pymysql

from libs.orm import patch_model

pymysql.install_as_MySQLdb()

patch_model()
