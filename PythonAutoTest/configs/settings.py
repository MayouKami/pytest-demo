# settings.py
import os
import configparser
from pathlib import Path

# 获取项目根目录
BASE_DIR = Path(__file__).resolve().parent.parent

# 加载配置文件
config = configparser.ConfigParser()
config.read(BASE_DIR / 'configs' / 'config.ini')

# 数据库配置
DB_CONFIG = {
    'server': config['DATABASE']['DB_SERVER'],
    'database': config['DATABASE']['DB_NAME'],
    'username': config['DATABASE']['DB_USER'],
    'password': config['DATABASE']['DB_PASSWORD'],
    'driver': config['DATABASE']['DB_DRIVER'],
    'port': config['DATABASE']['DB_PORT'],
    'timeout': int(config['DATABASE']['DB_TIMEOUT'])
}


# 获取当前文件所在目录的父目录（项目根目录）
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))