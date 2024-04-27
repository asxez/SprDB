#!/usr/bin/python3.10.6
# -*- coding: utf-8 -*-
#
# @Time    : 2024/4/20 20:39
# @Author  : ASXE


from enum import Enum, auto
from typing import Any

from common import log


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

    def __init__(self, keyword: str, length: int, tokenType: TokenType):
        self.keyword = keyword  # 关键字
        self.length = length  # 关键字长度
        self.tokenType = tokenType  # 关键字token类型


keywordsToken: list[KeywordsToken] = [
    KeywordsToken("CREATE", 6, TokenType.TOKEN_CREATE),
    KeywordsToken("TABLE", 5, TokenType.TOKEN_TABLE),
    KeywordsToken("DATABASE", 8, TokenType.TOKEN_DATABASE),
    KeywordsToken("SELECT", 6, TokenType.TOKEN_SELECT),
    KeywordsToken("DELETE", 6, TokenType.TOKEN_DELETE),
    KeywordsToken("FROM", 4, TokenType.TOKEN_FROM),
    KeywordsToken("UPDATE", 6, TokenType.TOKEN_UPDATE),
    KeywordsToken("INSERT", 6, TokenType.TOKEN_INSERT),
    KeywordsToken("INTO", 4, TokenType.TOKEN_INTO),
    KeywordsToken("VALUES", 6, TokenType.TOKEN_VALUES),
    KeywordsToken("WHERE", 5, TokenType.TOKEN_WHERE),
    KeywordsToken("SET", 3, TokenType.TOKEN_SET),
    KeywordsToken("AND", 3, TokenType.TOKEN_LOGIC_AND),
    KeywordsToken("OR", 2, TokenType.TOKEN_LOGIC_OR),
    KeywordsToken("NOT", 3, TokenType.TOKEN_LOGIC_NOT),
    KeywordsToken("NULL", 4, TokenType.TOKEN_NULL),
    KeywordsToken("IN", 2, TokenType.TOKEN_IN),
    KeywordsToken("STR", 3, TokenType.TOKEN_STR),
    KeywordsToken("INT", 3, TokenType.TOKEN_INT),
    KeywordsToken("FLOAT", 5, TokenType.TOKEN_FLOAT),
    KeywordsToken("BOOL", 4, TokenType.TOKEN_BOOL),
]


class LexParser:
    """词法分析器"""

    def __init__(self, statement: str):
        self.curToken: Token = Token(TokenType.TOKEN_END)  # 当前token
        self.preToken: Token = Token(TokenType.TOKEN_END)  # 前一个token
        self.__sourceCode: str = statement  # 源码串
        self.__curPosition: int = 0  # 当前所在源码串位置

    def __skipBlanks(self) -> None:
        """跳过空白"""
        while self.__curPosition < len(self.__sourceCode) and self.__sourceCode[self.__curPosition].isspace():
            self.__curPosition += 1

    def __parseAnother(self) -> None:
        # 识别关键字或者标识符
        if self.__sourceCode[self.__curPosition].isalpha() or self.__sourceCode[self.__curPosition] == '_':
            identifier = ''
            while self.__curPosition < len(self.__sourceCode) and (
                    self.__sourceCode[self.__curPosition].isalnum() or self.__sourceCode[self.__curPosition] == '_'):
                identifier += self.__sourceCode[self.__curPosition]
                self.__curPosition += 1
            for keywordToken in keywordsToken:
                if keywordToken.keyword.upper() == identifier.upper():
                    self.curToken.tokenType = keywordToken.tokenType
                    self.curToken.length = keywordToken.length
                    self.curToken.value = keywordToken.keyword
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
            self.curToken.value = num

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
                # 命令结束而字符串仍未结果，抛出syntax error
                log.error("Unterminated string.", 'syntax error')
            self.curToken.tokenType = TokenType.TOKEN_STRING
            self.curToken.length = len(string)
            self.curToken.value = string

        # 数字，字符串，关键字之外的错误类型
        else:
            log.error(f"an error occurred while parsing the token.", 'type error')

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

    def __init__(self, statement: str):
        self.__lexParser: LexParser = LexParser(statement)

    def parse(self):
        """启动语法分析器"""
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
        else:
            log.error('syntax is error.', 'syntax error')

    def __parseCreate(self) -> dict[str, dict[str, Any]]:
        """解析create命令"""
        self.__lexParser.getNextToken()  # 跳过create
        curToken = self.__lexParser.curToken
        if curToken.tokenType != TokenType.TOKEN_TABLE and curToken.tokenType != TokenType.TOKEN_DATABASE:
            log.error('expect "table" or "database" after "create".', 'syntax error')

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
                    "tableName": "",
                    "columns": []
                }
            }

            self.__lexParser.getNextToken()
            if self.__lexParser.curToken.tokenType != TokenType.TOKEN_ID:  # 未定义表名，抛出syntax error
                log.error('expect table name after "TABLE".', 'syntax error')
            syntaxTreeTable['CREATE_TABLE']['tableName'] = self.__lexParser.curToken.value

            self.__lexParser.getNextToken()
            if self.__lexParser.curToken.tokenType != TokenType.TOKEN_LEFT_PAREN:
                log.error('expected "(" after table name.', 'syntax error')

            # 死循环读入表列及列类型
            while True:
                self.__lexParser.getNextToken()
                if self.__lexParser.curToken.tokenType == TokenType.TOKEN_RIGHT_PAREN:
                    break

                # 取得列名
                if self.__lexParser.curToken.tokenType != TokenType.TOKEN_ID:
                    log.error('expected column name.', 'syntax error')
                column_name = self.__lexParser.curToken.value

                # 取得列类型
                self.__lexParser.getNextToken()
                token = self.__lexParser.curToken
                if token.tokenType != TokenType.TOKEN_INT and token.tokenType != TokenType.TOKEN_STR and token.tokenType != TokenType.TOKEN_FLOAT:
                    log.error('expected data type for column.', 'syntax error')
                data_type = self.__lexParser.curToken.value

                syntaxTreeTable['CREATE_TABLE']['columns'].append((column_name, data_type))

                self.__lexParser.getNextToken()
                if self.__lexParser.curToken.tokenType == TokenType.TOKEN_COMMA:  # 后面还有列，继续
                    continue
                elif self.__lexParser.curToken.tokenType == TokenType.TOKEN_RIGHT_PAREN:  # 结束
                    break
                else:
                    log.error('unexpected token.', 'syntax error')

            # 不允许空列
            if not syntaxTreeTable['CREATE_TABLE']['columns']:
                log.error('empty column definition.', 'syntax error')

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
                    log.error('expect comparison operator after column name.', 'syntax error')
                operator = curToken.value

                # 解析值
                self.__lexParser.getNextToken()
                curToken = self.__lexParser.curToken
                if curToken.tokenType != TokenType.TOKEN_STRING and curToken.tokenType != TokenType.TOKEN_NUM:
                    log.error('expect value type string or number after comparison operator.', 'type error')
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
            log.error('syntax error: unexpected token after expression.', 'syntax error')

    def __parseSelect(self) -> dict[str, dict[str, Any]]:
        """解析select命令"""
        self.__lexParser.getNextToken()  # 跳过select
        curToken = self.__lexParser.curToken
        if curToken.tokenType != TokenType.TOKEN_ID and curToken.tokenType != TokenType.TOKEN_STAR:
            log.error('expect "*" or column name after select.', 'syntax error')

        columns = []
        if curToken.tokenType == TokenType.TOKEN_STAR:
            columns.append('*')
        else:  # 解析列名列表
            while True:
                columns.append(self.__lexParser.curToken.value)
                self.__lexParser.getNextToken()  # 此处，若后面已经不是逗号，则列名已解析完成，目前已经读到from
                if self.__lexParser.curToken.tokenType != TokenType.TOKEN_COMMA:
                    break
                self.__lexParser.getNextToken()
                if self.__lexParser.curToken.tokenType != TokenType.TOKEN_ID:
                    log.error('expect column name after ",".', 'syntax error')

        syntaxTree = {
            "SELECT": {
                "columns": columns,  # 列名列表
                "from": "",  # 表名
                "where": [],  # WHERE 子句的条件表达式
            }
        }

        # 解析from
        if self.__lexParser.curToken.tokenType != TokenType.TOKEN_FROM:
            log.error('expect "from" after column list.', 'syntax error')

        self.__lexParser.getNextToken()
        if self.__lexParser.curToken.tokenType != TokenType.TOKEN_ID:
            log.error('expect table name after "from".', 'syntax error')

        syntaxTree['SELECT']['from'] = self.__lexParser.curToken.value  # 表名

        # 解析where子句
        self.__lexParser.getNextToken()
        if self.__lexParser.curToken.tokenType != TokenType.TOKEN_WHERE:
            return syntaxTree
        syntaxTree['SELECT']['where'] = self.__parseWhere()

        return syntaxTree

    def __parseInsert(self) -> dict[str, dict[str, Any]]:
        self.__lexParser.getNextToken()  # 跳过insert
        if self.__lexParser.curToken.tokenType != TokenType.TOKEN_INTO:
            log.error('expect "into" after "insert".', 'syntax error')

        self.__lexParser.getNextToken()
        if self.__lexParser.curToken.tokenType != TokenType.TOKEN_ID:
            log.error('expect table name after "insert into".', 'syntax error')

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
                log.error('expect "(" after "values".', 'syntax error')
            while True:
                syntaxTree['INSERT']['values'].append(self.__parseValues())

                self.__lexParser.getNextToken()  # 跳过右括号
                if self.__lexParser.curToken.tokenType == TokenType.TOKEN_COMMA:
                    self.__lexParser.getNextToken()  # 跳过逗号
                    continue
                elif self.__lexParser.curToken.tokenType == TokenType.TOKEN_END:
                    break
                else:
                    log.error('unexpect token', 'syntax error')

            return syntaxTree

        if self.__lexParser.curToken.tokenType == TokenType.TOKEN_LEFT_PAREN:
            self.__lexParser.getNextToken()  # 跳过左括号
            while True:
                if self.__lexParser.curToken.tokenType != TokenType.TOKEN_ID:
                    log.error('expect column after "(".', 'syntax error')
                syntaxTree['INSERT']['columns'].append(self.__lexParser.curToken.value)
                self.__lexParser.getNextToken()
                if self.__lexParser.curToken.tokenType == TokenType.TOKEN_COMMA:
                    self.__lexParser.getNextToken()  # 跳过逗号
                    continue
                elif self.__lexParser.curToken.tokenType == TokenType.TOKEN_RIGHT_PAREN:
                    break
                else:
                    log.error('unexpect token', 'syntax error')

            self.__lexParser.getNextToken()  # 获取values
            if self.__lexParser.curToken.tokenType != TokenType.TOKEN_VALUES:
                log.error('expect "values" after columns list.', 'syntax error')

            self.__lexParser.getNextToken()  # 跳过values
            if self.__lexParser.curToken.tokenType != TokenType.TOKEN_LEFT_PAREN:
                log.error('expect "(" after "values".', 'syntax error')
            while True:
                syntaxTree['INSERT']['values'].append(self.__parseValues())

                self.__lexParser.getNextToken()  # 跳过右括号
                if self.__lexParser.curToken.tokenType == TokenType.TOKEN_COMMA:
                    self.__lexParser.getNextToken()  # 跳过逗号
                    continue
                elif self.__lexParser.curToken.tokenType == TokenType.TOKEN_END:
                    break
                else:
                    log.error('unexpect token', 'syntax error')

            return syntaxTree

    def __parseValues(self):
        if self.__lexParser.curToken.tokenType != TokenType.TOKEN_LEFT_PAREN:
            log.error('unexpect token".', 'syntax error')

        self.__lexParser.getNextToken()  # 跳过左括号
        values = []
        while True:
            if self.__lexParser.curToken.tokenType != TokenType.TOKEN_NUM and self.__lexParser.curToken.tokenType != TokenType.TOKEN_STRING:
                log.error('unexpect type.', 'type error')
            values.append(self.__lexParser.curToken.value)

            self.__lexParser.getNextToken()  # 跳过当前值，准备获取下一个
            if self.__lexParser.curToken.tokenType == TokenType.TOKEN_COMMA:
                self.__lexParser.getNextToken()  # 跳过逗号
                continue
            elif self.__lexParser.curToken.tokenType == TokenType.TOKEN_RIGHT_PAREN:
                break
            else:
                log.error('unexpect token.', 'syntax error')

        return values

    def __parseUpdate(self):
        ...

    def __parseDelete(self):
        ...


if __name__ == '__main__':
    # parser = LexParser("insert into a values (1,2,3),(3,4,4)")
    # parser.getNextToken()
    # while parser.curToken.tokenType != TokenType.TOKEN_END:
    #     print((parser.curToken.value, parser.curToken.tokenType, parser.preToken.tokenType))
    #     parser.getNextToken()
    sparser = SyntaxParser("insert into a (b) values (1,'asxe',3)  ,  (3,4,4)")
    print(sparser.parse())
