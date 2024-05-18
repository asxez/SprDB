#!/usr/bin/python3.10.6
# -*- coding: utf-8 -*-
#
# @Time    : 2024/5/14 下午2:26
# @Author  : ASXE


import pickle

from typing import Any, Dict


class Row:
    def __init__(self):
        self.values: Dict[str, Any] = {} # 值

    def setValue(self, columnName: str, value: Any) -> None:
        """存值"""
        self.values[columnName] = value

    def getValue(self, columnName: str) -> Any:
        """取值"""
        return self.values.get(columnName)

    def serialized(self) -> bytes:
        """序列化行数据"""
        return pickle.dumps(self.values)

    def deserialized(self, data: bytes) -> 'Row':
        """反序列化行数据"""
        self.values = pickle.loads(data)
        return self
