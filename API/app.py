from flask import Flask, render_template, url_for, request, redirect, jsonify
from estimationAPI import stringToMonth, addNewProduct, moveToHistory, predictRate, removeFromStock
from extras import getData, db_constants, product_table, stock_table, executeQuery, addMonths
from datetime import datetime


app = Flask(__name__)

@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        product_name = request.form['name']
        product_created = request.form['created']
        product_expires = request.form['expires']
        product_qty = request.form['qty']
        product_created = datetime.strptime(product_created, "%Y-%m-%d")
        product_expires = datetime.strptime(product_expires, "%Y-%m-%d")
        #product_created = stringToMonth(product_created)
        #product_expires = stringToMonth(product_expires)
        addNewProduct(product_name, product_created, product_expires, int(product_qty))
        return redirect('/')
    else:
        stmt = "SELECT * FROM " +  db_constants['STOCK_TABLE']
        items = getData(stmt, [])
        items = displayStock(items)
        #print(items)
        return render_template('index.html', items=items)

@app.route('/decrease/<int:id>')
def decreaseQty(id):
    #add to history
    stockInfo = moveToHistory(id)
    predictRate(id)
    #Check if there still is products left in stock
    if stockInfo[0][stock_table['QUANTITY']] > 1:
        updateStmt = "UPDATE " + db_constants['STOCK_TABLE'] + " SET " +  stock_table['QUANTITY'] + " = "+ stock_table['QUANTITY'] + " - 1  WHERE " +  stock_table['PRODUCT_ID'] + "=?;"
        updateFields = [id]
        id = executeQuery(updateStmt, updateFields)
    else:
        id = removeFromStock(id)
    return redirect('/')


def displayStock(items):
    stmt = "SELECT "+ product_table['PRODUCT_NAME'] + " FROM " + db_constants['PRODUCT_TABLE'] + " WHERE "
    fields = []
    for item in items:
        stmt+= product_table['ID'] + " = ? OR "
        fields.append(item[stock_table['PRODUCT_ID']])
    stmt = stmt[:-4] + ';'
    nameItems = getData(stmt, fields)
    items = mergeItems(nameItems, items)
    return items

def mergeItems(nameItems, items):
    i = 0
    for name in nameItems:
        items[i]['name'] = name['name']
        i+=1
    return items

if __name__ == '__main__':
	app.run(debug=True)