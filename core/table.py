#!/usr/bin/python3.10.6
# -*- coding: utf-8 -*-
#
# @Time    : 2024/4/30 下午1:36
# @Author  : ASXE

import pickle
import sys
import threading

from typing import Tuple, List, Dict, Any, Optional, AnyStr

from column import Column
from core import SerializedInterface, BPlusTree
from page import Page
from row import Row


class Table(SerializedInterface):
    """表结构"""

    def __init__(self, name: str, columns: List[Tuple[str, str]]):
        self.name = name
        self.__columnObj: Dict = {}
        self.__index: Dict[AnyStr, BPlusTree] = {}  # 索引
        self.__initColumn(columns)
        self.__pages = [Page(), ]  # 页
        self.__lock = threading.RLock()

    def __initColumn(self, columns: List[Tuple[str, str]]):
        """初始化列名列表"""
        for column in columns:
            self.__columnObj[column[0]] = Column(column[0], column[1])
            self.__index[column[0]] = BPlusTree()

    def insert(self, row: Dict[AnyStr, Any]):
        """插入数据"""
        newRow = Row()
        for columnName, columnValue in row.items():
            newRow.setValue(columnName, columnValue)
            self.__index[columnName].insert(columnValue, newRow)

        with self.__lock:
            currentPage = self.__pages[-1]
            if len(currentPage) >= currentPage.rowMax:
                currentPage = Page()
                self.__pages.append(currentPage)
            currentPage.addRow(newRow)

    def select(self, condition: Optional[Dict[AnyStr, Any]] = None) -> List[Row]:
        """选择符合条件的行"""
        with self.__lock:
            if condition:
                # 如果有条件，根据索引加速查找
                for columnName, columnValue in condition.items():
                    if columnName in self.__index:
                        return self.__index[columnName].search(columnValue) or []
            else:
                # 没有条件，返回所有行
                result = []
                for page in self.__pages:
                    result.extend(page.rows)
                return result
        return []

    def update(self, condition: Dict[AnyStr, Any], newValues: Dict[AnyStr, Any]):
        """更新符合条件的行"""
        with self.__lock:
            rows2Update = self.select(condition)
            for row in rows2Update:
                for columnName, columnValue in newValues.items():
                    oldValue = row.getValue(columnName)
                    row.setValue(columnName, columnValue)
                    # 更新索引
                    self.__index[columnName].insert(columnValue, row)

    def delete(self, condition: Dict[AnyStr, Any]):
        """删除符合条件的行"""
        with self.__lock:
            rows2Delete = self.select(condition)
            for row in rows2Delete:
                for columnName in self.__columnObj.keys():
                    columnValue = row.getValue(columnName)
                    self.__index[columnName].remove(columnValue)
                for page in self.__pages:
                    page.deleteRow(row)

    def serialized(self) -> bytes:
        """序列化表数据"""
        data = {
            'name': self.name,
            'columns': list(self.__columnObj.keys()),
            'pages': [page.serialized() for page in self.__pages]
        }
        return pickle.dumps(data)

    def deserialized(self, data: bytes):
        """反序列化表数据"""
        obj = pickle.loads(data)
        self.name = obj['name']
        self.__columnObj = {col: Column(col, None) for col in obj['columns']}
        self.__pages = [Page().deserialized(page) for page in obj['pages']]


if __name__ == '__main__':
    table = Table('test', [('a', 'int'), ('b', 'float')])
    table.insert({'a': 666, 'b':77.7})
    print(table.select()[0].values)
