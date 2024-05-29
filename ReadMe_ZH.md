# SprDB

SprDB 是一门基于Python的关系型数据库。

## 🛠️ 构建说明
Windows上:
```bash
make w
```

Linux上（暂不支持）:
```bash
make l
```
然后你就可以得到一个`dist`文件夹，并且包含了一个可执行文件，双击或者终端使用命令即可运行。

## ✨ 语法结构
use < database >

create database < database >

create table < table > (< column > type, ...)

select * | < column > from < table > [where ...]

insert into < table >  [(column, ...)] values (...) [,(...)]

update < table > set < column=..., ... > [where ...]

delete from < table > [where ...]

语法与SQL语法一致，唯一不同在于列的类型，本系统仅包含三种类型，字符串类型（str），整型（int），浮点型（float）。

下列为本系统特有命令：
```sql
startup-auto  --开启开机自启动
destartup-auto  --关闭开机自启动
exit  --退出命令行
help  --查看帮助
```

## 👁️ 许可证
详见LICENSE。
