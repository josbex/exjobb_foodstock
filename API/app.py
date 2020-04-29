from flask import Flask, render_template, url_for, request, redirect, jsonify
from estimationAPI import stringToMonth, addNewProduct
from extras import getData, db_constants


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
        print(items)
        return render_template('index.html', items=items)

#def displaStock():
#    return null


if __name__ == '__main__':
	app.run(debug=True)