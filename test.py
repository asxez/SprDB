#!/usr/bin/python3.10.6
# -*- coding: utf-8 -*-
#
# @Time    : 2024/4/24 下午10:11
# @Author  : ASXE

"""
this is a test file.
"""

from parser import parser
from core import Table


def testLexParser():
    lexParser = parser.LexParser("select a from b where c = '11'")
    lexParser.getNextToken()
    while lexParser.curToken.tokenType != parser.TokenType.TOKEN_END:
        print((lexParser.curToken.value, lexParser.curToken.tokenType, lexParser.preToken.tokenType))
        lexParser.getNextToken()


def testSyntaxParser():
    sparser1 = parser.SyntaxParser("create database a")
    print(sparser1.parse())
    sparser2 = parser.SyntaxParser("create table a (a int , b str ,)")
    print(sparser2.parse())
    sparser3 = parser.SyntaxParser("select a,b from t where (c='asxe' or d=1) and e=10")
    print(sparser3.parse())
    sparser4 = parser.SyntaxParser("insert into t values (1,2,3), (2,3,4)")
    print(sparser4.parse())
    sparser5 = parser.SyntaxParser("update t set a=1,b=2 where c='6'")
    print(sparser5.parse())
    sparser6 = parser.SyntaxParser("delete from t where a=1")
    print(sparser6.parse())


def testCore():
    table = Table("a", [("a", "int"), ("b", "int"), ("c", "str"), ("d", "float")])
    table.insert(['a', 'b', 'c'], [[1, 2, 'test'], [2, 2, 'example'], [1, 3, 'sample']])
    table.insert(['a', 'b', 'c'], [[1, 2, 'test'], [2, 2, 'example'], [1, 3, 'sample']])
    table.insert(['a', 'b', 'c'], [[1, 2, 'test'], [2, 2, 'example'], [1, 3, 'sample']])
    table.insert(['a', 'b', 'c'], [[1, 2, 'test'], [2, 2, 'example'], [1, 3, 'sample']])
    table.insert(['a', 'b', 'c', 'd'], [[10, 23, 'asxe', 12.1]])
    selectQuery = {'SELECT': {'columns': ['a', 'b'], 'from': 'a',
                              'where': [('a', '=', 10), 'or', ('b', '=', 2)]}}
    selectedRows = table.select(selectQuery['SELECT'])
    for row in selectedRows:
        print(f'select: {row}')

    updateQuery = {'UPDATE': {'table': 'a', 'set': [('b', 10), ('c', 'updated')],
                              'where': [('a', '=', 1), 'and', ('b', '=', 2)]}}
    table.update(updateQuery['UPDATE'])
    selectedRows = table.select({'columns': ['*'], 'from': 'a'})
    for row in selectedRows:
        print(f'update: {row}')

    deleteQuery = {'DELETE': {'table': 'a', 'where': [('a', '=', 1), 'or', ('b', '=', 10)]}}
    table.delete(deleteQuery['DELETE'])
    selectedRows = table.select({'columns': ['*'], 'from': 'a'})
    for row in selectedRows:
        print(f'delete: {row}')


if __name__ == '__main__':
    testLexParser()
    testSyntaxParser()
    testCore()
