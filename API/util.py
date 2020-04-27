import sqlite3
from sqlite3 import Error

db_constants = {"PRODUCT_TABLE" : "products",
                "MONTHS_TABLE" : "months", 
                "STOCK_TABLE" : "stock", 
                "PRODUCT_HISTORY_TABLE" : "history",
                "ESTIMATIONS_TABLE" : "estimatedRates"
                }

def getDBConnection(db):
    try:
        conn = sqlite3.connect(db)
    except Error as e:
        print(e)
    return conn


def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d

def getData(stmt, fields):
    conn = getDBConnection('test.db')
    conn.row_factory = dict_factory
    cur = conn.cursor()
    data = cur.execute(stmt, fields).fetchall()
    return data

def executeQuery(stmt, fields):
    conn = getDBConnection('test.db')
    cur = conn.cursor()
    cur.execute(stmt, fields)
    conn.commit()
    return cur.lastrowid


