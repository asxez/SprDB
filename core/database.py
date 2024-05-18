#!/usr/bin/python3.10.6
# -*- coding: utf-8 -*-
#
# @Time    : 2024/4/30 下午1:36
# @Author  : ASXE

import lzma
import os
import pickle
import shutil
from typing import List, Tuple, Any

from common import log
from core import SerializedInterface, CompressInterface
from .table import Table


class Database(SerializedInterface, CompressInterface):

    def __init__(self, name: str):
        self.name = name
        self.tables = []

    def createTable(self, name: str, columns: List[Tuple[str, str]]) -> None:
        """创建表"""
        if name in self.tables:
            log.error('Table already exists.', 'tableExistsError')
        self.tables.append(name)
        with lzma.open(f'./{self.name}/{name}.db', 'wb') as file:
            newTable = Table(name, columns)
            data = self.compress(self.serialized(newTable.serialized()))
            file.write(data)

    def dropTable(self, name: str) -> None:
        """删除表"""
        if name not in self.tables:
            log.error('Table not exists.', 'tableNotExistsError')
        os.remove(f'{name}.db')

    def serialized(self, data: Any) -> bytes:
        """序列化"""
        return pickle.dumps(data)

    def deserialized(self, data: bytes) -> Any:
        """反序列化"""
        return pickle.loads(data)

    def compress(self, data: bytes) -> bytes:
        """压缩"""
        return lzma.compress(data)

    def decompress(self, data: bytes) -> bytes:
        """解压缩"""
        return lzma.decompress(data)


def createDatabase(databaseName: str) -> Database:
    """创建数据库"""
    if os.path.exists(databaseName):
        log.error('Database already exists.', 'databaseExistsError')
    os.makedirs(databaseName)
    return Database(databaseName)


def dropDatabase(databaseName: str) -> None:
    """删除数据库"""
    shutil.rmtree(databaseName)
