from flask import Flask, request, render_template, jsonify
from flask_cors import CORS, cross_origin
from pandas import DataFrame
import json
import time

from ratePrice import rate_price
from getProductsForCategory import getProductsForCategory
from getMostUnderpriced import mostUnderpriced
from cleanProductData import get_clean_data_for_product
from predictSequence import get_plottable_data_and_predictions, predict_upcoming_prices
from predictBayes import predictBayes

import configparser

config = configparser.ConfigParser()
app = Flask(__name__)
CORS(app)

@app.route('/')
@cross_origin()
def index():
    return 'Hello!'

@app.route('/rate')
@cross_origin()
def rate():
    return str(rate_price(request.args['asin']))

@app.route('/predict')
@cross_origin()
def predict():
    asin = request.args['asin']
    price = request.args['price']
    predictions, mae = predict_upcoming_prices(days_ahead=int(request.args['daysAhead']), time_steps=100, num_epochs=20, price=price, asin=asin)
    data_times, data_values, prediction_times, prediction_values = get_plottable_data_and_predictions(predictions, asin)
    data_times = [int(time.mktime(n.timetuple())) for n in data_times]
    data_values = [float(n) for n in data_values]
    prediction_times = [int(time.mktime(n.timetuple())) for n in prediction_times]
    prediction_values = [float(n) for n in prediction_values]
    return {'data_times': data_times, 'data_values': data_values, 'prediction_times': prediction_times, 'prediction_values': prediction_values, 'mae': mae}

@app.route('/most-underpriced') # takes a category ID, gets top n underpriced items
@cross_origin()
def most_underpriced():
    return jsonify(mostUnderpriced(getProductsForCategory(request.args['catid'])))

@app.route('/price-data')
@cross_origin()
def price_data():
    obj = json.loads(get_clean_data_for_product(request.args['asin']).to_json(orient='index'))

    return {'data': [obj[str(key)] for key in sorted([int(k) for k in obj.keys()])]}

@app.route('/predict-bayes')
@cross_origin()
def predict_bayes():
    return str(predictBayes(request.args['asin']))
