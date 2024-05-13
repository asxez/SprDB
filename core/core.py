#!/usr/bin/python3.10.6
# -*- coding: utf-8 -*-
#
# @Time    : 2024/4/25 上午8:41
# @Author  : ASXE

import pickle


class SerializedInterface:
    """序列化接口"""
    pickle: pickle = pickle

    def serialized(self):
        ...

    def deserialized(self):
        ...


class CompressInterface:
    """压缩"""

    def compress(self):
        ...

    def decompress(self):
        ...


def convertType(type: str):
    if type.lower() == 'int':
        return int()
    elif type.lower() == 'float':
        return float()
    elif type.lower() == 'str':
        return str()
