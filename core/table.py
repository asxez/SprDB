#!/usr/bin/python3.10.6
# -*- coding: utf-8 -*-
#
# @Time    : 2024/4/30 下午1:36
# @Author  : ASXE

from typing import Tuple, List, Dict, AnyStr

from .column import Column
from .core import SerializedInterface
from .page import Page


class Table(SerializedInterface):

    def __init__(self, name: AnyStr, columns: List[Tuple[AnyStr]]):
        self.name = name
        self.__columnObj: Dict = {}
        self.__initColumn(columns)
        self.__page = []

    def __initColumn(self, columns: List[Tuple[AnyStr]]):
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

    def serialized(self, data):
        ...

    def deserialized(self, data):
        ...
