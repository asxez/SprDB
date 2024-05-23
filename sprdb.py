#!/usr/bin/python3.10.6
# -*- coding: utf-8 -*-
#
# @Time    : 2024/4/23 下午2:01
# @Author  : ASXE

import sys

from parser import parser
from server.serve import startupServe, destartupServe


def local():
    while True:
        print("sprDB >>> ", end='')
        statement = input('')
        if statement == 'exit':
            print('Good Bye!')
            break
        elif statement == 'startup-auto':
            startupServe()
            continue
        elif statement == 'destartup-auto':
            destartupServe()
            continue
        elif statement == 'help':
            helps = [
                "use < database >",
                "create database < database >",
                "create table < table > (< column > type, ...)",
                "select * | < column > from < table > [where ...]",
                "insert into < table >  [(column, ...)] values (...) [,(...)]",
                "update < table > set < column=..., ... > [where ...]",
                "delete from < table > [where ...]"
            ]
            for help in helps:
                print(help)
            continue
        syntax = parser.SyntaxParser(statement).parse()
        try:
            parser.SemanticParser().main(syntax)
        except:
            pass


if __name__ == '__main__':
    print('Copyright (c) 2024 SprDB Software Foundation. All Rights Reserved.')
    print('Type "help", "exit", "startup-auto" for more information.')
    try:
        local()
    except KeyboardInterrupt:
        print("Terminating threads...")
        sys.exit(0)
