from flask import Flask, render_template, url_for, request, redirect, jsonify
from estimationAPI import stringToMonth, addNewProduct
from extras import getData, db_constants, product_table, stock_table


app = Flask(__name__)

@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        product_name = request.form['name']
        product_created = request.form['created']
        product_expires = request.form['expires']
        product_qty = request.form['qty']
        product_created = stringToMonth(product_created)
        product_expires = stringToMonth(product_expires)
        addNewProduct(product_name, product_created, product_expires, int(product_qty))
        return redirect('/')
    else:
        stmt = "SELECT * FROM " +  db_constants['STOCK_TABLE']
        items = getData(stmt, [])
        items = displayStock(items)
        print(items)
        return render_template('index.html', items=items)

def displayStock(items):
    stmt = "SELECT "+ product_table['PRODUCT_NAME'] + " FROM " + db_constants['PRODUCT_TABLE'] + " WHERE "
    fields = []
    for item in items:
        stmt+= product_table['ID'] + " = ? OR "
        fields.append(item[stock_table['PRODUCT_ID']])
    stmt = stmt[:-4] + ';'
    print(stmt)
    nameItems = getData(stmt, fields)
    print(nameItems)
    items = mergeItems(nameItems, items)
    return items

def mergeItems(nameItems, items):
    i = 0
    for name in nameItems:
        print(name['name'])
        print(items[i])
        items[i]['name'] = name['name']
        i+=1
    return items

if __name__ == '__main__':
	app.run(debug=True)