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
        """序列化"""
        ...

    def deserialized(self):
        """反序列化"""
        ...


class Compress:
    """压缩"""

    def compress(self):
        ...

    def uncompress(self):
        ...
