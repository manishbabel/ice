import os

from functools import lru_cache

import psycopg2

dbname = os.getenv('database')
user = os.getenv('user')
port = os.getenv('port')
host = os.getenv('host')
password = os.getenv('password')


@lru_cache(maxsize=32)
def get_connection(connection_name='db'):
    """
    This function returns postgres connection and keep in cache.

    :param connection_name:
    :return:
    """
    print('Getting postgres connection!')
    try:
        return psycopg2.connect(
            dbname=dbname,
            user=user,
            port=port,
            host=host,
            password=password)
    except Exception:
        print('Error Connecting Database!')
