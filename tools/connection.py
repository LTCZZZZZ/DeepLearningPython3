import os
import sys
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)
import configparser
# import json
# import requests
# import MySQLdb
# from sqlalchemy import create_engine
# import aiomysql
# from urllib.parse import quote_plus


class Myconfigparser(configparser.ConfigParser):

    def optionxform(self, optionstr):
        return optionstr


def config_dict(section):
    # section为配置文件“信息块”的名字
    config = Myconfigparser()
    config.read(os.path.join(os.path.dirname(os.path.dirname(
        os.path.abspath(__file__))), '.env'))
    return config._sections[section]


# def connection(section, DictCursor=True):
#     d = config_dict(section)
#     conn = MySQLdb.connect(host=d['HOST'], user=d['USER'], password=d[
#                            'PASSWORD'], port=int(d['PORT']), charset='utf8', db=d['NAME'])
#     if DictCursor:
#         cursor = conn.cursor(cursorclass=MySQLdb.cursors.DictCursor)
#     else:
#         cursor = conn.cursor()
#     cursor.execute("SET NAMES utf8")
#     return conn, cursor


# connmem, curmem = connection('db_cn')


# def get_engine(section):
#     # dialect+driver://username:password@host:port/database
#     d = config_dict(section)
#     # print(f"mysql+mysqldb://{d['USER']}:{d['PASSWORD']}@{d['HOST']}:{(d['PORT'])}/{d['NAME']}?charset=utf8")
#     # 密码里面带@，新版的SQLAlchemy的create_engine就会有问题，需要把@替换成%40
#     engine = create_engine(f"mysql+mysqldb://{d['USER']}:{quote_plus(d['PASSWORD'])}@{d['HOST']}:{(d['PORT'])}/{d['NAME']}?charset=utf8")
#     return engine


# def get_aiomysql_pool(section):
#     # 多次测试发现，size设为3的时候，综合速度是最快的。。。
#     d = config_dict(section)
#     return aiomysql.create_pool(
#         host=d['HOST'],
#         port=int(d['PORT']),
#         user=d['USER'],
#         password=d['PASSWORD'],
#         db=d['NAME'],
#         minsize=30,
#         maxsize=30,
#         echo=False,
#         autocommit=False,
#         loop=None,
#     )
