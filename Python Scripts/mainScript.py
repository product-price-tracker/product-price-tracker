#python mainScript.py <command> <ASIN> [category] [numProducts] [-h]

import argparse #command-line parsing module

from ratePrice import rate_price
from getProductsForCategory import getProductDataForCategory

parser = argparse.ArgumentParser()

parser.add_argument("command", choices=['ratePrice', 'catProducts'], help="command to be run - required")
parser.add_argument("ASIN", help="the ASIN of interest")
parser.add_argument("category", default=0, nargs='?', help="the root category of products")
parser.add_argument("numProducts", default=0, nargs='?', help="number of products to a page")

args = parser.parse_args()

if (args.command == "ratePrice"):
    print(rate_price(args.ASIN))
elif(args.command == "catProducts"):
    getProductDataForCategory(args.category, args.numProducts)