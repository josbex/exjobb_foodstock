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
    month_stmt = "SELECT id FROM " + API.util.db_constants['MONTHS_TABLE'] + " WHERE month=?"
    month_field = [month]
    month_data = API.util.getData(month_stmt, month_field)
    stmt = "UPDATE " + API.util.db_constants['ESTIMATIONS_TABLE'] + " WHERE month_id=? AND product_id=?"
    fields = [month_data['id'], id]
    lastrowid = API.util.executeQuery(stmt, fields)
    return lastrowid

def getProductHistory(id):
    stmt = "SELECT * FROM " + API.util.db_constants['PRODUCT_HISTORY_TABLE'] + "wHERE product_id=?" #TODO: make constants of db columns.
    field = [id]
    data = API.util.getData(stmt, field)
    return data

def sendPrediction():
    return null

#Functions for webpage 
#--------------------------------------------------------------------


