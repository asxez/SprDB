#!/usr/bin/python3.10.6
# -*- coding: utf-8 -*-
#
# @Time    : 2024/4/25 上午8:41
# @Author  : ASXE


class SerializedInterface:
    """序列化接口"""

    def serialized(self, data):
        ...

    def deserialized(self, data):
        ...


class CompressInterface:
    """压缩"""

    def compress(self, data):
        ...

    def decompress(self, data):
        ...


def convertType(type: str):
    if type.lower() == 'int':
        return int()
    elif type.lower() == 'float':
        return float()
    elif type.lower() == 'str':
        return str()
