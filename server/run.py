from flask import Flask, render_template
from ratePrice import rate_price

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/rate')
def rate():
    return rate_price(request.args['asin'])

@app.route('/predict')
def predict():
    pass