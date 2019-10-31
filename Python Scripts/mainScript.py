#python mainScript.py <command> <ASIN or "category"> <time period> [number of products] [-h]

import argparse #command-line parsing module

from ratePrice import rate_price
from getProductsForCategory import getProductDataForCategory
from predictNextPrice import predict_upcoming_prices

parser = argparse.ArgumentParser()

parser.add_argument("command", choices=['historic', 'predict', 'predictSequence', 'findFutureMin'], help="command to be run - required")
parser.add_argument("ASIN", help="the ASIN of interest")
parser.add_argument("time", choices=['day', 'week', 'month', 'year'], help="the root category of products")
parser.add_argument("numProducts", default=50, nargs='?', help="number of products")

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

bool asinIsCategory = False
if (args.ASIN == "category"):
    cat = input("Enter root category number:")
    asinIsCategory = True

if (args.command == "historic"):
    print(rate_price(args.ASIN))
elif(args.command == "historic" and asinIsCategory == True):  
    getProductDataForCategory(cat, args.numProducts)
elif(args.command == "predict"):
    predict_upcoming_prices(numDays, 150, 10, args.ASIN, price='NEW')
elif(args.command == "predictSequence"):
elif(args.command == "findFutureMin"):