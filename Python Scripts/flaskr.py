from flask import Flask, request, render_template, jsonify
from flask_cors import CORS
from pandas import DataFrame

from ratePrice import rate_price
from getProductsForCategory import getProductsForCategory
from getMostUnderpriced import mostUnderpriced
from getProductData import get_data_for_product

import configparser

config = configparser.ConfigParser()
app = Flask(__name__)
CORS(app)

@app.route('/')
def index():
    return 'Hello!'

@app.route('/rate')
def rate():
    return str(rate_price(request.args['asin']))

@app.route('/predict')
def predict():
    pass

@app.route('/most-underpriced') # takes a category ID, gets top n underpriced items
def most_underpriced():
    return jsonify(mostUnderpriced(getProductsForCategory(request.args['catid'])))

@app.route('/price-data')
def price_data():
    return get_data_for_product(request.args['asin']).to_json(orient='index')
