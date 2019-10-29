import keepa
import pandas
from getAccessKey import getAccessKey
from getProductData import get_data_for_product

# for any ASIN, say whether it is under or overpriced

def rate_price(asin):

    df = get_data_for_product(asin, plot=False)
    dflength = len(df) - 1

    if dflength == -1:
        print("Error: no price data for the product: " + asin)
    else:
        currentPrice = df.at[dflength, 'NEW']
        meanHistoryPrice = df.loc[:, 'NEW'].mean()
        return currentPrice / meanHistoryPrice

def current_price(asin):
    df = get_data_for_product(asin)
    return df.at[len(df) - 1, 'NEW']

def mean_history_price(asin):
    df = get_data_for_product(asin)
    return df.loc[:, 'NEW'].mean()

if __name__ == "__main__":
    print(rate_price('B0775451TT'))

