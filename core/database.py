#!/usr/bin/python3.10.6
# -*- coding: utf-8 -*-
#
# @Time    : 2024/4/30 下午1:36
# @Author  : ASXE

import os
import shutil
import pickle
import lzma

from .core import SerializedInterface, CompressInterface
from .table import Table
from common import log


class Database(SerializedInterface, CompressInterface):

    def __init__(self, name: str):
        self.databaseName = name
        self.__tableObj = {}

    def createTable(self, name: str, columns: list):
        """创建表"""
        if name in self.__tableObj:
            log.error('table already exists.', 'tableExistsError')
        self.__tableObj[name] = Table(name, columns)
        tableFile = os.open(f'./{self.databaseName}/{name}.db', os.O_RDWR | os.O_CREAT)
        os.write(tableFile, self.serialized())
        os.close(tableFile)
        ...

    def dropTable(self, name: str):
        """删除表"""
        if name not in self.__tableObj:
            log.error('table not exists.', 'tableNotExists')
        os.remove(f'{name}.db')

    def serialized(self):
        """序列化"""
        return pickle.dumps(self.__tableObj)

    def deserialized(self):
        """反序列化"""
        ...

    def compress(self):
        """压缩"""
        return lzma.compress

    def decompress(self):
        """解压缩"""
        return lzma.decompress


def createDatabase(databaseName: str) -> Database:
    """创建数据库"""
    if os.path.exists(databaseName):
        log.error('database already exists.', 'databaseExistsError')
    os.makedirs(databaseName)
    return Database(databaseName)


def dropDatabase(databaseName: str) -> None:
    """删除数据库"""
    shutil.rmtree(databaseName)
