#!/usr/bin/python3.10.6
# -*- coding: utf-8 -*-
#
# @Time    : 2024/5/11 下午1:38
# @Author  : ASXE

from core import convertType


class Column:
    def __init__(self, name: str, type: str):
        self.name = name
        self.type = convertType(type)
