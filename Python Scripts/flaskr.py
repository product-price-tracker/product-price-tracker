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
    predictor = request.args['predictor']
    if predictor == 'Machine Learning': # ML Model
        predictions, mse = predict_upcoming_prices(days_ahead=int(request.args['daysAhead']), time_steps=100, num_epochs=5, price=price, asin=asin)
        lower_ci = []
        upper_ci = []
        predicting_other_prices=True
    else: # "Bayesian" Statistical Model
        predictions, mse, lower_ci, upper_ci = predictBayes(request.args['asin'], daysAhead=int(request.args['daysAhead']), price=request.args['price'])
        predicting_other_prices=False

        # Get plottable CIs
        _, _, _, prediction_values = get_plottable_data_and_predictions(lower_ci, asin, predicting_other_prices=predicting_other_prices)
        lower_ci = [float(n) for n in prediction_values]

        _, _, _, prediction_values = get_plottable_data_and_predictions(upper_ci, asin, predicting_other_prices=predicting_other_prices)
        upper_ci = [float(n) for n in prediction_values]

    # Get plottable mean prices
    data_times, data_values, prediction_times, prediction_values = get_plottable_data_and_predictions(predictions, asin, predicting_other_prices=predicting_other_prices)
    data_times = [int(time.mktime(n.timetuple())) for n in data_times]
    data_values = [float(n) for n in data_values]
    prediction_times = [int(time.mktime(n.timetuple())) for n in prediction_times]
    prediction_values = [float(n) for n in prediction_values]



    return {'data_times': list(data_times), 'data_values': list(data_values),
            'prediction_times': list(prediction_times), 'prediction_values': list(prediction_values),
            'mse': mse, 'lower_ci': list(lower_ci), 'upper_ci': list(upper_ci)}

@app.route('/most-underpriced') # takes a category ID, gets top n underpriced items
@cross_origin()
def most_underpriced():
    return jsonify(mostUnderpriced(getProductsForCategory(request.args['catid'])))

@app.route('/price-data')
@cross_origin()
def price_data():
    obj = json.loads(get_clean_data_for_product(request.args['asin']).to_json(orient='index'))

    return {'data': [obj[str(key)] for key in sorted([int(k) for k in obj.keys()])]}

# @app.route('/predict-bayes')
# @cross_origin()
# def predict_bayes():
#     return str(predictBayes(asin=request.args['asin'], daysAhead=request.args['daysAhead'], price=price = request.args['price']))
