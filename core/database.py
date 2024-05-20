#!/usr/bin/python3.10.6
# -*- coding: utf-8 -*-
#
# @Time    : 2024/4/30 下午1:36
# @Author  : ASXE

import lzma
import os
import shutil
from typing import List, Tuple, Optional

from common import log
from .core import SerializedInterface, CompressInterface
from .table import Table

systemTable = '__system'
systemTableColumn = [('table', 'str')]


class Database(SerializedInterface, CompressInterface):

    def __init__(self, name: str):
        self.name = name
        self.tables = []

    def __loadTables(self) -> None:
        """加载表名列表"""
        with lzma.open(f'./data/{self.name}/{systemTable}.db', 'rb') as file:
            data = file.read()
        return self.deserialized(data)

    def createTable(self, name: str, columns: List[Tuple[str, str]]) -> None:
        """创建表"""
        if name in self.tables:
            log.error('Table already exists.', 'tableExistsError')
            return

        if name != systemTable: # 将用户创建的表名插入系统表以记录
            self.tables.append(name)
            table = Table(systemTable)
            with lzma.open(f'./data/{self.name}/{systemTable}.db', 'rb') as file:
                data = file.read()

            data = table.decompress(data)
            table.deserialized(data)
            table.insert(['table'], [[name]])

            with lzma.open(f'./data/{self.name}/{systemTable}.db', 'wb') as file:
                data = table.compress(table.serialized())
                file.write(data)

        # 创建表只需要初始化一个空表
        with lzma.open(f'./data/{self.name}/{name}.db', 'wb') as file:
            newTable = Table(name, columns)
            data = newTable.compress(newTable.serialized())
            file.write(data)

        self.__loadTables()

    def dropTable(self, name: str) -> None:
        """删除表"""
        if name not in self.tables:
            log.error('Table not exists.', 'tableNotExistsError')
            return
        os.remove(f'{name}.db')


def createDatabase(databaseName: str) -> Optional[Database]:
    """创建数据库"""
    if os.path.exists(databaseName):
        log.error('Database already exists.', 'databaseExistsError')
        return
    os.makedirs(f'./data/{databaseName}')
    database = Database(databaseName)
    database.createTable(systemTable, systemTableColumn)
    return Database(databaseName)


def dropDatabase(databaseName: str) -> None:
    """删除数据库"""
    shutil.rmtree(databaseName)


def useDatabase(databaseName: str) -> Database:
    """切换数据库"""
    return Database(databaseName)
