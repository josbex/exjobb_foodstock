from extras import getData, db_constants, product_table, stock_table, history_table, estimation_table, months_table, value_constants, executeQuery
from naiveBayes import makePrediction, trainModel
from datetime import datetime, date
import calendar

#Functions for making predictions
#------------------------------------------------------------------------------
def predictRate(id):
    if isEnoughEntries(id):
        month = monthToString(date.today())
        monthID = getMonthID(month)
        predictedRate = makeProductPrediction(id, monthID)
        print(predictedRate)
        #This will be done client side
        #The app will only contact the server once there is enough data
        if isFirstPrediction(id, month): 
            insertEstimation(id, month, predictedRate[0])
        else:
            updateEstimation(id,month, predictedRate[0])
    return predictRate

def makeProductPrediction(id, monthID):
    months, rates = getProductHistory(id)
    monthIDs = convertMonthsToInt(months)
    predictedRate = makePrediction(trainModel(monthIDs, rates), monthID)
    return predictedRate

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
    dateAdded = datetime.today()
    fields = [id, 0, qty, dateAdded, created]
    id = executeQuery(stmt, fields)
    return id

def increaseQty(id):
    updateStmt = "UPDATE " + db_constants['STOCK_TABLE'] + " SET " +  stock_table['QUANTITY'] + " = "+ stock_table['QUANTITY'] + " + 1  WHERE " +  stock_table['PRODUCT_ID'] + " =?;"
    updateFields = [id]
    id = executeQuery(updateStmt, updateFields)
    return id


#Database handling
#---------------------------------------------------------------------------------
def updateEstimation(id, month, rate):
    monthID = getMonthID(month)
    stmt = "UPDATE " + db_constants['ESTIMATIONS_TABLE'] + "SET " + estimation_table['ESTIMATED_RATE'] + " =? WHERE " +  estimation_table['MONTH_ID'] + "=? AND " +  estimation_table['PRODUCT_ID'] + "=?;"
    fields = [rate, monthID, id]
    lastrowid = executeQuery(stmt, fields)
    return lastrowid

def insertEstimation(id, month, rate):
    stmt = "INSERT INTO " + db_constants['ESTIMATIONS_TABLE'] +" ( "+ estimation_table['MONTH_ID'] + ", "+ estimation_table['PRODUCT_ID'] + ", "+ estimation_table['ESTIMATED_RATE'] + ") VALUES(?,?,?);"
    monthID = getMonthID(month)
    fields = [monthID, id, rate]
    id = executeQuery(stmt, fields)
    return id

def getEstimation(id, month):
    monthId = getMonthID(month)
    stmt = "SELECT * FROM " + db_constants['ESTIMATIONS_TABLE'] + " WHERE " +  estimation_table['PRODUCT_ID'] + "=? AND " + estimation_table['MONTH_ID'] + " =?;"
    field = [id, monthId]
    data = getData(stmt, field)
    return data
    
def getMonthID(month):
    #print(month)
    month_stmt = "SELECT * FROM " + db_constants['MONTHS_TABLE'] + " WHERE " +  months_table['MONTH_NAME'] + " =?;"
    month_field = [month]
    month_data = getData(month_stmt, month_field)
    #print(month_data)
    return month_data[0][months_table['MONTH_ID']]

def getProductHistory(id):
    stmt = "SELECT * FROM " + db_constants['PRODUCT_HISTORY_TABLE'] + " WHERE " +  history_table['PRODUCT_ID'] + " =?;"
    field = [id]
    data = getData(stmt, field)
    #print(data)
    months, rates = filterData(data)
    return months, rates

#Adds product to history, calculating the actual time of consumption
#returns the row of the stock that was affected
def moveToHistory(id):
    stmt = "SELECT * FROM " + db_constants['STOCK_TABLE'] + " WHERE " +  stock_table['PRODUCT_ID'] + " =?;"
    field = [id]
    stockInfo = getData(stmt, field)
    added = stringToMonth(stockInfo[0][stock_table['ADDED']])
    removed = datetime.today()
    rate = calculateRate(added, removed)
    updateHistory(id, added, removed, rate)
    return stockInfo

def updateHistory(id,added, removed, rate):
    stmt =  "INSERT INTO " + db_constants['PRODUCT_HISTORY_TABLE'] + " ( "+ history_table['PRODUCT_ID'] + ", "+ history_table['ADDED']+ ", "+ history_table['REMOVED'] + ", "+ history_table['ACTUAL_RATE'] + ")  VALUES(?,?,?,?);"
    actualRate = calculateRate(added, removed)
    fields = [id, added, removed, actualRate]
    id = executeQuery(stmt, fields)
    return id

def removeFromStock(id):
    stmt = "DELETE FROM " + db_constants['STOCK_TABLE'] + " WHERE " +  stock_table['PRODUCT_ID'] + " =?;"
    fields = [id]
    id = executeQuery(stmt, fields)
    #removes item from stock
    #only callable through decreaseQty
    #otherwise flag would be neccessary to see if it has been added to history yet
    return id


#Helper functions
#------------------------------------------------------------------------------------------------------------
def filterData(data):
    months = []
    rates = []
    for row in data:
        months.append(monthToString(whichMonth(row[history_table['ADDED']], row[history_table['REMOVED']])))
        rates.append(row[history_table['ACTUAL_RATE']])
    print("Months: " , months)
    print("Rates: " , rates)
    return months, rates

def isEnoughEntries(id):
    months, rates = getProductHistory(id)
    if len(months) >= value_constants['DATA_LIMIT']:
        return True
    else:
        return False

def isFirstPrediction(id, month):
    data = getEstimation(id, month)
    if len(data) == 0:
        return True
    else:
        return False

def monthToString(date):
    return date.strftime("%B")

def stringToMonth(dateStr):
    return datetime.strptime(str(dateStr), '%Y-%m-%d %H:%M:%S.%f')

def whichMonth(dateAdded, dateRemoved):
    #print("Added " + dateAdded)
    #print("Removed " + dateRemoved)
    dateAdded = stringToMonth(dateAdded)
    dateRemoved = stringToMonth(dateRemoved)
    lastDayofMonth = calendar.monthrange(dateAdded.year, dateAdded.month)[1]
    #At what month did the consumption mainly occur? 
    if (lastDayofMonth - dateAdded.day) > dateRemoved.day:
        return dateAdded
    else:
        return dateRemoved

#Added, removed are datetime objects 
#retrived from product history table
#TODO: set to 1 if rate is 0 to avoid errors
def calculateRate(added, removed):
    return (removed - added).days

def convertMonthsToInt(months):
    monthIDs = []
    for month in months:
        monthIDs.append(getMonthID(month))
    return monthIDs











