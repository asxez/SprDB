#!/usr/bin/python3.10.6
# -*- coding: utf-8 -*-
#
# @Time    : 2024/4/21 下午10:43
# @Author  : ASXE

import inspect


def __LINE__():
    stack_t = inspect.stack()
    ttt = inspect.getframeinfo(stack_t[1][0])
    return ttt.lineno


def __FUNC__():
    stack_t = inspect.stack()
    ttt = inspect.getframeinfo(stack_t[1][0])
    return ttt.function


# 此时是桩函数
def error(arg): ...
