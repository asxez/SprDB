## 语法
create database < database >

create table < table > (< column > type, ...)

select * | < column > from < table > [where ...]

insert into < table >  [(id, name, age, grade)] values(...) [,(...)]

update < table > set < column=..., ... > [where ...]

delete from < table > [where ...]

## 错误类型
- syntaxError
- typeError
- databaseExistsError
- tableExistsError
- columnExistsError
- tableNotExists
- 