import keepa
import matplotlib.pyplot as plt
import pandas as pd
import datetime

from getAccessKey import getAccessKey

from pandas.plotting import register_matplotlib_converters

register_matplotlib_converters()

def get_data_for_product(asin, plot=True):
    accesskey = getAccessKey()
    api = keepa.Keepa(accesskey)

    products = api.query(asin)
    history = products[0]['data']
    data = {}

    # keepa.plot_product(products[0])
    base_key = 'AMAZON' # Whatever key we're using to set the time
    start_time = history[base_key + '_time'][0].replace(microsecond=0,second=0,minute=0,hour=0)
    end_time = history[base_key + '_time'][-1].replace(microsecond=0,second=0,minute=0,hour=0)

    potential_keys = ['AMAZON', 'NEW', 'USED', 'SALES', 'COUNT_NEW', 'COUNT_USED', 'LISTPRICE', 'RATING', 'COUNT_REVIEWS']

    for key in potential_keys:
        if key not in history:
            continue
        # plt.step(history[key], history[key + '_time'], where='pre')

        time = start_time
        furthest_time_index = 0
        data[key] = []
        data[key + '_time'] = []
        while time < end_time:
            # Find latest price update for this day, and set that as the price for this day.
            while furthest_time_index < len(history[key + '_time']) and history[key + '_time'][furthest_time_index] < time + datetime.timedelta(days=1):

                furthest_time_index += 1

            data[key].append(history[key][furthest_time_index-1])
            data[key + '_time'].append(time)
            time += datetime.timedelta(days=1)

        # print(data[key])
        # print(data[key + '_time'])
        if plot:
            plt.figure(figsize=(16, 8))
            plt.xlabel('Time')
            plt.ylabel(key)
            plt.title(key + ' over Time')
            plt.plot(data[key + '_time'], data[key])
            plt.show()

    df = pd.DataFrame()
    for key in potential_keys:
        if key in data:
            df[key] = data[key]
            df['Time'] = data[key + '_time']

    print(df.head(100))
    return df



    # print(products[0]['data'].keys())
    # print(len(products[0]['data']['AMAZON']))
    # print(len(products[0]['data']['AMAZON_time'])) # _times correspond to the price it changed to at that time.
    # Make our predictions correspod to the start of discrete, unfiorm time periods





    # df = pd.read_csv(products[0]['data']))
    # print(df)

if __name__ == "__main__":
    get_data_for_product('B0047E0EII')

'''
dict_keys(['csv', 'categories', 'imagesCSV', 'manufacturer', 'title', 'lastUpdate', 'lastPriceChange', 'rootCategory', 'productType', 'parentAsin', 'variationCSV', 'asin', 'domainId', 'type', 'hasReviews', 'ean', 'upc', 'mpn', 'trackingSince', 'brand', 'label', 'department', 'publisher', 'productGroup', 'partNumber', 'studio', 'genre', 'model', 'color', 'size', 'edition', 'platform', 'format', 'packageHeight', 'packageLength', 'packageWidth', 'packageWeight', 'packageQuantity', 'isAdultProduct', 'isEligibleForTradeIn', 'isEligibleForSuperSaverShipping', 'offers', 'buyBoxSellerIdHistory', 'isRedirectASIN', 'isSNS', 'author', 'binding', 'numberOfItems', 'numberOfPages', 'publicationDate', 'releaseDate', 'languages', 'lastRatingUpdate', 'ebayListingIds', 'lastEbayUpdate', 'eanList', 'upcList', 'liveOffersOrder', 'frequentlyBoughtTogether', 'features', 'description', 'hazardousMaterialType', 'promotions', 'newPriceIsMAP', 'coupon', 'availabilityAmazon', 'listedSince', 'fbaFees', 'variations', 'itemHeight', 'itemLength', 'itemWidth', 'itemWeight', 'stats', 'offersSuccessful', 'g', 'categoryTree', 'data'])
'''
