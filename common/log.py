#!usr/bin/python3.12.2
# -*-  coding: utf-8 -*-
#
# @Time    : 2024/4/21 下午1:50
# @Author  : KeFang and ASXE

import inspect
from typing import List, Dict, Any

from .config import DEBUG


def warning(warningMessage: str):
    """传入警告信息"""
    stack = inspect.stack()[1]
    print(
        f"\033[93m\033[3m{warningMessage}\033[0m")


def error(errorMessage: str, errorType: str):
    """传入错误信息,以及错误类型"""
    stack = inspect.stack()[1]
    fileName = stack.filename
    function = stack.function
    row = stack.lineno
    if DEBUG:
        print(
            f"\033[91m{errorType}:\033[3m \033[91m{errorMessage}\n{fileName} in {function} \033[35m{row} \033[91mrow\033[0m")
    else:
        print(
            f"\033[91m{errorType}:\033[3m \033[91m{errorMessage}\033[0m")


def info(message: str):
    """传入info信息"""
    print(
        f"\033[92m\033[3m{message}\033[0m")


class OutputTable:
    """表格式"""

    def __init__(self, data: List[Dict[str, Any]]):
        if len(data) == 0:
            info('No data.')

        self.headers = list(data[0].keys())  # 列名
        self.rows = [list(item.values()) for item in data]

    def __str__(self):
        # 计算列宽
        columnWidths = [max(len(str(item)) for item in column) for column in zip(self.headers, *self.rows)]

        # C为每行创建一个格式字符串，其中包含居中文本
        def formatRow(row):
            return ' | '.join(str(item).center(width) for item, width in zip(row, columnWidths))

        # 创建表字符串
        border = '+-' + '-+-'.join(['-' * width for width in columnWidths]) + '-+'
        headerStr = '| ' + ' | '.join(
            str(item).center(width) for item, width in zip(self.headers, columnWidths)) + ' |'
        rowsStr = '\n'.join(
            '| ' + ' | '.join(str(item).center(width) for item, width in zip(row, columnWidths)) + ' |' for row in
            self.rows)

        tableStr = f"{border}\n{headerStr}\n{border}\n{rowsStr}\n{border}"
        return tableStr
