## 语法
use < database >

create database < database >

create table < table > (< column > type, ...)

select * | < column > from < table > [where ...]

insert into < table >  [(column, ...)] values (...) [,(...)]

update < table > set < column=..., ... > [where ...]

delete from < table > [where ...]

## 错误类型
- syntaxError
- typeError
- databaseExistsError
- databaseNotExistsError
- tableExistsError
- columnExistsError
- tableNotExists
- columnNotExistsError
- valueError
- pathNotExistsError
- systemError
- 