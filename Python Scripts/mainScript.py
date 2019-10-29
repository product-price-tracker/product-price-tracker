#python mainScript.py <command> <ASIN or "category"> <time period> [optional detail] [-h]

import argparse #command-line parsing module

from ratePrice import rate_price
from getProductsForCategory import getProductDataForCategory

parser = argparse.ArgumentParser()

parser.add_argument("command", choices=['historic', 'data', 'predict', 'findFutureMin'], help="command to be run - required")
parser.add_argument("ASIN", help="the ASIN of interest")
parser.add_argument("time", choices=['day', 'week', 'month', 'year'], help="the root category of products")
parser.add_argument("details", default=0, nargs='?', help="number of products to a page")

args = parser.parse_args()

bool asinIsCategory = False
# Lee to do - add check so that user can input 'category' instead of an ASIN and receive a prompt to enter the category
# (from there they can receive information about the items in that category)

if (args.command == "historic"):
    print(rate_price(args.ASIN))
elif(args.command == "historic"):  # check that asinIsCategory is equal to true
    getProductDataForCategory(args.category, args.numProducts)