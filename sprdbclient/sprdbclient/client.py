#!/usr/bin/python3.10.6
# -*- coding: utf-8 -*-
#
# @Time    : 2024/5/24 下午1:38
# @Author  : ASXE

import socket
from typing import Optional

from config import host, port


class SprClient:
    def __init__(self, host=host, port=port):
        self.host = host
        self.port = port
        self.client: Optional[socket.socket] = None

    def __enter__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.connect((self.host, self.port))
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.client.close()

    def execute(self, query: str):
        try:
            self.client.send(query.encode())
            res = self.client.recv(4096).decode()
            return {
                'res': res
            }
        finally:
            self.client.close()


if __name__ == '__main__':
    with SprClient() as c:
        print(c.execute('create database asxe'))
