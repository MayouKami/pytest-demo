# -*- coding: gbk -*-
import pyodbc
from dbutils.pooled_db import PooledDB
from configs.settings import DB_CONFIG
import types

class DBManager:
    pool = PooledDB(
        creator=pyodbc,
        driver=DB_CONFIG['driver'],
        host=DB_CONFIG['server'],
        port=DB_CONFIG['port'],
        database=DB_CONFIG['database'],
        user=DB_CONFIG['username'],
        password=DB_CONFIG['password'],
        mincached=2,  # 最小空闲连接数
        maxcached=5,  # 最大空闲连接数
        maxconnections=10,  # 最大连接数
        blocking=True  # 无可用连接时是否阻塞等待
    )
    
    @staticmethod
    def get_connection():
        return DBManager.pool.connection()
    
    @staticmethod
    def execute_query(conn, sql, params=None):
        with conn.cursor() as cursor:
            cursor.execute(sql, params or ())
            return cursor.fetchall()
    
    @staticmethod
    def execute_update(conn, sql, params=None):
        with conn.cursor() as cursor:
            cursor.execute(sql, params or ())
            return cursor.rowcount