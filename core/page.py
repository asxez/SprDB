#!/usr/bin/python3.10.6
# -*- coding: utf-8 -*-
#
# @Time    : 2024/5/13 下午7:05
# @Author  : ASXE

import pickle
from typing import List, Dict, Any

from row import Row


class Page:
    """页结构"""

    def __init__(self):
        self.rowMax = 258
        self.rows: List[Row] = []

    def __len__(self):
        return len(self.rows)

    def __contains__(self, row):
        return row in self.rows

    def addRow(self, row: Row):
        if len(self) < self.rowMax:
            self.rows.append(row)

    def __iter__(self):
        return iter(self.rows)

    def deleteRow(self, row: Row):
        """删除特定行"""
        if row in self.rows:
            self.rows.remove(row)

    def deleteRows(self, condition: Dict[str, Any]):
        """删除符合条件的行"""
        self.rows = [row for row in self.rows if not row.matchCondition(condition)]

    def serialized(self) -> bytes:
        """序列化页数据"""
        return pickle.dumps([row.serialized() for row in self.rows])

    def deserialized(self, data: bytes):
        """反序列化页数据"""
        rows = pickle.loads(data)
        self.rows = [Row().deserialized(row) for row in rows]
        return self
