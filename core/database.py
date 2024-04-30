#!/usr/bin/python3.10.6
# -*- coding: utf-8 -*-
#
# @Time    : 2024/4/30 下午1:36
# @Author  : ASXE

import os

from .core import SerializedInterface
from common import log


class DataBase(SerializedInterface):

    def __init__(self, name: str):
        self.databaseName = name
        self.__tableName = []

    def createDatabase(self):
        if os.path.exists(self.databaseName):
            log.error('database already exists.', 'databaseExistsError')
        os.makedirs(self.databaseName)

    def dropDatabase(self):
        os.rmdir(self.databaseName)

    def createTable(self, name: str):
        ...

    def existsTable(self):
        ...

    def dropTable(self):
        ...
