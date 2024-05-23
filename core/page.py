#!/usr/bin/python3.10.6
# -*- coding: utf-8 -*-
#
# @Time    : 2024/5/13 下午7:05
# @Author  : ASXE

import pickle
from typing import List

from .row import Row
from .core import SerializedInterface

class Page(SerializedInterface):
    """页结构"""

    def __init__(self):
        self.rowMax = 258 # 每页的最大行数
        self.rows: List[Row] = []

    def __len__(self):
        return len(self.rows)

    def __contains__(self, row):
        return row in self.rows

    def addRow(self, row: Row):
        """添加一行"""
        if len(self) < self.rowMax:
            self.rows.append(row)

    def __iter__(self):
        return iter(self.rows)

    def serialized(self) -> bytes:
        """序列化页数据"""
        return pickle.dumps([row.serialized() for row in self.rows])

    def deserialized(self, data: bytes):
        """反序列化页数据"""
        rows = pickle.loads(data)
        self.rows = [Row().deserialized(row) for row in rows]
        return self
