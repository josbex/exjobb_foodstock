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
    predictedRate = API.naiveBayes.makePrediction(API.naiveBayes.trainModel(months, rates), month)
    return predictedRate

def updateEstimation(id, month):
    month_stmt = "SELECT " +  API.util.months_table['MONTH_ID'] + " FROM " + API.util.db_constants['MONTHS_TABLE'] + " WHERE " +  API.util.months_table['MONTH_NAME'] + "=?;"
    month_field = [month]
    month_data = API.util.getData(month_stmt, month_field)
    stmt = "UPDATE " + API.util.db_constants['ESTIMATIONS_TABLE'] + " WHERE " +  API.util.estimation_table['MONTH_ID'] + "=? AND " +  API.util.estimation_table['PRODUCT_ID'] + "=?;"
    fields = [month_data['id'], id]
    lastrowid = API.util.executeQuery(stmt, fields)
    return lastrowid

def getProductHistory(id):
    stmt = "SELECT * FROM " + API.util.db_constants['PRODUCT_HISTORY_TABLE'] + "WHERE " +  API.util.history_table['PRODUCT_ID'] + "=?;"
    field = [id]
    data = API.util.getData(stmt, field)
    rate_month_data = filterData(data)
    return rate_month_data

def filterData(data):
    filteredData = {}
    for row in data:
        filteredData.update({row[API.util.history_table['ACTUAL_RATE']], monthToString(row[API.util.history_table['ADDED']], row[API.util.history_table['REMOVED']])})
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
    id = API.util.executeQuery(stmt, fields)
    addToStock(id, qty, created)
    return id

def addToStock(id, qty, created):
    stmt = "INSERT INTO " + db_constants['STOCK_TABLE'] + " VALUES(?,?,?,?);"
    dateAdded = date.today()
    fields = [id, 0, qty, dateAdded, created]
    id = API.util.executeQuery(stmt, fields)
    return id

def increaseQty(id):
    updateStmt = "UPDATE " + API.util.db_constants['STOCK_TABLE'] + " SET " +  API.util.stock_table['QUANTITY'] + " = "+ API.util.stock_table['QUANTITY'] + " + 1  WHERE " +  API.util.stock_table['PRODUCT_ID'] + "=?;"
    updateFields = [id]
    id = API.util.executeQuery(updateStmt, updateFields)
    return id

def decreaseQty(id):
    #add to history
    stmt = "SELECT * FROM " + API.util.db_constants['STOCK_TABLE'] + " WHERE " +  API.util.stock_table['PRODUCT_ID'] + "=?;"
    field = [id]
    stockInfo = API.util.getData(stmt, field)
    added = stockInfo[API.util.stock_table['ADDED']]
    removed = date.today()
    rate = calculateRate(added, removed)
    updateHistory(id, added, removed, rate)
    if stockInfo[API.util.stock_table['QUANITY']] > 1:
        updateStmt = "UPDATE " + API.util.db_constants['STOCK_TABLE'] + " SET " +  API.util.stock_table['QUANTITY'] + " = "+ API.util.stock_table['QUANTITY'] + " - 1  WHERE " +  API.util.stock_table['PRODUCT_ID'] + "=?;"
        updateFields = [id]
        id = API.util.executeQuery(updateStmt, updateFields)
    else:
        id = removeFromStock(id)
    return id

def removeFromStock(id):
    stmt = "DELETE FROM " + API.util.db_constants['STOCK_TABLE'] + " WHERE " +  API.util.stock_table['PRODUCT_ID'] + "=?;"
    fields = [id]
    id = API.util.executeQuery(stmt, fields)
    #removes item from stock
    #only callable through decreaseQty
    #otherwise flag would be neccessary to see if it has been added to history yet
    return id

def updateHistory(id,added, removed, rate):
    stmt =  "INSERT INTO " + db_constants['PRODUCT_HISTORY_TABLE'] + " VALUES(?,?,?,?);"
    actualRate = calculateRate(added, removed)
    fields = [id, added, removed, actualRate]
    id = API.util.executeQuery(stmt, fields)
    return id

#Added, removed are datetime objects 
#retrived from product history table
def calculateRate(added, removed):
    return (removed - added).days



