#!/usr/bin/python3.10.6
# -*- coding: utf-8 -*-
#
# @Time    : 2024/5/21 下午3:27
# @Author  : ASXE

import socket
import subprocess
import threading
from typing import List, Dict

from common import log, Logger, curdir
from common.config import port
from core import Row
from parser import parser

logger = Logger(f'{curdir}/logs/server')


def executeQuery(statement: str) -> List[Row | Dict] | None:
    syntax = parser.SyntaxParser(statement, logger).parse()
    return parser.SemanticParser(logger).main(syntax, mode=1)


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


def startupServe():
    """设置开机自启动"""
    command = ['nssm.exe', 'install', 'sprserve', 'sprserve.exe']
    result = subprocess.run(command, capture_output=True, text=True)
    if result.returncode != 0:
        log.error('Failed to set auto-start.', 'systemError')
        return
    log.info('Success, are you sure to restart your computer? (yes or no)')
    while True:
        choice = input()
        if choice.lower() in ['yes', 'y']:
            subprocess.run(['shutdown', '/r', '/t', '0'])
        elif choice.lower() in ['no', 'n']:
            log.warning(
                "You haven't restarted your computer, so you'll need to manually go to the service to start it.")
            break
        else:
            log.warning('Please input yes or no.')
            continue


def destartupServe():
    """取消自启动"""
    command = ['nssm.exe', 'remove', 'sprserve']
    result = subprocess.run(command, capture_output=True, text=True)
    if result.returncode != 0:
        log.error('Failed to set destartup-auto.', 'systemError')
        return
    log.info('Success.')
