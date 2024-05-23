#!usr/bin/python3.12.2
# -*-  coding: utf-8 -*-
#
# @Time    : 2024/4/21 下午1:50
# @Author  : KeFang and ASXE

import inspect
import os
import time
from queue import Queue
from threading import Thread, Lock
from typing import List, Dict, Any

from .config import DEBUG, curdir


def warning(warningMessage: str):
    """传入警告信息"""
    print(f"\033[93m\033[3m{warningMessage}\033[0m")


def error(errorMessage: str, errorType: str):
    """传入错误信息,以及错误类型"""
    stack = inspect.stack()[1]
    fileName = stack.filename
    function = stack.function
    row = stack.lineno
    if DEBUG:
        print(
            f"\033[91m{errorType}:\033[3m \033[91m{errorMessage}\n{fileName} in {function} \033[35m{row} \033[91m row\033[0m")
    else:
        print(
            f"\033[91m{errorType}:\033[3m \033[91m{errorMessage}\033[0m")


def info(message: str):
    """传入info信息"""
    print(f"\033[92m\033[3m{message}\033[0m")


class OutputTable:
    """表格式"""

    def __init__(self, data: List[Dict[str, Any]]):
        if len(data) == 0:
            info('No data.')

        self.headers = list(data[0].keys())  # 列名
        self.rows = [list(item.values()) for item in data]

    def __str__(self):
        # 计算列宽
        columnWidths = [max(len(str(item)) for item in column) for column in zip(self.headers, *self.rows)]

        # 创建表字符串
        border = '+-' + '-+-'.join(['-' * width for width in columnWidths]) + '-+'
        headerStr = '| ' + ' | '.join(str(item).center(width) for item, width in zip(self.headers, columnWidths)) + ' |'
        rowsStr = '\n'.join(
            '| ' + ' | '.join(str(item).center(width) for item, width in zip(row, columnWidths)) + ' |' for row in
            self.rows)

        tableStr = f"{border}\n{headerStr}\n{border}\n{rowsStr}\n{border}"
        return tableStr


class Logger:
    """日志记录器"""

    def __init__(self, logDir=f'{curdir}/logs', logLevel='INFO', maxFileSize=10 ** 6, backupCount=10):
        self.logDir = logDir
        self.logLevel = logLevel
        self.maxFileSize = maxFileSize
        self.backupCount = backupCount
        self.logQueue = Queue()
        self.lock = Lock()
        self.logLevels = ['DEBUG', 'INFO', 'WARNING', 'ERROR']

        self.logLevelIndex = self.logLevels.index(self.logLevel)

        if not os.path.exists(self.logDir):
            os.makedirs(self.logDir)
        self.logFile = self.__getLogFile()

        self.__startLoggingThread()

    def __startLoggingThread(self):
        self.loggingThread = Thread(target=self.__processLogQueue)
        self.loggingThread.daemon = True
        self.loggingThread.start()

    def __processLogQueue(self):
        while True:
            logEntry = self.logQueue.get()
            if logEntry is None:
                break
            self.__writeLog(logEntry)

    def log(self, level, message):
        if self.logLevels.index(level) >= self.logLevelIndex:
            logEntry = f"{self.__currentTime()} - {level} - {message}\n"
            self.logQueue.put(logEntry)

    def debug(self, message):
        self.log('DEBUG', message)

    def info(self, message, output=False):
        if output:
            info(message)
        self.log('INFO', message)

    def warning(self, message, output=False):
        if output:
            warning(message)
        self.log('WARNING', message)

    def error(self, message, type, output=True):
        if output:
            error(message, type)
        self.log('ERROR', message)

    @staticmethod
    def __currentTime():
        return time.strftime('%H:%M:%S', time.localtime())

    def __getLogFile(self):
        currentDate = time.strftime('%Y%m%d', time.localtime())
        return os.path.join(self.logDir, f"log_{currentDate}.log")

    def __writeLog(self, logEntry):
        with self.lock:
            if os.path.exists(self.logFile) and os.path.getsize(self.logFile) >= self.maxFileSize:
                self.__rotateLogs()

            with open(self.logFile, 'a', encoding='utf-8') as file:
                file.write(logEntry)

    def __rotateLogs(self):
        for i in range(self.backupCount - 1, 0, -1):
            sfn = f"{self.logFile}.{i}"
            dfn = f"{self.logFile}.{i + 1}"
            if os.path.exists(sfn):
                if os.path.exists(dfn):
                    os.remove(dfn)
                os.rename(sfn, dfn)

        dfn = f"{self.logFile}.1"
        if os.path.exists(dfn):
            os.remove(dfn)
        os.rename(self.logFile, dfn)

    def stop(self):
        self.logQueue.put(None)
        self.loggingThread.join()
