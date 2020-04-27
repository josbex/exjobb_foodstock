from API.util import db_constants
import API.naiveBayes
import flask
from flask import request, jsonify
import sqlite3

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
    #TODO: Filter data into rate, month dictionary
    return data

def sendPrediction():
    return null

#Functions for webpage 
#--------------------------------------------------------------------


