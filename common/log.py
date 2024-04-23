#!usr/bin/python3.12.2
# -*-  coding: utf-8 -*-
#
# @Time    : 2024/4/21 下午1:50
# @Author  : KeFang

import inspect
import sys


def warning(warningMessage=''):
    """传入警告信息"""
    if warningMessage == '':
        return "warning为空"
    stack = inspect.stack()[1]
    file_name = stack.filename
    function = stack.function
    row = stack.lineno
    # 输出黄色文本
    print(
        f"\033[93mWarning:\033[3m  \033[93m{warningMessage}\n{file_name} in {function} \033[35m{row} \033[93mrow")


def error(errorMessage='', errorType=''):
    """传入错误信息,以及错误类型,结束程序"""
    if errorMessage == '' or errorType == '':
        return "error为空"
    stack = inspect.stack()[1]
    file_name = stack.filename
    function = stack.function
    row = stack.lineno
    # 输出红色文本
    print(
        f"\033[91m{errorType.title()}:\033[3m  \033[91m{errorMessage}\n{file_name} in {function} \033[35m{row} \033[91mrow")
    sys.exit(1)


def info(info=''):
    """传入info信息"""
    if info == '':
        return "info为空"
    stack = inspect.stack()[1]
    file_name = stack.filename
    function = stack.function
    row = stack.lineno
    # 输出绿色文本
    print(
        f"\033[92mInfo:\033[3m  \033[92m{info}\n{file_name} in {function} \033[35m{row} \033[92mrow")


if __name__ == '__main__':
    warning('test warning')
    info('test info')
    error('test error', 'test')
