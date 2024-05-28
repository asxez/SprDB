```python
createDatabaseTree = {
    "CREATE_DATABASE": {
        "databaseName": '',
    }
}

createTableTree = {
    "CREATE_TABLE": {
        "tableName": "",  # 表名
        "columns": []  # 列名列表
    }
}

selectTree = {
    "SELECT": {
        "columns": [],  # 列名列表
        "from": "",  # 表名
        "where": [],  # WHERE 子句的条件表达式
    }
}

insertTree = {
    "INSERT": {
        "table": '',  # 目标数据表
        "columns": [],  # 插入的列名列表
        "values": []  # 插入的值列表，每个值列表对应一行数据
    }
}

updateTree = {
    "UPDATE": {
        "table": "",  # 目标数据表
        "set": [],  # SET 子句中的更新值
        "where": []  # WHERE 子句的条件表达式
    }
}

deleteTree = {
    "DELETE": {
        "table": '',  # 目标数据表
        "where": []  # WHERE 子句的条件表达式
    }
}

dropDatabaseTree = {
    "DROP_DATABASE": {
        "databaseName": ''
    }
}

dropTableTree = {
    "DROP_TABLE": {
        "tableName": ''
    }
}

```
