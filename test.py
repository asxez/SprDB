#!/usr/bin/python3.10.6
# -*- coding: utf-8 -*-
#
# @Time    : 2024/4/24 下午10:11
# @Author  : ASXE

"""
this is a test file.
"""

from common import log
from core import Table
from parser import parser


def testLog():
    """测试日志输出"""
    log.warning('test warning')
    log.info('test info')
    log.error('test error', 'test')


def testLexParser():
    """测试词法分析器"""
    codes = ["create database a", "create table a (a int , b str ,)",
             "select a,b from t where (c='asxe' or d=1) and e=10",
             "insert into t values (1,2,3), (2,3,4)",
             "update t set a=1,b=2 where c='6'",
             "delete from t where a=1",
             "use test"
             ]
    for code in codes:
        lexParser = parser.LexParser(code)
        lexParser.getNextToken()
        while lexParser.curToken.tokenType != parser.TokenType.TOKEN_END:
            print((lexParser.curToken.value, lexParser.curToken.tokenType, lexParser.preToken.tokenType))
            lexParser.getNextToken()
        print()


def testSyntaxParser():
    """测试语法分析器"""
    sparser = parser.SyntaxParser("create database a")
    print(sparser.parse())
    sparser = parser.SyntaxParser("create table a (a int , b str ,)")
    print(sparser.parse())
    sparser = parser.SyntaxParser("select a,b from t where (c='asxe' or d=1) and e=10")
    print(sparser.parse())
    sparser = parser.SyntaxParser("insert into t values (1,2,3), (2,3,4)")
    print(sparser.parse())
    sparser = parser.SyntaxParser("update t set a=1,b=2 where c='6'")
    print(sparser.parse())
    sparser = parser.SyntaxParser("delete from t where a=1")
    print(sparser.parse())
    sparser = parser.SyntaxParser('use test')
    print(sparser.parse())


def testCore():
    """测试内核"""
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
    testLog()
    testLexParser()
    testSyntaxParser()
    testCore()
