from util import db_constants
import naiveBayes
import sqlite3
from datetime import datetime
from datetime import date
import calendar

def makePrediction(id, month):
    data = getProductHistory(id)
    months = data.values()
    rates = data.keys()
    predictedRate = naiveBayes.makePrediction(naiveBayes.trainModel(months, rates), month)
    return predictedRate

def updateEstimation(id, month):
    month_stmt = "SELECT " +  util.months_table['MONTH_ID'] + " FROM " + util.db_constants['MONTHS_TABLE'] + " WHERE " +  util.months_table['MONTH_NAME'] + "=?;"
    month_field = [month]
    month_data = util.getData(month_stmt, month_field)
    stmt = "UPDATE " + util.db_constants['ESTIMATIONS_TABLE'] + " WHERE " +  util.estimation_table['MONTH_ID'] + "=? AND " +  util.estimation_table['PRODUCT_ID'] + "=?;"
    fields = [month_data['id'], id]
    lastrowid = util.executeQuery(stmt, fields)
    return lastrowid

def getProductHistory(id):
    stmt = "SELECT * FROM " + util.db_constants['PRODUCT_HISTORY_TABLE'] + "WHERE " +  util.history_table['PRODUCT_ID'] + "=?;"
    field = [id]
    data = util.getData(stmt, field)
    rate_month_data = filterData(data)
    return rate_month_data

def filterData(data):
    filteredData = {}
    for row in data:
        filteredData.update({row[util.history_table['ACTUAL_RATE']], monthToString(row[util.history_table['ADDED']], row[util.history_table['REMOVED']])})
    return filteredData

def monthToString(dateAdded, dateRemoved):
    month = whichMonth(dateAdded,dateRemoved)
    return month.strftime("%B")

def whichMonth(dateAdded, dateRemoved):
    lastDayofMonth = calendar.monthrange(dateAdded.year, dateAdded.month)
    #At what month did the consumption mainly occur? 
    if (lastDayofMonth - dateAdded).days > (datetime.datetime(dateRemoved.year, dateRemoved.month, 1) - dateRemoved).days:
        return dateAdded
    else:
        return dateRemoved



#Functions for webpage 
#--------------------------------------------------------------------

def addNewProduct(name, created, expires, qty):
    shelflife = (expires - created).days
    stmt = "INSERT INTO " + db_constants['PRODUCT_TABLE'] + " VALUES(?,?);"
    fields = [name, shelflife]
    id = util.executeQuery(stmt, fields)
    addToStock(id, qty, created)
    return id

def addToStock(id, qty, created):
    stmt = "INSERT INTO " + db_constants['STOCK_TABLE'] + " VALUES(?,?,?,?);"
    dateAdded = date.today()
    fields = [id, 0, qty, dateAdded, created]
    id = util.executeQuery(stmt, fields)
    return id

def increaseQty(id):
    updateStmt = "UPDATE " + util.db_constants['STOCK_TABLE'] + " SET " +  util.stock_table['QUANTITY'] + " = "+ util.stock_table['QUANTITY'] + " + 1  WHERE " +  util.stock_table['PRODUCT_ID'] + "=?;"
    updateFields = [id]
    id = util.executeQuery(updateStmt, updateFields)
    return id

def decreaseQty(id):
    #add to history
    stmt = "SELECT * FROM " + util.db_constants['STOCK_TABLE'] + " WHERE " +  util.stock_table['PRODUCT_ID'] + "=?;"
    field = [id]
    stockInfo = util.getData(stmt, field)
    added = stockInfo[util.stock_table['ADDED']]
    removed = date.today()
    rate = calculateRate(added, removed)
    updateHistory(id, added, removed, rate)
    if stockInfo[util.stock_table['QUANITY']] > 1:
        updateStmt = "UPDATE " + util.db_constants['STOCK_TABLE'] + " SET " +  util.stock_table['QUANTITY'] + " = "+ util.stock_table['QUANTITY'] + " - 1  WHERE " +  util.stock_table['PRODUCT_ID'] + "=?;"
        updateFields = [id]
        id = util.executeQuery(updateStmt, updateFields)
    else:
        id = removeFromStock(id)
    return id

def removeFromStock(id):
    stmt = "DELETE FROM " + util.db_constants['STOCK_TABLE'] + " WHERE " +  util.stock_table['PRODUCT_ID'] + "=?;"
    fields = [id]
    id = util.executeQuery(stmt, fields)
    #removes item from stock
    #only callable through decreaseQty
    #otherwise flag would be neccessary to see if it has been added to history yet
    return id

def updateHistory(id,added, removed, rate):
    stmt =  "INSERT INTO " + db_constants['PRODUCT_HISTORY_TABLE'] + " VALUES(?,?,?,?);"
    actualRate = calculateRate(added, removed)
    fields = [id, added, removed, actualRate]
    id = util.executeQuery(stmt, fields)
    return id

#Added, removed are datetime objects 
#retrived from product history table
def calculateRate(added, removed):
    return (removed - added).days



