#!/usr/bin/python3.10.6
# -*- coding: utf-8 -*-
#
# @Time    : 2024/5/21 下午3:27
# @Author  : ASXE

import socket

from common.config import port


def sendQuery(query: str, host: str = '127.0.0.1', port: int = port) -> None:
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((host, port))

    try:
        client.send(query.encode('utf-8'))
        response = client.recv(4096).decode('utf-8')
        print(f"Received response: {response}")
    finally:
        client.close()


if __name__ == '__main__':
    while True:
        a = input()
        sendQuery(a)
