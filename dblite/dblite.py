#! /usr/bin/env python3

import sqlite3, aiosqlite
from async_class import AsyncObject

class dbLite(object):
    def __init__(self, db_name):
        self.conn = sqlite3.connect(db_name, isolation_level=None, check_same_thread=False)
        self.cursor = self.conn.cursor()
        self.cursor.execute('PRAGMA journal_mode = WAL;')
        self.cursor.execute('PRAGMA synchronous = OFF;')
        self.cursor.execute('PRAGMA cache_size = 1000000;')
        self.cursor.execute('PRAGMA locking_mode = EXCLUSIVE;')
        self.cursor.execute('PRAGMA temp_store = MEMORY;')

    def create(self, table_name, **kwargs):
        data = ', '.join(f"{k} {v}" for k, v in kwargs.items())
        query = f"CREATE TABLE IF NOT EXISTS {table_name} ({data})"
        self.cursor.execute(query)
        self.conn.commit()
        
    def drop(self, table_name):
        query = f"DROP TABLE IF EXISTS {table_name}"
        self.cursor.execute(query)
        self.conn.commit()

    def add(self, table_name, **kwargs):
        col = ', '.join(list(kwargs.keys()))
        val = ', '.join('?' * len(list(kwargs.values())))
        query = f"INSERT INTO {table_name} ({col}) VALUES ({val})"
        self.cursor.execute(query, tuple(list(kwargs.values())))
        self.conn.commit()

    def add_list(self, target, source, col, **kwargs):
        condition = ' AND '.join("{} IN ({})".format(k, ','.join(f'"{x}"' for x in kwargs[k])) for k in kwargs)
        query = f"INSERT INTO {target} SELECT {col} FROM {source} WHERE {condition}"
        self.cursor.execute(query)
        self.conn.commit()

    def remove(self, table_name, **kwargs):
        condition = ' AND '.join(f"{k} = ?" for k, _ in kwargs.items())
        query = f"DELETE FROM {table_name} WHERE {condition}"
        self.cursor.execute(query, tuple(list(kwargs.values())))
        self.conn.commit()

    def select(self, table_name, data, **kwargs):
        condition = ' AND '.join(f"{k} = ?" for k, _ in kwargs.items())
        query = f"SELECT {data} FROM {table_name} WHERE {condition}"
        data = self.cursor.execute(query, tuple(list(kwargs.values())))
        return data.fetchall()
    
    def random(self, table_name, data):
        query = f"SELECT {data} FROM {table_name} ORDER BY RANDOM() LIMIT 1"
        data = self.cursor.execute(query)
        return list(map(' '.join, data.fetchall()))[0]

    def update(self, table_name, **kwargs):
        data_set = ', '.join(f"{k} = ?" for k in list(kwargs.keys())[:-1])
        condition = f"{list(kwargs.keys())[-1]} = ?"
        query = f"UPDATE {table_name} SET {data_set} WHERE {condition}"
        self.cursor.execute(query, tuple(list(kwargs.values())))
        self.conn.commit()

    def update_all(self, target, source, col):
        query = f"INSERT INTO {target} SELECT {col} FROM {source}"
        self.cursor.execute(query)
        self.conn.commit()

    def data(self, table_name):
        query = f"SELECT * FROM {table_name}"
        data = self.cursor.execute(query)
        return data.fetchall()

    def count_list(self, target):
        return self.cursor.execute(f"SELECT COUNT(1) FROM {target}").fetchone()[0]

    def close(self):
        self.cursor.close()
        self.conn.close()

    def __enter__(self):
        return self

    def __exit__(self):
        self.close()

class aioDbLite(AsyncObject):
    async def __ainit__(self, db_name):
        self.conn = await aiosqlite.connect(db_name, isolation_level=None, check_same_thread=False)
        self.cursor = await self.conn.cursor()
        await self.cursor.execute('PRAGMA journal_mode = WAL;')
        await self.cursor.execute('PRAGMA synchronous = OFF;')
        await self.cursor.execute('PRAGMA cache_size = 1000000;')
        await self.cursor.execute('PRAGMA locking_mode = EXCLUSIVE;')
        await self.cursor.execute('PRAGMA temp_store = MEMORY;')

    async def create(self, table_name, **kwargs):
        data = ', '.join(f"{k} {v}" for k, v in kwargs.items())
        query = f"CREATE TABLE IF NOT EXISTS {table_name} ({data})"
        await self.cursor.execute(query)
        await self.conn.commit()
        
    async def drop(self, table_name):
        query = f"DROP TABLE IF EXISTS {table_name}"
        await self.cursor.execute(query)
        await self.conn.commit()

    async def add(self, table_name, **kwargs):
        col = ', '.join(list(kwargs.keys()))
        val = ', '.join('?' * len(list(kwargs.values())))
        query = f"INSERT INTO {table_name} ({col}) VALUES ({val})"
        await self.cursor.execute(query, tuple(list(kwargs.values())))
        await self.conn.commit()
 
    async def add_list(self, target, source, col, **kwargs):
        condition = ' AND '.join("{} IN ({})".format(k, ','.join(f'"{x}"' for x in kwargs[k])) for k in kwargs)
        query = f"INSERT INTO {target} SELECT {col} FROM {source} WHERE {condition}"
        await self.cursor.execute(query)
        await self.conn.commit()

    async def remove(self, table_name, **kwargs):
        condition = ' AND '.join(f"{k} = ?" for k, _ in kwargs.items())
        query = f"DELETE FROM {table_name} WHERE {condition}"
        await self.cursor.execute(query, tuple(list(kwargs.values())))
        await self.conn.commit()

    async def select(self, table_name, data, **kwargs):
        condition = ' AND '.join(f"{k} = ?" for k, _ in kwargs.items())
        query = f"SELECT {data} FROM {table_name} WHERE {condition}"
        data = await self.cursor.execute(query, tuple(list(kwargs.values())))
        return await data.fetchall()
    
    async def random(self, table_name, data):
        query = f"SELECT {data} FROM {table_name} ORDER BY RANDOM() LIMIT 1"
        data = await self.cursor.execute(query)
        return list(map(' '.join, await data.fetchall()))[0]

    async def update(self, table_name, **kwargs):
        data_set = ', '.join(f"{k} = ?" for k in list(kwargs.keys())[:-1])
        condition = f"{list(kwargs.keys())[-1]} = ?"
        query = f"UPDATE {table_name} SET {data_set} WHERE {condition}"
        await self.cursor.execute(query, tuple(list(kwargs.values())))
        await self.conn.commit()

    async def update_all(self, target, source, col):
        query = f"INSERT INTO {target} SELECT {col} FROM {source}"
        await self.cursor.execute(query)
        await self.conn.commit()

    async def data(self, table_name):
        query = f"SELECT * FROM {table_name}"
        data = await self.cursor.execute(query)
        return await data.fetchall()

    async def count_list(self, target):
        return await self.cursor.execute(f"SELECT COUNT(1) FROM {target}").fetchone()[0]

    async def close(self):
        try:
            await self.conn.close()
        except ValueError:            
            pass

    async def __aenter__(self):
        return self

    async def __aexit__(self):
        await self.close()
