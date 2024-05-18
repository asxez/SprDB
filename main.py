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


def main(syntax: Dict[str, Dict]):
    global thisDatabase
    if 'CREATE_DATABASE' in syntax:
        dbInfo = syntax['CREATE_DATABASE']
        createDatabase(dbInfo['databaseName'])
        thisDatabase = Database(dbInfo['databaseName'])

    elif 'CREATE_TABLE' in syntax:
        if thisDatabase is None:
            log.error()
            return

        tableInfo = syntax['CREATE_TABLE']
        thisDatabase.createTable(tableInfo['tableName'], tableInfo['columns'])

    elif 'DROP_DATABASE' in syntax:
        ...

    elif 'DROP_TABLE' in syntax:
        ...

    elif 'INSERT' in syntax:
        if thisDatabase is None:
            log.error()
            return

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

    elif 'SELECT' in syntax:
        if thisDatabase is None:
            log.error()
            return

        selectInfo = syntax['SELECT']

    elif 'UPDATE' in syntax:
        if thisDatabase is None:
            log.error()
            return

        updateInfo = syntax['UPDATE']

    elif 'DELETE' in syntax:
        if thisDatabase is None:
            log.error()
            return

        deleteInfo = syntax['DELETE']

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
