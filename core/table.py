#!/usr/bin/python3.10.6
# -*- coding: utf-8 -*-
#
# @Time    : 2024/4/30 下午1:36
# @Author  : ASXE

import lzma
import pickle
import threading
from typing import Tuple, List, Dict, Any, Optional, AnyStr

from common import log
from .column import Column
from .core import SerializedInterface, CompressInterface, BPlusTree
from .page import Page
from .row import Row


class Table(SerializedInterface, CompressInterface):
    """表结构"""

    def __init__(self, name: str, columns: Optional[List[Tuple[str, str]]] = None):
        self.name = name
        self.__columnObj: Dict = {}  # 列对象
        self.__index: Dict[AnyStr, BPlusTree] = {}  # 索引
        if columns:
            self.__initColumn(columns)  # 有可能是加载数据库，此时则不需要初始化列
        self.__pages = [Page(), ]  # 页对象
        self.__lock = threading.RLock()

    def __initColumn(self, columns: List[Tuple[str, str]]) -> None:
        """初始化列名列表"""
        for column in columns:
            self.__columnObj[column[0]] = Column(column[0], column[1])
            self.__index[column[0]] = BPlusTree()

    def insert(self, columns: List[str], rows: List[List[Any]]) -> None:
        """插入数据"""
        if columns == ['*']:  # 若是 * 则更新为所有列名
            columns = [column for column in self.__columnObj.keys()]

        if len(columns) != len(rows[0]):  # 检测插入的数据与需要插入数据的列的数量是否匹配
            log.error("Number of columns doesn't match number of values", 'valueError')

        with self.__lock:
            for rowData in rows:
                if len(rowData) != len(columns):
                    log.error("Number of values in row doesn't match number of columns.", 'valueError')

                rowValues = {colName: None for colName in self.__columnObj}
                for colName, colValue in zip(columns, rowData):
                    if colName not in self.__columnObj:
                        log.error(f"Column '{colName}' does not exist in table.", 'columnNotExistsError')

                    column = self.__columnObj[colName]
                    if column.type == 'int':
                        try:
                            colValue = int(colValue)
                        except ValueError:
                            log.error(f"Invalid value '{colValue}' for column '{colName}'. Expected int.", 'typeError')
                    elif column.type == 'float':
                        try:
                            colValue = float(colValue)
                        except ValueError:
                            log.error(f"Invalid value '{colValue}' for column '{colName}'. Expected float.",
                                      'typeError')
                    elif column.type == 'str':
                        if not isinstance(colValue, str):
                            log.error(f"Invalid value '{colValue}' for column '{colName}'. Expected str.", 'typeError')
                    else:
                        log.error(f"Unsupported data type '{column.type}' for column '{colName}'", 'typeError')

                    rowValues[colName] = colValue

                newRow = Row()
                newRow.values = rowValues

                for columnName, columnValue in rowValues.items():
                    if columnValue is not None:
                        self.__index[columnName].insert(columnValue, newRow)  # 更新索引

                currentPage = self.__pages[-1]
                if len(currentPage) >= currentPage.rowMax:
                    currentPage = Page()
                    self.__pages.append(currentPage)
                currentPage.addRow(newRow)

    def parseCondition(self, condition: List[List | str | Tuple]):
        def parseSingleCondition(cond):
            if isinstance(cond, list):
                return self.parseCondition(cond)

            column, operator, value = cond
            if operator == '=':
                return lambda row: row.getValue(column) == value
            # elif operator == '!=':
            #     return lambda row: row.getValue(column) != value
            elif operator == '<':
                return lambda row: row.getValue(column) < value
            elif operator == '<=':
                return lambda row: row.getValue(column) <= value
            elif operator == '>':
                return lambda row: row.getValue(column) > value
            elif operator == '>=':
                return lambda row: row.getValue(column) >= value
            else:
                log.error(f"Unsupported operator: {operator}.", 'valueError')

        if not condition:
            return lambda row: True

        def combineConditions(conditions):
            if len(conditions) == 1:
                return parseSingleCondition(conditions[0])

            left = parseSingleCondition(conditions[0])
            operator = conditions[1]
            right = combineConditions(conditions[2:])

            if operator.lower() == 'and':
                return lambda row: left(row) and right(row)
            elif operator.lower() == 'or':
                return lambda row: left(row) or right(row)
            else:
                log.error(f"Unsupported logical operator: {operator}.", 'valueError')

        return combineConditions(condition)

    def select(self, query: Dict[AnyStr, Any]) -> List[Row | dict]:
        """选择符合条件的行"""
        with self.__lock:
            if 'where' in query:  # 如有 where 子句
                condition = query['where']
                conditionFn = self.parseCondition(condition)
            else:
                conditionFn = lambda row: True

            columns2Select = query['columns']  # 只需要返回指定列
            selectedRows = []
            for page in self.__pages:
                for row in page.rows:
                    if conditionFn(row):
                        if columns2Select == ['*']:
                            selectedRows.append(row.values)
                        else:
                            selectedRow = {col: row.getValue(col) for col in columns2Select}
                            selectedRows.append(selectedRow)

            return selectedRows

    def update(self, query: Dict[AnyStr, Any]) -> None:
        """更新符合条件的行"""
        with self.__lock:
            condition = query['where']
            conditionFn = self.parseCondition(condition)  # 解析 where 子句
            setClause = query['set']

            for page in self.__pages:
                for row in page.rows:
                    if conditionFn(row):
                        for columnName, newValue in setClause:
                            oldValue = row.getValue(columnName)
                            row.setValue(columnName, newValue)
                            # 更新索引
                            self.__index[columnName].remove(oldValue)
                            self.__index[columnName].insert(newValue, row)

    def delete(self, query: Dict[AnyStr, Any]) -> None:
        """删除符合条件的行"""
        with self.__lock:
            # 解析 where 子句
            condition = query['where']
            conditionFn = self.parseCondition(condition)

            rows2Delete = []
            for page in self.__pages:
                for row in page.rows:
                    if conditionFn(row):
                        rows2Delete.append(row)
                        for columnName in self.__columnObj.keys():
                            columnValue = row.getValue(columnName)
                            self.__index[columnName].remove(columnValue)
                page.rows = [row for row in page.rows if row not in rows2Delete]

    def serialized(self) -> bytes:
        """序列化表数据"""
        data = {
            'name': self.name,
            'columns': self.__columnObj,
            'pages': [page.serialized() for page in self.__pages],
            'index': self.__index
        }
        return pickle.dumps(data)

    def deserialized(self, data: bytes):
        """反序列化表数据"""
        obj = pickle.loads(data)
        self.name = obj['name']
        self.__columnObj = obj['columns']
        self.__pages = [Page().deserialized(page) for page in obj['pages']]
        self.__index = obj['index']

    def compress(self, data: bytes) -> bytes:
        """压缩数据"""
        return lzma.compress(data)

    def decompress(self, data: bytes) -> bytes:
        """解压数据"""
        return lzma.decompress(data)
