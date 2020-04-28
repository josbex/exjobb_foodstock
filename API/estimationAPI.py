from API.util import db_constants
import API.naiveBayes
import flask
from flask import request, jsonify
import sqlite3
from datetime import datetime
import calendar

@app.route('/', methods=['POST', 'GET'])
def index():
    return null

def makePrediction(id, month):
    data = getProductHistory(id)
    months = data.values()
    rates = data.keys()
    predictedRate = API.naiveBayes.makePrediction(API.naiveBayes.trainModel(months, rates), month)
    return predictedRate

def updateEstimation(id, month):
    month_stmt = "SELECT " +  API.util.months_table['MONTH_ID'] + " FROM " + API.util.db_constants['MONTHS_TABLE'] + " WHERE " +  API.util.months_table['MONTH_NAME'] + "=?"
    month_field = [month]
    month_data = API.util.getData(month_stmt, month_field)
    stmt = "UPDATE " + API.util.db_constants['ESTIMATIONS_TABLE'] + " WHERE " +  API.util.estimation_table['MONTH_ID'] + "=? AND " +  API.util.estimation_table['PRODUCT_ID'] + "=?"
    fields = [month_data['id'], id]
    lastrowid = API.util.executeQuery(stmt, fields)
    return lastrowid

def getProductHistory(id):
    stmt = "SELECT * FROM " + API.util.db_constants['PRODUCT_HISTORY_TABLE'] + "wHERE " +  API.util.history_table['PRODUCT_ID'] + "=?"
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
def sendPrediction():
    return null

def addNewProduct():
    return null

def addToStock(id):
    return null

def removeFromStock(id, qty):
    return null

def updateHistory(id,added, removed, rate):
    return null

#Added, removed are datetime objects 
#retrived from product history table
def calculateRate(added, removed):
    return (removed - added).days


