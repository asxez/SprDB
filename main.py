#!/usr/bin/python3.10.6
# -*- coding: utf-8 -*-
#
# @Time    : 2024/4/23 下午2:01
# @Author  : ASXE

import lzma
import sys
import os
from typing import Dict

from common import log, OutputTable
from core.database import Database, createDatabase, useDatabase
from core.table import Table
from parser import parser

# 若系统数据库不存在则创建
if not os.path.exists('./data/sprdb'):
    createDatabase('sprdb')
thisDatabase: Database = Database('sprdb')  # 默认


def writeNewData(tableName: str, table: Table):
    """为表写入新数据"""
    with lzma.open(f'./data/{thisDatabase.name}/{tableName}.db', 'wb') as file:
        data = table.compress(table.serialized())
        file.write(data)


def main(syntax: Dict[str, Dict]):
    """入口"""
    global thisDatabase
    if 'CREATE_DATABASE' in syntax:  # 创建数据库
        dbInfo = syntax['CREATE_DATABASE']
        createDatabase(dbInfo['databaseName'])
        thisDatabase = Database(dbInfo['databaseName'])

    elif 'CREATE_TABLE' in syntax:  # 创建表
        tableInfo = syntax['CREATE_TABLE']
        thisDatabase.createTable(tableInfo['tableName'], tableInfo['columns'])

    elif 'DROP_DATABASE' in syntax:
        ...

    elif 'DROP_TABLE' in syntax:
        ...

    elif 'USE' in syntax:  # 切换数据库
        thisDatabase = useDatabase(syntax['USE']['databaseName'])

    elif 'INSERT' in syntax:  # 插入数据
        insertInfo = syntax['INSERT']
        tableName = insertInfo['table']
        values = insertInfo['values']
        columns = insertInfo['columns']
        table = Table(tableName)

        with lzma.open(f'./data/{thisDatabase.name}/{tableName}.db', 'rb') as file:
            data = file.read()
            data = table.decompress(data)

        table.deserialized(data)
        table.insert(columns, values)

        writeNewData(tableName, table)

    elif 'SELECT' in syntax:  # 查询
        selectInfo = syntax['SELECT']
        tableName = selectInfo['from']
        table = Table(tableName)

        with lzma.open(f'./data/{thisDatabase.name}/{tableName}.db', 'rb') as file:
            data = file.read()
            data = table.decompress(data)

        table.deserialized(data)
        rows = table.select(selectInfo)
        try:
            output = OutputTable(rows)
        except:
            return
        print(output)

    elif 'UPDATE' in syntax:  # 更新
        updateInfo = syntax['UPDATE']
        tableName = updateInfo['table']
        table = Table(tableName)

        with lzma.open(f'./data/{thisDatabase.name}/{tableName}.db', 'rb') as file:
            data = file.read()
            data = table.decompress(data)

        table.deserialized(data)
        table.update(updateInfo)

        writeNewData(tableName, table)

    elif 'DELETE' in syntax:  # 删除
        deleteInfo = syntax['DELETE']
        tableName = deleteInfo['table']
        table = Table(tableName)

        with lzma.open(f'./data/{thisDatabase.name}/{tableName}.db', 'rb') as file:
            data = file.read()
            data = table.decompress(data)

        table.deserialized(data)
        table.delete(deleteInfo)

        writeNewData(tableName, table)

    else:
        log.error('There is no such command.', 'syntaxError')
        return


if __name__ == '__main__':
    print('Copyright (c) 2024 SprDB Software Foundation. All Rights Reserved.')
    print("sprDB >>> ", end='')
    while True:
        statement = input('')
        if statement == 'exit':
            print('Good Bye!')
            sys.exit(0)
        parse = parser.SyntaxParser(statement)
        main(parse.parse())
        print("sprDB >>> ", end='')
