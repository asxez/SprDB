#!/usr/bin/python3.10.6
# -*- coding: utf-8 -*-
#
# @Time    : 2024/4/30 下午1:36
# @Author  : ASXE

from .core import SerializedInterface
from common import log


class Table(SerializedInterface):

    def __init__(self):
        ...

    def insert(self):
        ...

    def select(self):
        ...

    def update(self):
        ...

    def delete(self):
        ...

    def serialized(self):
        ...

    def deserialized(self):
        ...
