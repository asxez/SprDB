#!/usr/bin/python3.10.6
# -*- coding: utf-8 -*-
#
# @Time    : 2024/5/13 下午7:05
# @Author  : ASXE

class Page:
    """页"""

    def __init__(self):
        self.rowMax = 258
        self.row = []

    def __len__(self):
        return len(self.row)

    def __contains__(self, row):
        return row in self.row
