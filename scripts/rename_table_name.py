import os
import pymysql

host = "localhost"
user = "root"
password = "root"
db = "sophon_sam_singer_test"
preStr = "singer_"
dumpFile = "g://temp//{}_bk.sql".format(db)


def showTables(connect):
    cursor = connect.cursor()
    tableCount = cursor.execute("show tables")
    connect.commit()
    print("table number is {}".format(tableCount))
    tables = []
    for table in cursor.fetchall():
        print(table, end="\t")
        tables.append(table[0])
    print()
    cursor.close()
    return tables


def renameTable():
    connect = pymysql.connect(host=host, user=user, password=password, database=db)
    cursor = connect.cursor()

    tables = showTables(connect)
    alterNameSQLs = []
    for table in tables:
        sql = "rename table {} to {}".format(table, preStr + table)
        alterNameSQLs.append(sql)

    for alterNameSQL in alterNameSQLs:
        print("execute sql [{}]".format(alterNameSQL))
        cursor.execute(alterNameSQL)
        connect.commit()

    showTables(connect)

    cursor.close()
    connect.close()


def rollbackTable():
    connect = pymysql.connect(host=host, user=user, password=password, database=db)
    cursor = connect.cursor()

    tables = showTables(connect)
    for table in tables:
        tableName = str(table)
        if tableName.startswith(preStr):
            newTableName = tableName[len(preStr):]
            sql = "rename table {} to {}".format(tableName, newTableName)
            print("roll back sql [{}]".format(sql))
            cursor.execute(sql)
            connect.commit()

    showTables(connect)
    cursor.close()
    connect.close()


if __name__ == '__main__':
    # dumpDataBase()
    # renameTable()
    # rollbackTable()

    pass
