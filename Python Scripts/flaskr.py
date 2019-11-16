from flask import Flask, render_template
from ratePrice import rate_price
import configparser
":{?>P:{?}

config = configparser.ConfigParser()
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

if __name__ == '__main__':
    app.run(**config['app'])