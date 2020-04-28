from flask import Flask, render_template, url_for, request, redirect, jsonify
import estimationAPI as eAPI
import util as u


app = Flask(__name__)

@app.route('/', methods=['POST', 'GET'])
def index():
    stmt = "SELECT * FROM " +  u.db_constants['STOCK_TABLE']
    items = u.getData(stmt, [])
    return render_template('index.html', items=items)

#def displaStock():
#    return null


if __name__ == '__main__':
	app.run(debug=True)