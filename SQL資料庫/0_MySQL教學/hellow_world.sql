# 開始指令
# SHOW databases/tables
# CREATE databases {databases_name}
# DROP databases/table {databases_name/table_name}
# USE {databases_name}

# 創造資料
# CREATE TABLE {table_name}{  
#	a int,
#	b varchar(123)
# };

# 顯示資料
# SELECT {a,b} 
# FROM {table_name} 
# WHERE {條件};  

# 新增資料
# INSERT INTO {table_name}(a,b) VALUES (a_data, b_data);  

# 更新資料
# UPDATE {table_name}  
# SET a={new_value}, b={new_value}
# WHERE {篩選條件};

# 刪除資料
# DELETE FROM {table_name}
# WHERE {篩選條件};


show databases; # 查看所有databse
create database test;
#drop database test;
use test;
show tables; # 查看databse裡的所有table

# 建立新的資料表
create table product( 
	id int primary key auto_increment,  # primary key auto_increment:主鍵(提供報錯)，編號自動增加
    name varchar(255) not null,  # not null:資料不可以是空白
    price int not null default 30  # default:預設30
);

select * from product;  # 查詢
select price, name, id from product where price!=40;  # <>: 不等於

insert into product(id, name, price) values(1, '牛奶', 100);
insert into product(id, name, price) values(2, '熱狗', 40);
insert into product(name, price) values('綠茶', 20);  # 自動primary key加1 (auto_increment效果)
insert into product(name) values('紅茶');

drop table product; # 移除table

SET sql_safe_updates=0;  # 關閉安全索引 (與key有關)

UPDATE product  # 更新attribute
SET price = 1000
WHERE name='綠茶';

DELETE FROM product  # 刪除attribute
WHERE id=4;