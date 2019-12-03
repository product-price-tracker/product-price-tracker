import keepa
import pandas
import numpy
from getAccessKey import getAccessKey
from ratePrice import rate_price
from getProductsForCategory import getProductsForCategory

# for a set of ASINs, get the top n most underpriced

def mostUnderpriced(asins, n = 10):

    ratings = []

    for asin in asins:
        priceRating = rate_price(asin)
        if priceRating > -1:
            ratings.append((asin, priceRating))

    #print(ratings)
    ratings.sort(reverse=False, key=lambda tup: tup[1])
    return ratings[0:n-1]

if __name__ == "__main__":
    print(mostUnderpriced(getProductsForCategory()[0:19])) # gets default list of electronics products
    #print(mostUnderpriced(['B01J4GCK1W', 'B07JQ5WTZL']))
