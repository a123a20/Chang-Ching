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
                     database='testDB')  # 需在Workbench先建立空的database

cursor = db.cursor()

#%% 建立TABLE
cursor.execute("DROP TABLE IF EXISTS employee")  # 如果表存在則刪除
cursor.execute("DROP TABLE IF EXISTS department")  # 如果表存在則刪除

sql1 = """CREATE TABLE employee(
    id int primary key auto_increment,
    first_name char(20) not null,
    last_name char(20),
    age int,
    sex char(1),
    dno int
)
"""
# 另一種寫法
sql2 = "CREATE TABLE department( \
    dnumber int primary key auto_increment, \
    dname char(255) \
) \
"

# 執行sql命令
cursor.execute(sql1)  
cursor.execute(sql2) 


#%% 插入data
sql1 = """INSERT INTO employee(first_name, last_name, age, sex, dno) VALUES('Mac', 'Mohan', 20, 'M', 1)"""
sql2 = "INSERT INTO employee(first_name, last_name, age, sex, dno) VALUES('%s', '%s', '%s', '%s', '%s')" % ('Nick', 'Young', 10, 'G', 2)
sql3 = "INSERT INTO employee(first_name, last_name, age, sex, dno) VALUES('%s', '%s', '%s', '%s', '%s')" % ('Nick', 'Wang', 28, 'M', 3)
sql4 = "INSERT INTO employee(first_name, last_name, age, sex, dno) VALUES('%s', '%s', '%s', '%s', '%s')" % ('Jone', 'JJ', 20, 'M', 1)
sql5 = "INSERT INTO employee(first_name, last_name, age, sex, dno) VALUES('%s', '%s', '%s', '%s', '%s')" % ('Ching', 'Cc', 24, 'M', 3)

sql6 = "INSERT INTO department(dnumber, dname) VALUES('%s', '%s')" % (1,'Apple')
sql7 = "INSERT INTO department(dnumber, dname) VALUES('%s', '%s')" % (2,'Google')
sql8 = "INSERT INTO department(dnumber, dname) VALUES('%s', '%s')" % (3,'FB')

try:
    # 執行sql命令
    cursor.execute(sql1)
    cursor.execute(sql2)
    cursor.execute(sql3)
    cursor.execute(sql4)
    cursor.execute(sql5)
    cursor.execute(sql6)
    cursor.execute(sql7)
    cursor.execute(sql8)
    # 提交到數據庫執行
    db.commit()
except:
    # 如果發生錯誤回滾
    print("Insert error")
    db.rollback()
    
#%% 查詢data
# fetchone(): 獲取單條數據 (若為單變數，需加%(,))
# fetchall(): 獲取全部數據

age_num = 1
sql = """
    SELECT *
    FROM employee
    WHERE age > %s
""" %(age_num)

try:
    cursor.execute(sql)
    
    # 獲取所有紀錄列表
    results = cursor.fetchall()
    print("資料列數:", len(results))
    print("Result=%s" %(results,),"\n")
    # 抓出想要的值
    for row in results:
        id = row[0]  # 單條看有幾個attribute
        fname = row[1]  
        lname = row[2]
        age = row[3]
        sex = row[4]
        dno = row[5]

        print("id=%s, fname=%s, lname=%s, age=%s, sex=%s, dno=%s" %(id, fname, lname, age, sex, dno))
except:
    print("Select error")

#%% 更新data
sql = """
    UPDATE employee
    SET age = age + 1000
    WHERE sex = '%c'
""" %('G')

try:
    cursor.execute(sql)
    db.commit()
except:
    print("Update error")
    db.rollback()

#%% 加入Foreign Key外鍵 (防止誤刪-關聯資料)

# foreign_key = """
#     ALTER TABLE employee ADD FOREIGN KEY(dno)
#     REFERENCES department(dnumber)
# """
# cursor.execute(foreign_key)

#%% 刪除data
sql = """
    DELETE FROM department
    WHERE dname = '%s'
""" %('FB')

try:
    cursor.execute(sql)
    db.commit()
except:
    print("Delete error")
    db.rollback()

db.close()