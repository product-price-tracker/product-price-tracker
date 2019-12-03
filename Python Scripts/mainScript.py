#python mainScript.py <command> <ASIN or "category"> <time period> [number of products] [-h]

import argparse #command-line parsing module

from ratePrice import rate_price
from getProductsForCategory import getProductDataForCategory
from predictSequence import predict_upcoming_prices, plot_data_and_predictions

parser = argparse.ArgumentParser()

parser.add_argument("command", choices=['historic', 'predict'], help="command to be run (required)")
parser.add_argument("ASIN", help="the ASIN of interest, or 'category' to enter a category")
parser.add_argument("time", choices=['day', 'week', 'month', 'year'], help="time period to predict")
parser.add_argument("numProducts", default=50, nargs='?', help="number of products (default 50)")

args = parser.parse_args()

numDays = 1
if (args.time == 'day'):
    numDays = 1
elif (args.time == 'week'):
    numDays = 7
elif (args.time == 'month'):
    numDays = 30 #assume 30-day month
elif (args.time == 'year'):
    numDays = 365

asinIsCategory = False
if (args.ASIN == "category"):
    cat = input("Enter root category number:")
    asinIsCategory = True

if (args.command == "historic"):
    print(rate_price(args.ASIN))
elif (args.command == "historic" and asinIsCategory == True):
    getProductDataForCategory(cat, args.numProducts)
elif (args.command == "predict"):
       price='NEW'
       predictions = predict_upcoming_prices(days_ahead=5, time_steps=365, num_epochs=10, price=price, asin=args.ASIN)
       plot_data_and_predictions(predictions, asin=args.ASIN, price=price)
       min_pred = min(predictions)
       print('Minimum price of ${} in {} days from now.'.format(min_pred, predictions.index(min_pred)+1))
