#!/usr/bin/python3.10.6
# -*- coding: utf-8 -*-
#
# @Time    : 2024/4/30 下午1:36
# @Author  : ASXE

import lzma
import os
import shutil
from typing import List, Tuple

from common import curdir, Logger, log
from .core import SerializedInterface, CompressInterface
from .table import Table

systemTable = '__system'
systemTableColumn = [('table', 'str')]


class Database(SerializedInterface, CompressInterface):
    """数据库类"""

    def __init__(self, name: str):
        self.name = name

    def createTable(self, name: str, columns: List[Tuple[str, str]]) -> str:
        """创建表"""
        if os.path.exists(f'{curdir}/data/{self.name}/{name}.db'):
            log.error('Table already exists.', 'tableExistsError')
            return 'Table already exists.'

        if name != systemTable:  # 将用户创建的表名插入系统表以记录
            table = Table(systemTable)
            with lzma.open(f'{curdir}/data/{self.name}/{systemTable}.db', 'rb') as file:
                data = file.read()

            data = table.decompress(data)
            table.deserialized(data)
            table.insert(['table'], [[name]])

            with lzma.open(f'{curdir}/data/{self.name}/{systemTable}.db', 'wb') as file:
                data = table.compress(table.serialized())
                file.write(data)

        # 创建表只需要初始化一个空表
        with lzma.open(f'{curdir}/data/{self.name}/{name}.db', 'wb') as file:
            newTable = Table(name, columns)
            data = newTable.compress(newTable.serialized())
            file.write(data)

    def dropTable(self, name: str, logger: Logger) -> str:
        """删除表"""
        if not os.path.exists(f'{curdir}/data/{self.name}/{name}.db'):
            logger.error('There is no such table.', 'tableNotExistsError')
            return 'There is no such table.'
        os.remove(f'{curdir}/data/{self.name}/{name}.db')
        return 'true'


def createDatabase(databaseName: str) -> Database | str:
    """创建数据库"""
    if os.path.exists(f'{curdir}/data/{databaseName}'):
        log.error('Database already exists.', 'databaseExistsError')
        return 'Database already exists.'
    os.makedirs(f'{curdir}/data/{databaseName}')
    database = Database(databaseName)
    database.createTable(systemTable, systemTableColumn)
    return Database(databaseName)


def dropDatabase(databaseName: str, logger: Logger) -> str:
    """删除数据库"""
    if not os.path.exists(f'{curdir}/data/{databaseName}'):
        logger.error('There is no such database.', 'databaseNotExistsError')
        return 'There is no such database.'
    shutil.rmtree(f'{curdir}/data/{databaseName}')
    return 'true'


def useDatabase(databaseName: str, logger: Logger) -> Database | str:
    """切换数据库"""
    if os.path.exists(f'{curdir}/data/{databaseName}'):
        return Database(databaseName)
    logger.error('There is no such database.', 'databaseNotExistsError')
    return 'There is no such database.'
