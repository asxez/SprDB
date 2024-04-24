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
    sparser = parser.SyntaxParser("create table a (a int , b str ,)")
    print(sparser.parse())

if __name__ == '__main__':
    testLexParser()
    testSyntaxParser()
