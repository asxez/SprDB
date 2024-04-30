#!/usr/bin/python3.10.6
# -*- coding: utf-8 -*-
#
# @Time    : 2024/4/24 下午10:11
# @Author  : ASXE

"""
this is a test file.
"""

from parser import parser


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

if __name__ == '__main__':
    testLexParser()
    testSyntaxParser()
