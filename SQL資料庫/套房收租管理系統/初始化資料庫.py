# -*- coding: utf-8 -*-
"""
Created on Wed Nov 30 19:31:01 2022

@author: Cc

參考資料: https://www.runoob.com/python3/python3-mysql.html
"""

import pymysql

# 與資料庫連線
db = pymysql.connect(host='127.0.0.1',
                     user='root',
                     password='123456',
                     database='rental_system')  # 需在Workbench先建立空的database

cursor = db.cursor()

#%% 建立TABLE
cursor.execute("DROP TABLE IF EXISTS 房東")  # 如果表存在則刪除
cursor.execute("DROP TABLE IF EXISTS 房子")  # 如果表存在則刪除
cursor.execute("DROP TABLE IF EXISTS 提供房")  # 如果表存在則刪除
cursor.execute("DROP TABLE IF EXISTS 房間")  # 如果表存在則刪除
cursor.execute("DROP TABLE IF EXISTS 租客")  # 如果表存在則刪除
cursor.execute("DROP TABLE IF EXISTS 合約")  # 如果表存在則刪除
cursor.execute("DROP TABLE IF EXISTS 繳費")  # 如果表存在則刪除

sql1 = """CREATE TABLE 房東(
    房東身分證 char(20) primary key not null,
    房東姓名 char(20) not null,
    房東電話 char(20) not null
)
"""

sql2 = """CREATE TABLE 房子(
    房子地址 char(100) primary key,
    房子名稱 char(100) not null,
    樓層數 int not null
)
"""

sql3 = """CREATE TABLE 提供房(
    房東身分證 char(100) not null,
    房子地址 char(100) not null,
    primary key (房東身分證, 房子地址)
)
"""

sql4 = """CREATE TABLE 房間(
    房子地址 char(100) not null,
    房號 char(10) not null,
    坪數 int not null,
    房間類型 char(10) not null,
    出租狀態 char(10) not null,
    primary key (房子地址, 房號)
)
"""

sql5 = """CREATE TABLE 租客(
    租客身分證 char(20) primary key not null,
    租客姓名 char(20) not null,
    租客電話 char(20) not null
)
"""

sql6 = """CREATE TABLE 合約(
    合約編號 int primary key not null auto_increment,
    每月電費 char(10) not null,
    每月水費 int not null,
    每月租金 int not null,
    租期開始 char(20) not null,
    租期結束 char(20) not null,
    房東身分證 char(20) not null,
    租客身分證 char(20) not null,
    房子地址 char(20) not null,
    房號 char(10) not null
)
"""

sql7 = """CREATE TABLE 繳費(
    合約編號 int primary key not null,
    租客身分證 char(20) not null,
    繳租金 char(10) not null,
    繳水費 char(10) not null,
    繳電費 char(10) not null
)
"""


# 執行sql命令
cursor.execute(sql1)  
cursor.execute(sql2) 
cursor.execute(sql3) 
cursor.execute(sql4) 
cursor.execute(sql5) 
cursor.execute(sql6) 
cursor.execute(sql7) 


#%% 插入data  
sql1_1 = "INSERT INTO 房東(房東身分證, 房東姓名, 房東電話) VALUES('%s', '%s', '%s')" % ('A111111111', '蛇丸', '0911111111')
sql1_2 = "INSERT INTO 房東(房東身分證, 房東姓名, 房東電話) VALUES('%s', '%s', '%s')" % ('A222222222', '陳翔', '0922222222')
sql1_3 = "INSERT INTO 房東(房東身分證, 房東姓名, 房東電話) VALUES('%s', '%s', '%s')" % ('A333333333', '海牛', '0933333333')
sql1_4 = "INSERT INTO 房東(房東身分證, 房東姓名, 房東電話) VALUES('%s', '%s', '%s')" % ('A444444444', '肥叔', '0944444444')

sql2_1 = "INSERT INTO 房子(房子地址, 房子名稱, 樓層數) VALUES('%s', '%s', '%s')" % ('台北市天龍路1號', '天龍泡泡', 2)
sql2_2 = "INSERT INTO 房子(房子地址, 房子名稱, 樓層數) VALUES('%s', '%s', '%s')" % ('桃園市捷運路2號', '棒球公寓', 1)
sql2_3 = "INSERT INTO 房子(房子地址, 房子名稱, 樓層數) VALUES('%s', '%s', '%s')" % ('新竹市風大路3號', '三隻小豬', 3)
sql2_4 = "INSERT INTO 房子(房子地址, 房子名稱, 樓層數) VALUES('%s', '%s', '%s')" % ('栗市木雕路4號', '木頭村', 4)

sql3_1 = "INSERT INTO 提供房(房東身分證, 房子地址) VALUES('%s', '%s')" % ('A111111111', '台北市天龍路1號')
sql3_2 = "INSERT INTO 提供房(房東身分證, 房子地址) VALUES('%s', '%s')" % ('A111111111', '桃園市捷運路2號')
sql3_3 = "INSERT INTO 提供房(房東身分證, 房子地址) VALUES('%s', '%s')" % ('A222222222', '新竹市風大路3號')
sql3_4 = "INSERT INTO 提供房(房東身分證, 房子地址) VALUES('%s', '%s')" % ('A333333333', '栗市木雕路4號')
sql3_5 = "INSERT INTO 提供房(房東身分證, 房子地址) VALUES('%s', '%s')" % ('A444444444', '南投縣魚池鄉5號')

sql4_1 = "INSERT INTO 房間(房子地址, 房號, 坪數, 房間類型, 出租狀態) VALUES('%s', '%s', '%s', '%s', '%s')" % ('台北市天龍路1號', '101', 5, '套房', '已出租')
sql4_2 = "INSERT INTO 房間(房子地址, 房號, 坪數, 房間類型, 出租狀態) VALUES('%s', '%s', '%s', '%s', '%s')" % ('台北市天龍路1號', '102', 4, '套房', '已出租')
sql4_3 = "INSERT INTO 房間(房子地址, 房號, 坪數, 房間類型, 出租狀態) VALUES('%s', '%s', '%s', '%s', '%s')" % ('桃園市捷運路2號', '101', 10, '套房', '已出租')
sql4_4 = "INSERT INTO 房間(房子地址, 房號, 坪數, 房間類型, 出租狀態) VALUES('%s', '%s', '%s', '%s', '%s')" % ('新竹市風大路3號', '101', 6, '雅房', '空房')
sql4_5 = "INSERT INTO 房間(房子地址, 房號, 坪數, 房間類型, 出租狀態) VALUES('%s', '%s', '%s', '%s', '%s')" % ('新竹市風大路3號', '102', 7, '雅房', '已出租')
sql4_6 = "INSERT INTO 房間(房子地址, 房號, 坪數, 房間類型, 出租狀態) VALUES('%s', '%s', '%s', '%s', '%s')" % ('新竹市風大路3號', '201', 6, '套房', '空房')
sql4_7 = "INSERT INTO 房間(房子地址, 房號, 坪數, 房間類型, 出租狀態) VALUES('%s', '%s', '%s', '%s', '%s')" % ('新竹市風大路3號', '202', 7, '套房', '空房')
sql4_8 = "INSERT INTO 房間(房子地址, 房號, 坪數, 房間類型, 出租狀態) VALUES('%s', '%s', '%s', '%s', '%s')" % ('栗市木雕路4號', '101', 5, '雅房', '空房')
sql4_9 = "INSERT INTO 房間(房子地址, 房號, 坪數, 房間類型, 出租狀態) VALUES('%s', '%s', '%s', '%s', '%s')" % ('栗市木雕路4號', '102', 4, '雅房', '空房')
sql4_10 = "INSERT INTO 房間(房子地址, 房號, 坪數, 房間類型, 出租狀態) VALUES('%s', '%s', '%s', '%s', '%s')" % ('栗市木雕路4號', '201', 6, '雅房', '空房')
sql4_11 = "INSERT INTO 房間(房子地址, 房號, 坪數, 房間類型, 出租狀態) VALUES('%s', '%s', '%s', '%s', '%s')" % ('栗市木雕路4號', '202', 3, '雅房', '已出租')

sql5_1 = "INSERT INTO 租客(租客身分證, 租客姓名, 租客電話) VALUES('%s', '%s', '%s')" % ('B111111111', '皮卡丘', '0900000001')
sql5_2 = "INSERT INTO 租客(租客身分證, 租客姓名, 租客電話) VALUES('%s', '%s', '%s')" % ('B222222222', '傑尼龜', '0900000002')
sql5_3 = "INSERT INTO 租客(租客身分證, 租客姓名, 租客電話) VALUES('%s', '%s', '%s')" % ('B333333333', '噴火龍', '0900000003')
sql5_4 = "INSERT INTO 租客(租客身分證, 租客姓名, 租客電話) VALUES('%s', '%s', '%s')" % ('B444444444', '梗鬼', '0900000004')

# INSERT INTO 合約(每月電費, 每月水費, 每月租金, 租期開始, 租期結束, 房東身分證, 租客身分證, 房子地址, 房號) VALUES('1', '1', '1', '1', '1', '1', '1', '1', '1')
sql6_1 = "INSERT INTO 合約(每月電費, 每月水費, 每月租金, 租期開始, 租期結束, 房東身分證, 租客身分證, 房子地址, 房號) VALUES('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s')" % ('4.5/度', 150, 5000, '2019/12/7', '2020/5/31', 'A111111111', 'B222222222', '台北市天龍路1號', '101')
sql6_2 = "INSERT INTO 合約(每月電費, 每月水費, 每月租金, 租期開始, 租期結束, 房東身分證, 租客身分證, 房子地址, 房號) VALUES('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s')" % ('6/度', 200, 7000, '2020/1/1', '2020/12/31', 'A222222222', 'B111111111', '新竹市風大路3號', '102')
sql6_3 = "INSERT INTO 合約(每月電費, 每月水費, 每月租金, 租期開始, 租期結束, 房東身分證, 租客身分證, 房子地址, 房號) VALUES('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s')" % ('4.5/度', 150, 4800, '2019/12/31', '2020/11/30', 'A111111111', 'B333333333', '台北市天龍路1號', '102')
sql6_4 = "INSERT INTO 合約(每月電費, 每月水費, 每月租金, 租期開始, 租期結束, 房東身分證, 租客身分證, 房子地址, 房號) VALUES('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s')" % ('4/度', 100, 4000, '2020/1/1', '2020/6/30', 'A333333333', 'B111111111', '苗栗市木雕路4號', '202')
sql6_5 = "INSERT INTO 合約(每月電費, 每月水費, 每月租金, 租期開始, 租期結束, 房東身分證, 租客身分證, 房子地址, 房號) VALUES('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s')" % ('8/度', 500, 10000, '2020/2/2', '2020/7/31', 'A111111111', 'B444444444', '桃園市捷運路2號', '101')

sql7_1 = "INSERT INTO 繳費(合約編號, 租客身分證, 繳租金, 繳水費, 繳電費) VALUES('%s', '%s', '%s', '%s', '%s')" % (2, 'B111111111', 'O', 'O', 'O')
sql7_2 = "INSERT INTO 繳費(合約編號, 租客身分證, 繳租金, 繳水費, 繳電費) VALUES('%s', '%s', '%s', '%s', '%s')" % (4, 'B111111111', 'O', 'O', 'X')
sql7_3 = "INSERT INTO 繳費(合約編號, 租客身分證, 繳租金, 繳水費, 繳電費) VALUES('%s', '%s', '%s', '%s', '%s')" % (1, 'B222222222', 'X', 'X', 'X')
sql7_4 = "INSERT INTO 繳費(合約編號, 租客身分證, 繳租金, 繳水費, 繳電費) VALUES('%s', '%s', '%s', '%s', '%s')" % (3, 'B333333333', 'O', 'X', 'O')
sql7_5 = "INSERT INTO 繳費(合約編號, 租客身分證, 繳租金, 繳水費, 繳電費) VALUES('%s', '%s', '%s', '%s', '%s')" % (5, 'B444444444', 'X', 'O', 'O')


try:
    # 執行sql命令
    cursor.execute(sql1_1)
    cursor.execute(sql1_2)
    cursor.execute(sql1_3)
    cursor.execute(sql1_4)
    
    cursor.execute(sql2_1)
    cursor.execute(sql2_2)
    cursor.execute(sql2_3)
    cursor.execute(sql2_4)
    
    cursor.execute(sql3_1)
    cursor.execute(sql3_2)
    cursor.execute(sql3_3)
    cursor.execute(sql3_4)
    cursor.execute(sql3_5)
    
    cursor.execute(sql4_1)
    cursor.execute(sql4_2)
    cursor.execute(sql4_3)
    cursor.execute(sql4_4)
    cursor.execute(sql4_5)
    cursor.execute(sql4_6)
    cursor.execute(sql4_7)
    cursor.execute(sql4_8)
    cursor.execute(sql4_9)
    cursor.execute(sql4_10)
    cursor.execute(sql4_11)
    
    cursor.execute(sql5_1)    
    cursor.execute(sql5_2)    
    cursor.execute(sql5_3)    
    cursor.execute(sql5_4)
       
    cursor.execute(sql6_1)
    cursor.execute(sql6_2)
    cursor.execute(sql6_3)
    cursor.execute(sql6_4)
    cursor.execute(sql6_5)
    
    cursor.execute(sql7_1)
    cursor.execute(sql7_2)
    cursor.execute(sql7_3)
    cursor.execute(sql7_4)
    cursor.execute(sql7_5)
    
    # 提交到數據庫執行
    db.commit()
except:
    # 如果發生錯誤回滾
    print("Insert error")
    db.rollback()
    
# #%% 查詢data
# # fetchone(): 獲取單條數據 (若為單變數，需加%(,))
# # fetchall(): 獲取全部數據

# age_num = 1
# sql = """
#     SELECT *
#     FROM employee
#     WHERE age > %s
# """ %(age_num)

# try:
#     cursor.execute(sql)
    
#     # 獲取所有紀錄列表
#     results = cursor.fetchall()
#     print("資料列數:", len(results))
#     print("Result=%s" %(results,),"\n")
#     # 抓出想要的值
#     for row in results:
#         id = row[0]  # 單條看有幾個attribute
#         fname = row[1]  
#         lname = row[2]
#         age = row[3]
#         sex = row[4]
#         dno = row[5]

#         print("id=%s, fname=%s, lname=%s, age=%s, sex=%s, dno=%s" %(id, fname, lname, age, sex, dno))
# except:
#     print("Select error")

# #%% 更新data
# sql = """
#     UPDATE employee
#     SET age = age + 1000
#     WHERE sex = '%c'
# """ %('G')

# try:
#     cursor.execute(sql)
#     db.commit()
# except:
#     print("Update error")
#     db.rollback()

# #%% 加入Foreign Key外鍵 (防止誤刪-關聯資料)

# # foreign_key = """
# #     ALTER TABLE employee ADD FOREIGN KEY(dno)
# #     REFERENCES department(dnumber)
# # """
# # cursor.execute(foreign_key)

# #%% 刪除data
# sql = """
#     DELETE FROM department
#     WHERE dname = '%s'
# """ %('FB')

# try:
#     cursor.execute(sql)
#     db.commit()
# except:
#     print("Delete error")
#     db.rollback()

db.close()