#!/usr/bin/python3.10.6
# -*- coding: utf-8 -*-
#
# @Time    : 2024/4/30 下午1:36
# @Author  : ASXE

import lzma
import os
import pickle
import shutil
from typing import List, Tuple

from common import log
from .core import SerializedInterface, CompressInterface
from .table import Table


class Database(SerializedInterface, CompressInterface):

    def __init__(self, name: str):
        self.databaseName = name
        self.__tables = []

    def createTable(self, name: str, columns: List[Tuple[str]]):
        """创建表"""
        if name in self.__tables:
            log.error('table already exists.', 'tableExistsError')
        self.__tables.append(name)
        with lzma.open(f'./{self.databaseName}/{name}.db', 'wb') as file:
            file.write(self.compress(self.serialized(Table(name, columns))))

    def dropTable(self, name: str):
        """删除表"""
        if name not in self.__tables:
            log.error('table not exists.', 'tableNotExists')
        os.remove(f'{name}.db')

    def serialized(self, data):
        """序列化"""
        return pickle.dumps(data)

    def deserialized(self, data):
        """反序列化"""
        return pickle.loads(data)

    def compress(self, data):
        """压缩"""
        return lzma.compress(data)

    def decompress(self, data):
        """解压缩"""
        return lzma.decompress(data)


def createDatabase(databaseName: str) -> Database:
    """创建数据库"""
    if os.path.exists(databaseName):
        log.error('database already exists.', 'databaseExistsError')
    os.makedirs(databaseName)
    return Database(databaseName)


def dropDatabase(databaseName: str) -> None:
    """删除数据库"""
    shutil.rmtree(databaseName)
