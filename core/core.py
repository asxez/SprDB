#!/usr/bin/python3.10.6
# -*- coding: utf-8 -*-
#
# @Time    : 2024/4/25 上午8:41
# @Author  : KeFang

import os
import shutil
from itertools import islice

from common import log


def determine(file):
    return os.path.exists(file)


def createDatabase(file):
    """添加数据库"""
    if determine(file):
        log.error("database already exists", "Creating database")
    try:
        os.mkdir(file)
        log.info(f"created {file}")
        return file
    except FileExistsError:
        log.error("database create false", "Creating false")


def dropDatabase(file):
    """删除数据库"""
    if not determine(file):
        log.error("database not exists", "Dropping database")
    try:
        shutil.rmtree(file)
        log.info(f"dropped {file}")
    except OSError as e:
        log.error(f"Error: {e}", "Dropping database")


def createTable(dataName, table, dataType):
    """创建表"""
    dataName = dataName + "\\" + table + ".db"
    if determine(dataName):
        log.error("table already exists", "Creating table")
    key = []
    value = []
    # 存储字段位置,为之后的获取值添加消息
    n = 0
    for i in dataType.keys():
        key.append(i)
        value.append(dataType[i] + ":" + str(n))
        n += 1
    dataType = dict(zip(key, value))
    with open(dataName, "w", encoding="utf-8") as f:
        f.write(str(dataType) + "\n")
    log.info(f"created {dataName}")


def dropTable(dataName, table):
    """删除表"""
    dataName = dataName + "\\" + table + ".db"
    flag = determine(dataName)
    if not flag:
        log.error("table not exists", "Dropping table")
    try:
        os.remove(dataName)
        log.info(f"dropped {dataName}")
    except OSError as e:
        log.error(f"Error: {e}", "Dropping table")


def insert(databaseName, table, dataSource):
    """插入数据"""
    file = databaseName + "\\" + table + ".db"
    flag = determine(file)
    if not flag:
        log.error("table not exists", "Inserting table")
    value = []
    for i in dataSource.keys():
        value.append(dataSource[i])
    # 压缩文件
    with open(file, "a") as f:
        f.writelines(str(value) + "\n")
        f.close()


def selectUseEQ(databaseName, table, dataCheck=None):
    """返回集合,集合中是查询数据的集合"""
    result = []
    file = databaseName + "\\" + table + ".db"
    if dataCheck is None:
        f = open(file, "r", encoding="utf-8")
        for line in islice(f, 2, None):
            line = line.strip()
            result.append(line)
        return result
    # 将map取出后转化为map集合才行
    # else:
    #     with open(file, "r", encoding="utf-8") as f:
    #         temp = f.readlines()
    # target = temp[0]
    # value = []
    # for i in dataCheck.keys():


if __name__ == '__main__':
    liss = selectUseEQ("mydata", "table")
    print(liss)
#
# if __name__ == '__main__':
#     data = {"a": 1, "b": 2, "c": 3}
#     insert("mydata", "table", data)
#
# if __name__ == '__main__':
#     createDatabase("mydata")
#     datatype = {"a": "int", "b": "int", "c": "int"}
#     createTable("mydata", "table", datatype)
#
# if __name__ == '__main__':
#     dropTable("mydata", "table")
#     dropDatabase("mydata")
