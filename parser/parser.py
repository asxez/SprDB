#!/usr/bin/python3.10.6
# -*- coding: utf-8 -*-
#
# @Time    : 2024/4/20 20:39
# @Author  : ASXE


from enum import Enum, auto


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
    KeywordsToken("IN", 2, TokenType.TOKEN_IN)
]


class Parser:
    """词法分析器"""

    def __init__(self):
        self.curToken: Token = Token(TokenType.TOKEN_END)  # 当前token
        self.preToken: Token = Token(TokenType.TOKEN_END)  # 前一个token
        self.sourceCode: str = ''  # 源码串
        self.curPosition: int = 0  # 当前所在源码串位置

    def parse(self, statement: str):
        """解析"""
        self.sourceCode = statement
        self.getNextToken()

    def skipBlanks(self):
        """跳过空白"""
        while self.curPosition < len(self.sourceCode) and self.sourceCode[self.curPosition].isspace():
            self.curPosition += 1

    def parseID(self):
        if self.sourceCode[self.curPosition].isalpha():
            # 识别关键字或者标识符
            identifier = ''
            while self.curPosition < len(self.sourceCode) and self.sourceCode[self.curPosition].isalnum():
                identifier += self.sourceCode[self.curPosition]
                self.curPosition += 1
            for keywordToken in keywordsToken:
                if keywordToken.keyword.upper() == identifier.upper():
                    self.curToken.tokenType = keywordToken.tokenType
                    self.curToken.length = keywordToken.length
                    self.curToken.value = keywordToken.keyword
                    break
                self.curToken.tokenType = TokenType.TOKEN_ID
                self.curToken.length = len(identifier)
                self.curToken.value = identifier

        elif self.sourceCode[self.curPosition].isdigit():
            # 识别数字
            num = ''
            while self.curPosition < len(self.sourceCode) and self.sourceCode[self.curPosition].isdigit():
                num += self.sourceCode[self.curPosition]
                self.curPosition += 1
            self.curToken.tokenType = TokenType.TOKEN_NUM
            self.curToken.length = len(num)
            self.curToken.value = num

    def getNextToken(self):
        """获取下一个token"""
        self.preToken = self.curToken
        self.skipBlanks()
        self.curToken = Token(TokenType.TOKEN_END)
        while self.curPosition < len(self.sourceCode) and self.sourceCode[self.curPosition] != ';':
            match self.sourceCode[self.curPosition]:
                case ',':
                    self.curToken.tokenType = TokenType.TOKEN_COMMA
                    self.curToken.length = 1
                    self.curToken.value = ','
                    self.curPosition += 1
                    break
                case '.':
                    self.curToken.tokenType = TokenType.TOKEN_DOT
                    self.curToken.length = 1
                    self.curToken.value = '.'
                    self.curPosition += 1
                    break
                case '>':
                    if self.sourceCode[self.curPosition + 1] == '=':
                        self.curToken.tokenType = TokenType.TOKEN_MORE_EQUAL
                        self.curToken.length = 2
                        self.curToken.value = '>='
                        self.curPosition += 2
                    else:
                        self.curToken.tokenType = TokenType.TOKEN_MORE
                        self.curToken.length = 1
                        self.curToken.value = '>'
                        self.curPosition += 1
                    break
                case '<':
                    if self.sourceCode[self.curPosition + 1] == '=':
                        self.curToken.tokenType = TokenType.TOKEN_LESS_EQUAL
                        self.curToken.length = 2
                        self.curToken.value = '<='
                        self.curPosition += 2
                    else:
                        self.curToken.tokenType = TokenType.TOKEN_LESS
                        self.curToken.length = 1
                        self.curToken.value = '<'
                        self.curPosition += 1
                    break
                case '(':
                    self.curToken.tokenType = TokenType.TOKEN_LEFT_PAREN
                    self.curToken.length = 1
                    self.curToken.value = '('
                    self.curPosition += 1
                    break
                case ')':
                    self.curToken.tokenType = TokenType.TOKEN_RIGHT_PAREN
                    self.curToken.length = 1
                    self.curToken.value = ')'
                    self.curPosition += 1
                    break
                case '*':
                    self.curToken.tokenType = TokenType.TOKEN_STAR
                    self.curToken.length = 1
                    self.curToken.value = '*'
                    self.curPosition += 1
                    break
                case '=':
                    self.curToken.tokenType = TokenType.TOKEN_EQUAL
                    self.curToken.length = 1
                    self.curToken.value = '='
                    self.curPosition += 1
                    break
                case ';':
                    self.curToken.tokenType = TokenType.TOKEN_END
                    self.curToken.length = 1
                    self.curToken.value = ';'
                    self.curPosition += 1
                    break
                case _:
                    self.parseID()
                    break

        if self.curPosition > len(self.sourceCode):
            # 如果已经到达源代码的末尾，设置当前 token 为结束标志
            self.curToken.tokenType = TokenType.TOKEN_END


if __name__ == '__main__':
    parser = Parser()
    parser.parse("update test set col=1 where a = 1")
    while parser.curToken.tokenType != TokenType.TOKEN_END:
        print((parser.curToken.value, parser.curToken.tokenType, parser.preToken.tokenType))
        parser.getNextToken()
