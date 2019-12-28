# -*- coding: utf-8 -*-
# !/usr/bin python
"""
@author: fzj 
@license: (C) Copyright 2013-2017, Node Supply Chain Manager Corporation Limited.
@time: 2019/12/27 17:16
@desc:
PyMySQL 是在 Python3.x 版本中用于连接 MySQL 服务器的一个库，Python2中则使用mysqldb。


"""

import pymysql

props = {}
props["host"] = ""
props["user"] = ""
props["password"] = ""
props["database"] = ""
props["table"] = ""


def get_mysql_conn(props):
    conn = pymysql.connect(props['host'], props['user'], props["password"], props["database"], charset="utf8")
    return conn


def create_mysql(conn):
    """
    如果数据库连接存在我们可以使用execute()方法来为数据库创建表，如下所示创建表EMPLOYEE：
    :param conn:
    :return:
    """
    # 使用 cursor() 方法创建一个游标对象 cursor
    cursor = conn.cursor()

    # 使用 execute() 方法执行 SQL，如果表存在则删除
    sql_drop = "DROP TABLE IF EXISTS EMPLOYEE"
    cursor.execute(sql_drop)

    # 使用预处理语句创建表
    sql = """CREATE TABLE EMPLOYEE (
             FIRST_NAME  CHAR(20) NOT NULL,
             LAST_NAME  CHAR(20),
             AGE INT,  
             SEX CHAR(1),
             INCOME FLOAT )"""
    cursor.execute(sql)

    # 关闭数据库连接
    conn.close()


def insert_mysql(conn):
    """将数据库中的基站信息通过web接口获取地理位置"""
    # 使用cursor()方法获取操作游标
    cursor = conn.cursor()
    # SQL 插入语句
    sql = """INSERT INTO EMPLOYEE(FIRST_NAME,
             LAST_NAME, AGE, SEX, INCOME)
             VALUES ('Mac', 'Mohan', 20, 'M', 2000)"""
    try:
        # 执行sql语句
        cursor.execute(sql)
        # 提交到数据库执行
        conn.commit()
    except:
        # 如果发生错误则回滚
        conn.rollback()
    # 关闭数据库连接
    conn.close()


def delete_mysql(conn):
    """

    :param conn:
    :return:
    """
    # 使用cursor()方法获取操作游标
    cursor = conn.cursor()

    # SQL 删除语句
    value = "20"
    sql = f"DELETE FROM EMPLOYEE WHERE AGE > {value}"
    try:
        # 执行SQL语句
        cursor.execute(sql)
        # 提交修改
        conn.commit()
    except:
        # 发生错误时回滚
        conn.rollback()

    # 关闭连接
    conn.close()


def update_mysql(conn):
    """

    :param conn:
    :return:
    """
    # 使用cursor()方法获取操作游标
    cursor = conn.cursor()
    # SQL 更新语句
    sex = "M"
    sql = f"UPDATE EMPLOYEE SET AGE = AGE + 1 WHERE SEX = '{sex}'"
    try:
        # 执行SQL语句
        cursor.execute(sql)
        # 提交到数据库执行
        conn.commit()
    except:
        # 发生错误时回滚
        conn.rollback()
    # 关闭数据库连接
    conn.close()
    pass


def select_mysql(conn):
    """
    fetchone(): 该方法获取下一个查询结果集。结果集是一个对象
    fetchall(): 接收全部的返回结果行.
    rowcount: 这是一个只读属性，并返回执行execute()方法后影响的行数。
    :param conn:
    :return:
    """
    # 使用cursor()方法获取操作游标
    cursor = conn.cursor()
    # SQL 查询语句
    count = 20
    sql = f"SELECT * FROM EMPLOYEE limit {count}"
    try:
        # 执行SQL语句
        cursor.execute(sql)
        # 获取所有记录列表
        results = cursor.fetchall()
        for row in results:
            fname = row[0]
            lname = row[1]
            age = row[2]
            sex = row[3]
            income = row[4]
            # 打印结果
            print(f"fname={fname},lname={lname},age={age},sex={sex},income={income}")
    except:
        print("Error: unable to fetch data")
    # 关闭数据库连接
    conn.close()


if __name__ == '__main__':
    global props
    # 1. 获取mysql连接
    conn = get_mysql_conn(props)
    select_mysql(conn)

    pass
