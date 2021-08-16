import urllib3
import sqlite3
import os


def init(data_file='config.yml', raw_database_variables={}):
    global config, connection
    config = set_config(data_file)
    connection = set_database_connection()


def set_http_manager():
    return urllib3.PoolManager()


def set_database_connection():
    connection = sqlite3.connect('db')

    return connection
