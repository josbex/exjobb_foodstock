from extras import *
from naiveBayes import *
from datetime import datetime
from datetime import date
import calendar

def makeProductPrediction(id, month):
    data = getProductHistory(id)
    months = data.values()
    rates = data.keys()
    predictedRate = makePrediction(trainModel(months, rates), month)
    return predictedRate

def updateEstimation(id, month):
    month_stmt = "SELECT " +  months_table['MONTH_ID'] + " FROM " + db_constants['MONTHS_TABLE'] + " WHERE " +  months_table['MONTH_NAME'] + "=?;"
    month_field = [month]
    month_data = getData(month_stmt, month_field)
    stmt = "UPDATE " + db_constants['ESTIMATIONS_TABLE'] + " WHERE " +  estimation_table['MONTH_ID'] + "=? AND " +  estimation_table['PRODUCT_ID'] + "=?;"
    fields = [month_data['id'], id]
    lastrowid = executeQuery(stmt, fields)
    return lastrowid

def getProductHistory(id):
    stmt = "SELECT * FROM " + db_constants['PRODUCT_HISTORY_TABLE'] + "WHERE " +  history_table['PRODUCT_ID'] + "=?;"
    field = [id]
    data = getData(stmt, field)
    rate_month_data = filterData(data)
    return rate_month_data

def filterData(data):
    filteredData = {}
    for row in data:
        filteredData.update({row[history_table['ACTUAL_RATE']], monthToString(row[history_table['ADDED']], row[history_table['REMOVED']])})
    return filteredData

def monthToString(dateAdded, dateRemoved):
    month = whichMonth(dateAdded,dateRemoved)
    return month.strftime("%B")

def stringToMonth(dateStr):
    return datetime.strptime(dateStr, '%Y-%m-%d').date()

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
    stmt = "INSERT INTO " + db_constants['PRODUCT_TABLE'] +" ( "+ product_table['PRODUCT_NAME'] + ", "+ product_table['SHELFLIFE'] +") VALUES(?,?);"
    fields = [name, shelflife]
    id = executeQuery(stmt, fields)
    addToStock(id, qty, created)
    return id

def addToStock(id, qty, created):
    stmt = "INSERT INTO " + db_constants['STOCK_TABLE'] +" ( "+ stock_table['PRODUCT_ID'] + ", "+ stock_table['SIZE']+ ", "+ stock_table['QUANTITY'] + ", "+ stock_table['ADDED'] + ", "+ stock_table['MANUFACTURED'] + ") VALUES(?,?,?,?,?);"
    dateAdded = date.today()
    fields = [id, 0, qty, dateAdded, created]
    id = executeQuery(stmt, fields)
    return id

def increaseQty(id):
    updateStmt = "UPDATE " + db_constants['STOCK_TABLE'] + " SET " +  stock_table['QUANTITY'] + " = "+ stock_table['QUANTITY'] + " + 1  WHERE " +  stock_table['PRODUCT_ID'] + "=?;"
    updateFields = [id]
    id = executeQuery(updateStmt, updateFields)
    return id

def decreaseQty(id):
    #add to history
    stmt = "SELECT * FROM " + db_constants['STOCK_TABLE'] + " WHERE " +  stock_table['PRODUCT_ID'] + "=?;"
    field = [id]
    stockInfo = getData(stmt, field)
    added = stockInfo[stock_table['ADDED']]
    removed = date.today()
    rate = calculateRate(added, removed)
    updateHistory(id, added, removed, rate)
    if stockInfo[stock_table['QUANITY']] > 1:
        updateStmt = "UPDATE " + db_constants['STOCK_TABLE'] + " SET " +  stock_table['QUANTITY'] + " = "+ stock_table['QUANTITY'] + " - 1  WHERE " +  stock_table['PRODUCT_ID'] + "=?;"
        updateFields = [id]
        id = executeQuery(updateStmt, updateFields)
    else:
        id = removeFromStock(id)
    return id

def removeFromStock(id):
    stmt = "DELETE FROM " + db_constants['STOCK_TABLE'] + " WHERE " +  stock_table['PRODUCT_ID'] + "=?;"
    fields = [id]
    id = executeQuery(stmt, fields)
    #removes item from stock
    #only callable through decreaseQty
    #otherwise flag would be neccessary to see if it has been added to history yet
    return id

def updateHistory(id,added, removed, rate):
    stmt =  "INSERT INTO " + db_constants['PRODUCT_HISTORY_TABLE'] + " ( "+ history_table['PRODUCT_ID'] + ", "+ history_table['ADDED']+ ", "+ history_table['REMOVED'] + ", "+ history_table['ACTUAL_RATE'] + ")  VALUES(?,?,?,?);"
    actualRate = calculateRate(added, removed)
    fields = [id, added, removed, actualRate]
    id = executeQuery(stmt, fields)
    return id

#Added, removed are datetime objects 
#retrived from product history table
def calculateRate(added, removed):
    return (removed - added).days



