import hashlib
import os
import pickle
from functools import lru_cache

import redis

host = os.getenv('redis_host')
port = os.getenv('redis_port')
db = os.getenv('redis_db')
password = os.getenv('redis_password')


class ExpiredKeyException(object):
    pass


class RedisNoConnException(Exception):
    pass


class RedisCache(object):
    """
    Helper class to make connection to redis and story key value pair.

    """

    # Create a key using prefix. Format is prefix:key

    def make_key(self, prefix, key):
        format_key = 'Redis Cache - {}:{}'.format(prefix, key)
        return self.get_hash_of_key(format_key)

    # Store the key and value in redis store

    def store(self, prefix, key, value, expire=None):
        pipe = self.get_redis_connection().pipeline()
        if expire is None:
            pipe.set(self.make_key(prefix, key), value)
        else:
            pipe.setex(self.make_key(prefix, key=key), expire, value)
        pipe.execute()

    # Store the key and value in redis store using pickle to serialize object

    def store_pickle(self, prefix, key, value, expire=None):
        self.store(prefix, key, pickle.dumps(value), expire)

    # Returns the value from key store

    def get(self, prefix, key):
        value = self.get_redis_connection().get(self.make_key(prefix, key=key))
        if value is None:
            raise ExpiredKeyException
        else:
            return value

    def get_csci_salt(self):
        return bytes.fromhex(os.environ['CSCI_SALT'])

    #
    def get_hash_of_key(self, key):
        return hashlib.sha256((str(self.get_csci_salt()) + key).encode()).digest()

    def get_pickle(self, prefix, key):
        return pickle.loads(self.get(prefix, key=key))

    @lru_cache(maxsize=32)
    def get_redis_connection(self, connection_name='redis'):
        print('Getting Redis Connection....')
        try:
            redis.StrictRedis(host=host, port=port, password=None).ping()
        except redis.ConnectionError:
            raise RedisNoConnException("Failed to create connection to redis",
                                       (host,
                                        port)
                                       )
            # Returns a redis connection

        return redis.StrictRedis(host=host,
                                 port=port,
                                 db=db,
                                 password=None)
