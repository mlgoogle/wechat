import os, platform

VERSION = '1.3.8'
BASE_URL = 'https://login.weixin.qq.com'
OS = platform.system() # Windows, Linux, Darwin
DIR = os.getcwd()
DEFAULT_QR = 'QR.png'
TIMEOUT = (10, 60)

USER_AGENT = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36'

KAFKA_HOST = '139.224.34.22'
KAFKA_TOPIC = 'robot'
SQL_HOST = '139.224.18.190'
SQL_USER = 'smobaspecialplane'
SQL_PASSWD = 'smobaspecialplane!@#$%^'
SQL_DBNAME = 'smoba_special_plane_t'
SQL_PORT = 3306
SQL_CHARSET = 'utf8'
