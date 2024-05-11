#!/usr/bin/python3.10.6
# -*- coding: utf-8 -*-
#
# @Time    : 2024/4/30 下午1:36
# @Author  : ASXE

from .core import SerializedInterface
from .column import Column
from common import log


class Table(SerializedInterface):

    def __init__(self, name: str, columns: list):
        self.name = name
        self.__columnObj = []
        self.__initColumn(columns)

    def __initColumn(self, columns):
        """初始化列名列表"""
        for column in columns:
            self.__columnObj[column[0]] = Column(column[0], column[1])

    def insert(self):
        ...

    def select(self):
        ...

    def update(self):
        ...

    def delete(self):
        ...

    def serialized(self):
        ...

    def deserialized(self):
        ...
