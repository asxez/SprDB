#!/usr/bin/python3.10.6
# -*- coding: utf-8 -*-
#
# @Time    : 2024/4/23 下午2:01
# @Author  : ASXE

import sys

from parser import parser

if __name__ == '__main__':
    print("sprDB >>> ", end='')
    while True:
        statement = input('')
        if statement == 'exit':
            print('Good Bye!')
            sys.exit(0)
        parse = parser.LexParser(statement)
        parse.getNextToken()
        while parse.curToken.tokenType != parser.TokenType.TOKEN_END:
            print((parse.curToken.value, parse.curToken.tokenType, parse.preToken.tokenType))
            parse.getNextToken()
        sparser = parser.SyntaxParser(statement)
        print(sparser.parse())
        print("sprDB >>> ", end='')
