# SprDB

SprDB is a relational database based on Python.

## Build Instructions
on Windows:
```bash
make w
```

on Linux(Not at this time):
```bash
make l
```

Then you will get a `dist` folder with an executable file that can be run by double-clicking or using the terminal command.

## ✨Grammar
use < database >

create database < database >

create table < table > (< column > type, ...)

select * | < column > from < table > [where ...]

insert into < table >  [(column, ...)] values (...) [,(...)]

update < table > set < column=..., ... > [where ...]

delete from < table > [where ...]

The syntax is the same as the SQL syntax, the only difference is the type of column, the SprDB only contains three types, string type (str), inter type (int), floating point type (float).

The following commands are unique to SprDB:：
```sql
startup-auto  --Turn on auto-start at boot
destartup-auto  --Turn off auto-start at boot
exit  --Exit the command line
help  --Check out Help
```

## LICENSE
For details, see the license file。
