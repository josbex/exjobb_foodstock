import sqlite3
from sqlite3 import Error

db_constants = {"PRODUCT_TABLE" : "products",
                "MONTHS_TABLE" : "months", 
                "STOCK_TABLE" : "stock", 
                "PRODUCT_HISTORY_TABLE" : "history",
                "ESTIMATIONS_TABLE" : "estimatedRates"
                }

product_table = {'ID' : 'id', 'PRODUCT_NAME' : 'name'}
months_table = {'MONTH_ID' : 'id', 'MONTH_NAME' : 'month'}
stock_table = {'PRODUCT_ID' : 'product_id', 'QUANTITY' : 'qty', 'SIZE' : 'packageSize', 'ADDED' : 'addedDate', 'MANUFACTURED' : 'manufactured'}
history_table = {'PRODUCT_ID' : 'product_id', 'ADDED' : 'added_date', 'REMOVED' : 'removed_date', "ACTUAL_RATE" : 'actualRate'}
estimation_table = {'MONTH_ID' : 'month_id', 'PRODUCT_ID' : 'product_id', 'ESTIMATED_RATE' : 'estimatedRate'}

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


