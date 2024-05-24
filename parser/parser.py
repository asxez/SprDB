#!/usr/bin/python3.10.6
# -*- coding: utf-8 -*-
#
# @Time    : 2024/4/20 20:39
# @Author  : ASXE

import lzma
import os
from enum import Enum, auto
from typing import Any, List, Dict, Optional

from common import OutputTable, curdir, Logger
from core import Row
from core.database import createDatabase, useDatabase, Database
from core.table import Table


class TokenType(Enum):
    """枚举token类型"""
    TOKEN_CREATE = auto()  # create
    TOKEN_TABLE = auto()  # table
    TOKEN_DATABASE = auto()  # database
    TOKEN_SELECT = auto()  # select
    TOKEN_DELETE = auto()  # delete
    TOKEN_FROM = auto()  # from
    TOKEN_UPDATE = auto()  # update
    TOKEN_INSERT = auto()  # insert
    TOKEN_INTO = auto()  # into
    TOKEN_VALUES = auto()  # values
    TOKEN_WHERE = auto()  # where
    TOKEN_SET = auto()  # set
    TOKEN_LOGIC_AND = auto()  # and &&
    TOKEN_LOGIC_OR = auto()  # or ||
    TOKEN_LOGIC_NOT = auto()  # not
    TOKEN_IN = auto()  # in
    TOKEN_STR = auto()  # str
    TOKEN_INT = auto()  # int
    TOKEN_FLOAT = auto()  # float
    TOKEN_BOOL = auto()  # bool
    TOKEN_NULL = auto()  # null
    TOKEN_USE = auto()  # use

    TOKEN_MORE = auto()  # >
    TOKEN_MORE_EQUAL = auto()  # >=
    TOKEN_LESS = auto()  # <
    TOKEN_LESS_EQUAL = auto()  # <=
    TOKEN_LEFT_PAREN = auto()  # (
    TOKEN_RIGHT_PAREN = auto()  # )
    TOKEN_DOT = auto()  # .
    TOKEN_COMMA = auto()  # ,
    TOKEN_STAR = auto()  # *
    TOKEN_EQUAL = auto()  # =
    TOKEN_END = auto()  # ;
    TOKEN_QUO = auto()  # '

    TOKEN_NUM = auto()  # 数字类型
    TOKEN_STRING = auto()  # 字符串类型
    TOKEN_ID = auto()  # 名称


class Token:
    """token结构"""

    def __init__(self, tokenType: TokenType):
        self.tokenType: TokenType = tokenType
        self.length: int = 0
        self.value: str = ''


class KeywordsToken:
    """关键字token结构"""

    def __init__(self, keyword: str, tokenType: TokenType):
        self.keyword = keyword  # 关键字
        self.tokenType = tokenType  # 关键字token类型


keywordsToken: List[KeywordsToken] = [
    KeywordsToken("CREATE", TokenType.TOKEN_CREATE),
    KeywordsToken("TABLE", TokenType.TOKEN_TABLE),
    KeywordsToken("DATABASE", TokenType.TOKEN_DATABASE),
    KeywordsToken("SELECT", TokenType.TOKEN_SELECT),
    KeywordsToken("DELETE", TokenType.TOKEN_DELETE),
    KeywordsToken("FROM", TokenType.TOKEN_FROM),
    KeywordsToken("UPDATE", TokenType.TOKEN_UPDATE),
    KeywordsToken("INSERT", TokenType.TOKEN_INSERT),
    KeywordsToken("INTO", TokenType.TOKEN_INTO),
    KeywordsToken("VALUES", TokenType.TOKEN_VALUES),
    KeywordsToken("WHERE", TokenType.TOKEN_WHERE),
    KeywordsToken("SET", TokenType.TOKEN_SET),
    KeywordsToken("AND", TokenType.TOKEN_LOGIC_AND),
    KeywordsToken("OR", TokenType.TOKEN_LOGIC_OR),
    KeywordsToken("NOT", TokenType.TOKEN_LOGIC_NOT),
    KeywordsToken("NULL", TokenType.TOKEN_NULL),
    KeywordsToken("IN", TokenType.TOKEN_IN),
    KeywordsToken("STR", TokenType.TOKEN_STR),
    KeywordsToken("INT", TokenType.TOKEN_INT),
    KeywordsToken("FLOAT", TokenType.TOKEN_FLOAT),
    KeywordsToken("BOOL", TokenType.TOKEN_BOOL),
    KeywordsToken('USE', TokenType.TOKEN_USE),
]


class LexParser:
    """词法分析器"""

    def __init__(self, statement: str, logger: Logger):
        self.logger = logger
        self.logger.info('LexParser initialized')

        self.curToken: Token = Token(TokenType.TOKEN_END)  # 当前token
        self.preToken: Token = Token(TokenType.TOKEN_END)  # 前一个token
        self.__sourceCode: str = statement  # 源码串
        self.__curPosition: int = 0  # 当前所在源码串位置

    def __skipBlanks(self) -> None:
        """跳过空白"""
        while self.__curPosition < len(self.__sourceCode) and self.__sourceCode[self.__curPosition].isspace():
            self.__curPosition += 1

    def __parseAnother(self) -> Optional[str]:
        # 识别关键字或者标识符
        if self.__sourceCode[self.__curPosition].isalpha() or self.__sourceCode[self.__curPosition] == '_':
            identifier = ''
            while self.__curPosition < len(self.__sourceCode) and (
                    self.__sourceCode[self.__curPosition].isalnum() or self.__sourceCode[self.__curPosition] == '_'):
                identifier += self.__sourceCode[self.__curPosition]
                self.__curPosition += 1
            upper = identifier.upper()
            for keywordToken in keywordsToken:
                if keywordToken.keyword.upper() == upper:
                    self.curToken.tokenType = keywordToken.tokenType
                    self.curToken.length = len(identifier)
                    self.curToken.value = identifier
                    break
                self.curToken.tokenType = TokenType.TOKEN_ID
                self.curToken.length = len(identifier)
                self.curToken.value = identifier

        elif self.__sourceCode[self.__curPosition].isdigit():  # 识别数字
            num = ''
            while self.__curPosition < len(self.__sourceCode) and (
                    self.__sourceCode[self.__curPosition].isdigit() or self.__sourceCode[self.__curPosition] == '.'):
                num += self.__sourceCode[self.__curPosition]
                self.__curPosition += 1
            self.curToken.tokenType = TokenType.TOKEN_NUM
            self.curToken.length = len(num)
            self.curToken.value = float(num) if '.' in num else int(num)

        elif self.__sourceCode[self.__curPosition] == "'":  # 识别字符串
            self.__curPosition += 1  # 跳过当前的"'"
            string = ''
            while self.__curPosition < len(self.__sourceCode):
                if self.__sourceCode[self.__curPosition] == "'":
                    if self.__curPosition + 1 < len(self.__sourceCode) and self.__sourceCode[
                        self.__curPosition + 1] == "'":
                        # 此时是一个转义字符
                        string += "'"
                        self.__curPosition += 2
                        continue
                    else:  # 继续读入
                        self.__curPosition += 1
                        break
                string += self.__sourceCode[self.__curPosition]
                self.__curPosition += 1
            else:
                # 命令结束而字符串仍未结果，抛出syntaxError
                self.logger.error("Unterminated string.", 'syntaxError')
                return "Unterminated string."
            self.curToken.tokenType = TokenType.TOKEN_STRING
            self.curToken.length = len(string)
            self.curToken.value = string

        # 数字，字符串，关键字之外的错误类型
        else:
            self.logger.error("An error occurred while parsing the token.", 'typeError')
            return "An error occurred while parsing the token."

    def getNextToken(self) -> None:
        """获取下一个token"""
        self.preToken = self.curToken
        self.__skipBlanks()
        self.curToken = Token(TokenType.TOKEN_END)
        while self.__curPosition < len(self.__sourceCode) and self.__sourceCode[self.__curPosition] != ';':
            match self.__sourceCode[self.__curPosition]:
                case ',':
                    self.curToken.tokenType = TokenType.TOKEN_COMMA
                    self.curToken.length = 1
                    self.curToken.value = ','
                    self.__curPosition += 1
                    break
                case '.':
                    self.curToken.tokenType = TokenType.TOKEN_DOT
                    self.curToken.length = 1
                    self.curToken.value = '.'
                    self.__curPosition += 1
                    break
                case '>':
                    if self.__sourceCode[self.__curPosition + 1] == '=':
                        self.curToken.tokenType = TokenType.TOKEN_MORE_EQUAL
                        self.curToken.length = 2
                        self.curToken.value = '>='
                        self.__curPosition += 2
                    else:
                        self.curToken.tokenType = TokenType.TOKEN_MORE
                        self.curToken.length = 1
                        self.curToken.value = '>'
                        self.__curPosition += 1
                    break
                case '<':
                    if self.__sourceCode[self.__curPosition + 1] == '=':
                        self.curToken.tokenType = TokenType.TOKEN_LESS_EQUAL
                        self.curToken.length = 2
                        self.curToken.value = '<='
                        self.__curPosition += 2
                    else:
                        self.curToken.tokenType = TokenType.TOKEN_LESS
                        self.curToken.length = 1
                        self.curToken.value = '<'
                        self.__curPosition += 1
                    break
                case '(':
                    self.curToken.tokenType = TokenType.TOKEN_LEFT_PAREN
                    self.curToken.length = 1
                    self.curToken.value = '('
                    self.__curPosition += 1
                    break
                case ')':
                    self.curToken.tokenType = TokenType.TOKEN_RIGHT_PAREN
                    self.curToken.length = 1
                    self.curToken.value = ')'
                    self.__curPosition += 1
                    break
                case '*':
                    self.curToken.tokenType = TokenType.TOKEN_STAR
                    self.curToken.length = 1
                    self.curToken.value = '*'
                    self.__curPosition += 1
                    break
                case '=':
                    self.curToken.tokenType = TokenType.TOKEN_EQUAL
                    self.curToken.length = 1
                    self.curToken.value = '='
                    self.__curPosition += 1
                    break
                case ';':
                    self.curToken.tokenType = TokenType.TOKEN_END
                    self.curToken.length = 1
                    self.curToken.value = ';'
                    self.__curPosition += 1
                    break
                case _:
                    self.__parseAnother()
                    break


class SyntaxParser:
    """语法分析器"""

    def __init__(self, statement: str, logger: Logger):
        self.logger = logger
        self.logger.info('SyntaxParser initialized')
        self.__lexParser: LexParser = LexParser(statement, self.logger)

    def parse(self):
        """启动语法分析器"""
        self.logger.info('Starting syntax parse...')
        self.__lexParser.getNextToken()
        if self.__lexParser.curToken.tokenType == TokenType.TOKEN_CREATE:
            return self.__parseCreate()
        elif self.__lexParser.curToken.tokenType == TokenType.TOKEN_SELECT:
            return self.__parseSelect()
        elif self.__lexParser.curToken.tokenType == TokenType.TOKEN_INSERT:
            return self.__parseInsert()
        elif self.__lexParser.curToken.tokenType == TokenType.TOKEN_UPDATE:
            return self.__parseUpdate()
        elif self.__lexParser.curToken.tokenType == TokenType.TOKEN_DELETE:
            return self.__parseDelete()
        elif self.__lexParser.curToken.tokenType == TokenType.TOKEN_USE:
            return self.__parseUse()
        else:
            self.logger.error('Syntax is error.', 'syntaxError')
            return 'Syntax is error.'

    def __parseCreate(self) -> Dict[str, Dict[str, Any]] | str:
        """解析create命令"""
        self.__lexParser.getNextToken()  # 跳过create
        curToken = self.__lexParser.curToken
        if curToken.tokenType != TokenType.TOKEN_TABLE and curToken.tokenType != TokenType.TOKEN_DATABASE:
            self.logger.error(f'Expect "table" or "database" after "{self.__lexParser.preToken.value}".', 'syntaxError')
            return f'Expect "table" or "database" after "{self.__lexParser.preToken.value}".'

        # create database [databaseName]
        if curToken.tokenType == TokenType.TOKEN_DATABASE:
            self.__lexParser.getNextToken()
            return {
                "CREATE_DATABASE": {
                    "databaseName": self.__lexParser.curToken.value,
                }
            }

        # create table ...
        if curToken.tokenType == TokenType.TOKEN_TABLE:
            syntaxTreeTable = {
                "CREATE_TABLE": {
                    "tableName": "",  # 表名
                    "columns": []  # 列名列表
                }
            }

            self.__lexParser.getNextToken()
            if self.__lexParser.curToken.tokenType != TokenType.TOKEN_ID:  # 未定义表名，抛出syntaxError
                self.logger.error(f'Expect table name after "{self.__lexParser.preToken.value}".', 'syntaxError')
                return f'Expect table name after "{self.__lexParser.preToken.value}".'
            syntaxTreeTable['CREATE_TABLE']['tableName'] = self.__lexParser.curToken.value

            self.__lexParser.getNextToken()
            if self.__lexParser.curToken.tokenType != TokenType.TOKEN_LEFT_PAREN:
                self.logger.error(f'Expected "(" after "{self.__lexParser.preToken.value}".', 'syntaxError')
                return f'Expected "(" after "{self.__lexParser.preToken.value}".'

            # 死循环读入表列及列类型
            while True:
                self.__lexParser.getNextToken()
                if self.__lexParser.curToken.tokenType == TokenType.TOKEN_RIGHT_PAREN:
                    break

                # 取得列名
                if self.__lexParser.curToken.tokenType != TokenType.TOKEN_ID:
                    self.logger.error(f'Expected column name but it is "{self.__lexParser.curToken.value}".',
                                      'syntaxError')
                    return f'Expected column name but it is "{self.__lexParser.curToken.value}".'
                column_name = self.__lexParser.curToken.value

                # 取得列类型
                self.__lexParser.getNextToken()
                token = self.__lexParser.curToken
                if token.tokenType != TokenType.TOKEN_INT and token.tokenType != TokenType.TOKEN_STR and token.tokenType != TokenType.TOKEN_FLOAT:
                    self.logger.error(f'Expected data type for column but it is "{self.__lexParser.curToken.value}".',
                                      'syntaxError')
                    return f'Expected data type for column but it is "{self.__lexParser.curToken.value}".'
                data_type = self.__lexParser.curToken.value

                syntaxTreeTable['CREATE_TABLE']['columns'].append((column_name, data_type))

                self.__lexParser.getNextToken()
                if self.__lexParser.curToken.tokenType == TokenType.TOKEN_COMMA:  # 后面还有列，继续
                    continue
                elif self.__lexParser.curToken.tokenType == TokenType.TOKEN_RIGHT_PAREN:  # 结束
                    break
                else:
                    self.logger.error(f'unexpected token:{self.__lexParser.curToken.value}.', 'syntaxError')
                    return f'Unexpected token:{self.__lexParser.curToken.value}.'

            # 不允许空列
            if not syntaxTreeTable['CREATE_TABLE']['columns']:
                self.logger.error('Empty column definition.', 'syntaxError')
                return 'Empty column definition.'

            return syntaxTreeTable

    def __parseWhere(self):
        """解析WHERE子句"""
        self.__lexParser.getNextToken()  # 跳过WHERE
        where = self.__parseExpression()
        return where

    def __parseExpression(self):
        """解析表达式"""
        expression = []
        while True:
            if self.__lexParser.curToken.tokenType != TokenType.TOKEN_LEFT_PAREN:
                column = self.__lexParser.curToken.value

                # 解析操作符
                self.__lexParser.getNextToken()
                curToken = self.__lexParser.curToken
                if curToken.tokenType not in [TokenType.TOKEN_EQUAL, TokenType.TOKEN_MORE, TokenType.TOKEN_MORE_EQUAL,
                                              TokenType.TOKEN_LESS, TokenType.TOKEN_LESS_EQUAL]:
                    self.logger.error(f'Expect comparison operator after "{self.__lexParser.preToken.value}".',
                                      'syntaxError')
                    return f'Expect comparison operator after "{self.__lexParser.preToken.value}".'
                operator = curToken.value

                # 解析值
                self.__lexParser.getNextToken()
                curToken = self.__lexParser.curToken
                if curToken.tokenType != TokenType.TOKEN_STRING and curToken.tokenType != TokenType.TOKEN_NUM:
                    self.logger.error(f'Expect value type string or number after "{self.__lexParser.preToken.value}".',
                                      'typeError')
                    return f'Expect value type string or number after "{self.__lexParser.preToken.value}".'
                value = curToken.value
                expression.append((column, operator, value))

                self.__lexParser.getNextToken()
            else:
                # 遇到左括号，递归解析括号内的表达式
                self.__lexParser.getNextToken()  # 跳过左括号
                sub_expression = self.__parseExpression()
                expression.append(sub_expression)

            # 判断是否继续解析下一个条件
            if self.__lexParser.curToken.tokenType != TokenType.TOKEN_LOGIC_AND and self.__lexParser.curToken.tokenType != TokenType.TOKEN_LOGIC_OR:
                break

            # 解析逻辑运算符
            logical_operator = self.__lexParser.curToken.value
            expression.append(logical_operator)
            self.__lexParser.getNextToken()

        # 在这里，检查是否遇到右括号或者是 WHERE 子句的结束
        if self.__lexParser.curToken.tokenType == TokenType.TOKEN_RIGHT_PAREN:
            self.__lexParser.getNextToken()  # 跳过右括号
            return expression  # 返回括号内的表达式
        elif self.__lexParser.curToken.tokenType == TokenType.TOKEN_END:
            return expression  # 返回整个表达式
        else:
            self.logger.error(f'Unexpected token after expression:{self.__lexParser.curToken.value}', 'syntaxError')
            return f'Unexpected token after expression:{self.__lexParser.curToken.value}'

    def __parseSelect(self) -> Dict[str, Dict[str, Any]] | str:
        """解析select命令"""
        self.__lexParser.getNextToken()  # 跳过select
        curToken = self.__lexParser.curToken
        if curToken.tokenType != TokenType.TOKEN_ID and curToken.tokenType != TokenType.TOKEN_STAR:
            self.logger.error(f'Expect "*" or column name after {self.__lexParser.preToken.value}.', 'syntaxError')
            return f'Expect "*" or column name after {self.__lexParser.preToken.value}.'

        columns = []
        if curToken.tokenType == TokenType.TOKEN_STAR:
            columns.append('*')
            self.__lexParser.getNextToken()
        else:  # 解析列名列表
            while True:
                columns.append(self.__lexParser.curToken.value)
                self.__lexParser.getNextToken()  # 此处，若后面已经不是逗号，则列名已解析完成，目前应该读到from（这句执行后）
                if self.__lexParser.curToken.tokenType != TokenType.TOKEN_COMMA:
                    break
                self.__lexParser.getNextToken()
                if self.__lexParser.curToken.tokenType != TokenType.TOKEN_ID:
                    self.logger.error('Expect column name after ",".', 'syntaxError')
                    return 'Expect column name after ",".'

        syntaxTree = {
            "SELECT": {
                "columns": columns,  # 列名列表
                "from": "",  # 表名
                "where": [],  # WHERE 子句的条件表达式
            }
        }

        # 解析from
        if self.__lexParser.curToken.tokenType != TokenType.TOKEN_FROM:
            self.logger.error('Expect "from" after column list.', 'syntaxError')
            return 'Expect "from" after column list.'

        self.__lexParser.getNextToken()
        if self.__lexParser.curToken.tokenType != TokenType.TOKEN_ID:
            self.logger.error(f'Expect table name after "{self.__lexParser.preToken.value}".', 'syntaxError')
            return f'Expect table name after "{self.__lexParser.preToken.value}".'

        syntaxTree['SELECT']['from'] = self.__lexParser.curToken.value  # 表名

        # 解析where子句
        self.__lexParser.getNextToken()
        if self.__lexParser.curToken.tokenType != TokenType.TOKEN_WHERE:
            return syntaxTree
        syntaxTree['SELECT']['where'] = self.__parseWhere()

        return syntaxTree

    def __parseInsert(self) -> Dict[str, Dict[str, Any]] | str:
        """解析insert命令"""
        self.__lexParser.getNextToken()  # 跳过insert
        if self.__lexParser.curToken.tokenType != TokenType.TOKEN_INTO:
            self.logger.error(f'Expect "into" after "{self.__lexParser.preToken.value}".', 'syntaxError')
            return f'Expect "into" after "{self.__lexParser.preToken.value}".'

        self.__lexParser.getNextToken()
        if self.__lexParser.curToken.tokenType != TokenType.TOKEN_ID:
            self.logger.error(f'Expect table name after "{self.__lexParser.preToken.value}".', 'syntaxError')
            return f'Expect table name after "{self.__lexParser.preToken.value}".'

        syntaxTree = {
            "INSERT": {
                "table": self.__lexParser.curToken.value,  # 目标数据表
                "columns": [],  # 插入的列名列表
                "values": []  # 插入的值列表，每个值列表对应一行数据
            }
        }

        self.__lexParser.getNextToken()
        if self.__lexParser.curToken.tokenType == TokenType.TOKEN_VALUES:  # 为所有列添加
            syntaxTree['INSERT']['columns'].append('*')

            self.__lexParser.getNextToken()  # 跳过values
            if self.__lexParser.curToken.tokenType != TokenType.TOKEN_LEFT_PAREN:
                self.logger.error(f'Expect "(" after "{self.__lexParser.preToken.value}".', 'syntaxError')
                return f'Expect "(" after "{self.__lexParser.preToken.value}".'
            while True:
                syntaxTree['INSERT']['values'].append(self.__parseValues())

                self.__lexParser.getNextToken()  # 跳过右括号
                if self.__lexParser.curToken.tokenType == TokenType.TOKEN_COMMA:
                    self.__lexParser.getNextToken()  # 跳过逗号
                    continue
                elif self.__lexParser.curToken.tokenType == TokenType.TOKEN_END:
                    break
                else:
                    self.logger.error(f'Unexpect token:{self.__lexParser.curToken.value}.', 'syntaxError')
                    return f'Unexpect token:{self.__lexParser.curToken.value}.'

            return syntaxTree

        if self.__lexParser.curToken.tokenType == TokenType.TOKEN_LEFT_PAREN:
            self.__lexParser.getNextToken()  # 跳过左括号
            while True:
                if self.__lexParser.curToken.tokenType != TokenType.TOKEN_ID:
                    self.logger.error('Expect column after "(".', 'syntaxError')
                    return 'Expect column after "(".'
                syntaxTree['INSERT']['columns'].append(self.__lexParser.curToken.value)
                self.__lexParser.getNextToken()
                if self.__lexParser.curToken.tokenType == TokenType.TOKEN_COMMA:
                    self.__lexParser.getNextToken()  # 跳过逗号
                    continue
                elif self.__lexParser.curToken.tokenType == TokenType.TOKEN_RIGHT_PAREN:
                    break
                else:
                    self.logger.error(f'Unexpect token:{self.__lexParser.curToken.value}.', 'syntaxError')
                    return f'Unexpect token:{self.__lexParser.curToken.value}.'

            self.__lexParser.getNextToken()  # 获取values
            if self.__lexParser.curToken.tokenType != TokenType.TOKEN_VALUES:
                self.logger.error('Expect "values" after columns list.', 'syntaxError')
                return 'Expect "values" after columns list.'

            self.__lexParser.getNextToken()  # 跳过values
            if self.__lexParser.curToken.tokenType != TokenType.TOKEN_LEFT_PAREN:
                self.logger.error(f'Expect "(" after "{self.__lexParser.preToken.value}".', 'syntaxError')
                return f'Expect "(" after "{self.__lexParser.preToken.value}".'
            while True:
                syntaxTree['INSERT']['values'].append(self.__parseValues())

                self.__lexParser.getNextToken()  # 跳过右括号
                if self.__lexParser.curToken.tokenType == TokenType.TOKEN_COMMA:
                    self.__lexParser.getNextToken()  # 跳过逗号
                    continue
                elif self.__lexParser.curToken.tokenType == TokenType.TOKEN_END:
                    break
                else:
                    self.logger.error(f'Unexpect token:{self.__lexParser.curToken.value}.', 'syntaxError')
                    return f'Unexpect token:{self.__lexParser.curToken.value}.'

            return syntaxTree

    def __parseValues(self):
        if self.__lexParser.curToken.tokenType != TokenType.TOKEN_LEFT_PAREN:
            self.logger.error(f'Unexpect token:{self.__lexParser.curToken.value}.', 'syntaxError')
            return f'Unexpect token:{self.__lexParser.curToken.value}.'

        self.__lexParser.getNextToken()  # 跳过左括号
        values = []
        while True:
            if self.__lexParser.curToken.tokenType != TokenType.TOKEN_NUM and self.__lexParser.curToken.tokenType != TokenType.TOKEN_STRING:
                self.logger.error(f'Unexpect type:{self.__lexParser.curToken.value}.', 'typeError')
                return f'Unexpect type:{self.__lexParser.curToken.value}.'
            values.append(self.__lexParser.curToken.value)

            self.__lexParser.getNextToken()  # 跳过当前值，准备获取下一个
            if self.__lexParser.curToken.tokenType == TokenType.TOKEN_COMMA:
                self.__lexParser.getNextToken()  # 跳过逗号
                continue
            elif self.__lexParser.curToken.tokenType == TokenType.TOKEN_RIGHT_PAREN:
                break
            else:
                self.logger.error(f'Unexpect token:{self.__lexParser.curToken.value}.', 'syntaxError')
                return f'Unexpect token:{self.__lexParser.curToken.value}.'

        return values

    def __parseUpdate(self) -> Dict[str, Dict[str, str | List]] | str:
        """解析update命令"""
        self.__lexParser.getNextToken()  # 跳过update
        if self.__lexParser.curToken.tokenType != TokenType.TOKEN_ID:
            self.logger.error(f'Expect table name after "{self.__lexParser.preToken.value}".', 'syntaxError')
            return f'Expect table name after "{self.__lexParser.preToken.value}".'

        syntaxTree = {
            "UPDATE": {
                "table": "",  # 目标数据表
                "set": [],  # SET 子句中的更新值
                "where": []  # WHERE 子句的条件表达式
            }
        }
        syntaxTree['UPDATE']['table'] = self.__lexParser.curToken.value

        self.__lexParser.getNextToken()  # set
        if self.__lexParser.curToken.tokenType != TokenType.TOKEN_SET:
            self.logger.error('Expect "set" after table name.', 'syntaxError')
            return 'Expect "set" after table name.'

        self.__lexParser.getNextToken()  # 跳过set，后面应该是column name
        while True:
            if self.__lexParser.curToken.tokenType != TokenType.TOKEN_ID:
                self.logger.error('Expect column name.', 'syntaxError')
                return 'Expect column name.'
            column = self.__lexParser.curToken.value

            self.__lexParser.getNextToken()
            if self.__lexParser.curToken.tokenType != TokenType.TOKEN_EQUAL:
                self.logger.error('Expect "=" after column name.', 'syntaxError')
                return 'Expect "=" after column name.'

            self.__lexParser.getNextToken()
            if self.__lexParser.curToken.tokenType != TokenType.TOKEN_NUM and self.__lexParser.curToken.tokenType != TokenType.TOKEN_STRING:
                self.logger.error(f'Unexpect value type:{self.__lexParser.curToken.value}.', 'typeError')
                return f'Unexpect value type:{self.__lexParser.curToken.value}.'
            value = self.__lexParser.curToken.value
            syntaxTree['UPDATE']['set'].append((column, value))

            self.__lexParser.getNextToken()
            if self.__lexParser.curToken.tokenType == TokenType.TOKEN_COMMA:
                self.__lexParser.getNextToken()  # 跳过逗号，便于下次循环
                continue
            elif self.__lexParser.curToken.tokenType == TokenType.TOKEN_WHERE or self.__lexParser.curToken.tokenType == TokenType.TOKEN_END:
                break
            else:
                self.logger.error(f'Unexpect token:{self.__lexParser.curToken.value}.', 'syntaxError')
                return f'Unexpect token:{self.__lexParser.curToken.value}.'

                # 解析where子句
        if self.__lexParser.curToken.tokenType == TokenType.TOKEN_WHERE:
            syntaxTree['UPDATE']['where'] = self.__parseWhere()

        return syntaxTree

    def __parseDelete(self) -> Dict[str, Dict[str, str | List]] | str:
        """解析delete命令"""
        self.__lexParser.getNextToken()  # 跳过delete
        if self.__lexParser.curToken.tokenType != TokenType.TOKEN_FROM:
            self.logger.error(f'Expect "from" after "{self.__lexParser.preToken.value}".', 'syntaxError')
            return f'Expect "from" after "{self.__lexParser.preToken.value}".'

        self.__lexParser.getNextToken()
        if self.__lexParser.curToken.tokenType != TokenType.TOKEN_ID:
            self.logger.error(f'Expect table name after "{self.__lexParser.preToken.value}".', 'syntaxError')
            return f'Expect table name after "{self.__lexParser.preToken.value}".'

        syntaxTree = {
            "DELETE": {
                "table": self.__lexParser.curToken.value,  # 目标数据表
                "where": []  # WHERE 子句的条件表达式
            }
        }

        self.__lexParser.getNextToken()
        if self.__lexParser.curToken.tokenType == TokenType.TOKEN_WHERE:
            syntaxTree['DELETE']['where'] = self.__parseWhere()

        return syntaxTree

    def __parseUse(self) -> Dict[str, Dict[str, str]] | str:
        """解析use命令"""
        self.__lexParser.getNextToken()  # 跳过use
        if self.__lexParser.curToken.tokenType != TokenType.TOKEN_ID:
            self.logger.error(f'Expect database name after "{self.__lexParser.preToken.value}".', 'syntaxError')
            return f'Expect database name after "{self.__lexParser.preToken.value}".'
        return {
            'USE': {
                'databaseName': self.__lexParser.curToken.value
            }
        }


if not os.path.exists(f'{curdir}/data/sprdb'):
    createDatabase('sprdb')
thisDatabase: Database = Database('sprdb')  # 默认


class SemanticParser:
    """语义分析器"""

    def __init__(self, logger: Logger):
        self.logger = logger
        logger.info('SemanticParser initialized')

    @staticmethod
    def writeNewData(tableName: str, table: Table) -> None:
        """为表写入新数据"""
        with lzma.open(f'{curdir}/data/{thisDatabase.name}/{tableName}.db', 'wb') as file:
            data = table.compress(table.serialized())
            file.write(data)

    def exists(self, path: str):
        if not os.path.exists(path):
            self.logger.error(f'There is no such {path}.', 'pathNotExists')
            return f'There is no such {path}.'

    def main(self, syntax: Dict[str, Dict], mode=0) -> List[Row | Dict] | None | str:
        """入口"""
        global thisDatabase
        if 'CREATE_DATABASE' in syntax:  # 创建数据库
            dbInfo = syntax['CREATE_DATABASE']
            result = createDatabase(dbInfo['databaseName'])
            thisDatabase = Database(dbInfo['databaseName'])
            return result

        elif 'CREATE_TABLE' in syntax:  # 创建表
            tableInfo = syntax['CREATE_TABLE']
            result = thisDatabase.createTable(tableInfo['tableName'], tableInfo['columns'])
            return result

        elif 'DROP_DATABASE' in syntax:
            ...

        elif 'DROP_TABLE' in syntax:
            ...

        elif 'USE' in syntax:  # 切换数据库
            thisDatabase = useDatabase(syntax['USE']['databaseName'], self.logger)
            if isinstance(thisDatabase, str):
                return thisDatabase

        elif 'INSERT' in syntax:  # 插入数据
            insertInfo = syntax['INSERT']
            tableName = insertInfo['table']
            values = insertInfo['values']
            columns = insertInfo['columns']
            table = Table(tableName)

            if not os.path.exists(f'{curdir}/data/{thisDatabase.name}/{tableName}.db'):
                self.logger.error('There is no such table.', 'pathNotExists')
                return 'There is no such table.'

            with lzma.open(f'{curdir}/data/{thisDatabase.name}/{tableName}.db', 'rb') as file:
                data = file.read()
                data = table.decompress(data)

            table.deserialized(data)
            result = table.insert(columns, values)
            self.writeNewData(tableName, table)
            return result

        elif 'SELECT' in syntax:  # 查询
            selectInfo = syntax['SELECT']
            tableName = selectInfo['from']
            table = Table(tableName)

            if not os.path.exists(f'{curdir}/data/{thisDatabase.name}/{tableName}.db'):
                self.logger.error('There is no such table.', 'tableNotExists')
                return 'There is no such table.'

            with lzma.open(f'{curdir}/data/{thisDatabase.name}/{tableName}.db', 'rb') as file:
                data = file.read()
                data = table.decompress(data)

            table.deserialized(data)
            rows = table.select(selectInfo)
            if mode != 0:
                return rows
            try:
                output = OutputTable(rows)
            except:
                return 'No data.'
            print(output)

        elif 'UPDATE' in syntax:  # 更新
            updateInfo = syntax['UPDATE']
            tableName = updateInfo['table']
            table = Table(tableName)

            if not os.path.exists(f'{curdir}/data/{thisDatabase.name}/{tableName}.db'):
                self.logger.error('There is no such table.', 'pathNotExists')
                return 'There is no such table.'

            with lzma.open(f'{curdir}/data/{thisDatabase.name}/{tableName}.db', 'rb') as file:
                data = file.read()
                data = table.decompress(data)

            table.deserialized(data)
            table.update(updateInfo)
            self.writeNewData(tableName, table)

        elif 'DELETE' in syntax:  # 删除
            deleteInfo = syntax['DELETE']
            tableName = deleteInfo['table']
            table = Table(tableName)

            if not os.path.exists(f'{curdir}/data/{thisDatabase.name}/{tableName}.db'):
                self.logger.error('There is no such table.', 'pathNotExists')
                return 'There is no such table.'

            with lzma.open(f'{curdir}/data/{thisDatabase.name}/{tableName}.db', 'rb') as file:
                data = file.read()
                data = table.decompress(data)

            table.deserialized(data)
            table.delete(deleteInfo)

            self.writeNewData(tableName, table)

        else:
            self.logger.error('There is no such command.', 'syntaxError')
            return 'There is no such command.'
