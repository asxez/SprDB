#!/usr/bin/python3.10.6
# -*- coding: utf-8 -*-
#
# @Time    : 2024/5/11 下午1:38
# @Author  : ASXE


from typing import Optional


class Column:
    def __init__(self, name: str, type: Optional[str]):
        self.name = name
        self.type = type
