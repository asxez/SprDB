#!/usr/bin/python3.10.6
# -*- coding: utf-8 -*-
#
# @Time    : 2024/4/23 下午2:01
# @Author  : ASXE

import lzma
import pickle
import sys
from typing import Dict, Optional

from common import log
from core.database import Database, createDatabase
from core.table import Table
from parser import parser

# TODO

thisDatabase: Optional[Database] = Database('asxe')


def writeNewData(tableName: str, table: Table):
    with lzma.open(f'./{thisDatabase.name}/{tableName}.db', 'wb') as file:
        data = thisDatabase.compress(thisDatabase.serialized(table.serialized()))
        file.write(data)


def main(syntax: Dict[str, Dict]):
    global thisDatabase
    if 'CREATE_DATABASE' in syntax:
        dbInfo = syntax['CREATE_DATABASE']
        createDatabase(dbInfo['databaseName'])
        thisDatabase = Database(dbInfo['databaseName'])

    elif 'CREATE_TABLE' in syntax:
        if thisDatabase is None:
            log.error()

        tableInfo = syntax['CREATE_TABLE']
        thisDatabase.createTable(tableInfo['tableName'], tableInfo['columns'])

    elif 'DROP_DATABASE' in syntax:
        ...

    elif 'DROP_TABLE' in syntax:
        ...

    elif 'INSERT' in syntax:
        if thisDatabase is None:
            log.error()

        insertInfo = syntax['INSERT']
        tableName = insertInfo['table']
        values = insertInfo['values']
        columns = insertInfo['columns']

        with lzma.open(f'./{thisDatabase.name}/{tableName}.db', 'rb') as file:
            data = file.read()
            data = lzma.decompress(data)
            data = pickle.loads(data)
        table = Table(tableName)
        table.deserialized(data)
        table.insert(columns, values)

        writeNewData(tableName, table)

    elif 'SELECT' in syntax:
        if thisDatabase is None:
            log.error()

        selectInfo = syntax['SELECT']
        tableName = selectInfo['from']
        with lzma.open(f'./{thisDatabase.name}/{tableName}.db', 'rb') as file:
            data = file.read()
            data = lzma.decompress(data)
            data = pickle.loads(data)
        table = Table(tableName)
        table.deserialized(data)
        rows = table.select(selectInfo)
        for row in rows:
            print(row)

    elif 'UPDATE' in syntax:
        if thisDatabase is None:
            log.error()

        updateInfo = syntax['UPDATE']
        tableName = updateInfo['table']
        with lzma.open(f'./{thisDatabase.name}/{tableName}.db', 'rb') as file:
            data = file.read()
            data = lzma.decompress(data)
            data = pickle.loads(data)

        table = Table(tableName)
        table.deserialized(data)
        table.update(updateInfo)

        writeNewData(tableName, table)

    elif 'DELETE' in syntax:
        if thisDatabase is None:
            log.error()

        deleteInfo = syntax['DELETE']
        tableName = deleteInfo['table']
        with lzma.open(f'./{thisDatabase.name}/{tableName}.db', 'rb') as file:
            data = file.read()
            data = lzma.decompress(data)
            data = pickle.loads(data)

        table = Table(tableName)
        table.deserialized(data)
        table.delete(deleteInfo)

        writeNewData(tableName, table)

    else:
        log.error()


if __name__ == '__main__':
    print("sprDB >>> ", end='')
    while True:
        statement = input('')
        if statement == 'exit':
            print('Good Bye!')
            sys.exit(0)
        parse = parser.SyntaxParser(statement)
        main(parse.parse())
        print("sprDB >>> ", end='')
