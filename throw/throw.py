#!usr/bin/python3.12.2
# -*-  coding: utf-8 -*-
#
# @Time    : 2024/4/21 下午1:50
# @Author  : KeFang
# @Email   : 19130728969@163.com
# @File    : throw.py
# Software : PyCharm
import inspect
import sys


def warning(waring_message=''):
    """传入警告信息"""
    if waring_message == '':
        return "warning为空"
    stack = inspect.stack()
    stack = stack[1]
    file_name = stack.filename
    function = stack.function
    row = stack.lineno
    # 输出黄色文本
    print(
        f"\033[93mWarning:\033[3m  \033[93m{waring_message}\n{file_name} in {function} \033[35m{row} \033[93mrow")


def error(error_message='', error_type=''):
    """传入错误信息,以及错误类型,结束程序"""
    if error_message == '' or error_type == '':
        return "error为空"
    stack = inspect.stack()
    stack = stack[1]
    file_name = stack.filename
    function = stack.function
    row = stack.lineno
    # 输出红色文本
    print(
        f"\033[91m{error_type.title()}:\033[3m  \033[91m{error_message}\n{file_name} in {function} \033[35m{row} \033[91mrow")
    sys.exit(1)


def info(info=''):
    """传入info信息"""
    if info == '':
        return "info为空"
    stack = inspect.stack()
    stack = stack[1]
    file_name = stack.filename
    function = stack.function
    row = stack.lineno
    # 输出绿色文本
    print(
        f"\033[92mInfo:\033[3m  \033[92m{info}\n{file_name} in {function} \033[35m{row} \033[92mrow")
