#!/usr/bin/python3.10.6
# -*- coding: utf-8 -*-
#
# @Time    : 2024/5/21 下午3:27
# @Author  : ASXE


import socket
import threading
from typing import List, Dict

from common.config import port
from core import Row
from parser import parser


def executeQuery(statement: str) -> List[Row | Dict] | None:
    syntax = parser.SyntaxParser(statement).parse()
    return parser.SemanticParser().main(syntax, mode=1)


def handleClient(clientSocket: socket.socket) -> None:
    try:
        # 接收数据
        request = clientSocket.recv(1024).decode('utf-8')

        result = executeQuery(request)

        # 将结果转换为字符串并发送回客户端
        response = str(result)
        clientSocket.send(response.encode('utf-8'))
    finally:
        clientSocket.close()


def startServer(host='0.0.0.0', port=port) -> None:
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((host, port))
    server.listen(151)

    while True:
        try:
            server.settimeout(0.5)
            clientSocket, addr = server.accept()

            # 为每个客户端创建一个新线程
            clientHandler = threading.Thread(target=handleClient, args=(clientSocket,))
            clientHandler.start()
        except socket.timeout:
            continue
