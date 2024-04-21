#!/usr/bin/python3.10.6
# -*- coding: utf-8 -*-
#
# @Time    : 2024/4/20 20:39
# @Author  : ASXE


from enum import Enum


class TokenType(Enum):
    TOKEN_CREATE = 1  # create
    TOKEN_TABLE = 2  # table
    TOKEN_DATABASE = 3  # database
    TOKEN_SELECT = 4  # select
    TOKEN_DELETE = 5  # delete
    TOKEN_FROM = 6  # from
    TOKEN_UPDATE = 7  # update
    TOKEN_INSERT = 8  # insert
    TOKEN_INTO = 9  # into
    TOKEN_VALUES = 10  # values
    TOKEN_WHERE = 11  # where
    TOKEN_SET = 12  # set
    TOKEN_LOGIC_AND = 13  # and &&
    TOKEN_LOGIC_OR = 14  # or ||
    TOKEN_LOGIC_NOT = 15  # not
    TOKEN_MORE = 16  # >
    TOKEN_MORE_EQUAL = 17  # >=
    TOKEN_LESS = 18  # <
    TOKEN_LESS_EQUAL = 19  # <=
    TOKEN_LEFT_PAREN = 20  # (
    TOKEN_RIGHT_PAREN = 21  # )
    TOKEN_DOT = 22  # .
    TOKEN_NULL = 23  # null

    TOKEN_NUM = 24  # 数字类型
    TOKEN_STRING = 25  # 字符串类型
    TOKEN_ID = 26  # 名称


class Token:
    tokenType: TokenType


class KeywordsToken:
    def __init__(self, keyword: str, length: int, token: TokenType):
        self.keyword = keyword
        self.length = length
        self.token = token


keywordsToken: list[KeywordsToken] = [
    KeywordsToken("create", 6, TokenType.TOKEN_CREATE),
    KeywordsToken("table", 5, TokenType.TOKEN_TABLE),
    KeywordsToken("database", 8, TokenType.TOKEN_DATABASE),
    KeywordsToken("select", 6, TokenType.TOKEN_SELECT),
    KeywordsToken("delete", 6, TokenType.TOKEN_DELETE),
    KeywordsToken("from", 4, TokenType.TOKEN_FROM),
    KeywordsToken("update", 6, TokenType.TOKEN_UPDATE),
    KeywordsToken("insert", 6, TokenType.TOKEN_INSERT),
    KeywordsToken("into", 4, TokenType.TOKEN_INTO),
    KeywordsToken("values", 6, TokenType.TOKEN_VALUES),
    KeywordsToken("where", 5, TokenType.TOKEN_WHERE),
    KeywordsToken("set", 3, TokenType.TOKEN_SET),
    KeywordsToken("and", 3, TokenType.TOKEN_LOGIC_AND),
    KeywordsToken("or", 2, TokenType.TOKEN_LOGIC_OR),
    KeywordsToken("not", 3, TokenType.TOKEN_LOGIC_NOT),
    KeywordsToken("null", 4, TokenType.TOKEN_NULL),
]


class Parser:
    curToken: Token  # 当前token
    preToken: Token  # 前一个token
    sourceCode: str  # 源码串
    curChar: str  # 当前字符
