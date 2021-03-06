import keepa
import pandas
import globals
from getAccessKey import getAccessKey
from cleanProductData import get_clean_data_for_product

# for any ASIN, say whether it is under or overpriced

def rate_price(asin):

    df = get_clean_data_for_product(asin)
    dflength = len(df) - 1

    if dflength == -1:
        print("No price data for the product: " + asin)
        return -1
    else:
        currentPrice = df.at[dflength, 'MIN_UNUSED']
        meanHistoryPrice = df.loc[:, 'MIN_UNUSED'].mean()
        globals.rating = currentPrice / meanHistoryPrice
        return currentPrice / meanHistoryPrice

def current_price(asin):
    df = get_clean_data_for_product(asin)
    return df.at[len(df) - 1, 'MIN_UNUSED']

def mean_history_price(asin):
    df = get_clean_data_for_product(asin)
    return df.loc[:, 'MIN_UNUSED'].mean()

if __name__ == "__main__":
    print(rate_price('B0775451TT'))
