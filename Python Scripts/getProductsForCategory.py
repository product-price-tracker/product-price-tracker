import keepa
from getAccessKey import getAccessKey
from getProductData import get_data_for_product

def getProductsForCategory(rootCategory=172282, number_of_products=50): # page size in range of [50, 10000]
    accesskey = getAccessKey()
    api = keepa.Keepa(accesskey)
    product_parms = {'rootCategory': rootCategory,
                     "page": 0,
                     "perPage": number_of_products,}
    # A list of all the product ASINs
    products = api.product_finder(product_parms)

    #print(products)
    return products

def getProductDataForASINs(asins):
    dfs = {}
    for asin in asins:
        dfs[asin] = get_data_for_product(asin, plot=False)
        dfs[asin].to_pickle('../Data/{}.pkl'.format(str(asin)))

def getProductDataForCategory(rootCategory=172282, number_of_products=50):
    getProductDataForASINs(getProductsForCategory(rootCategory, number_of_products))

if __name__ == "__main__":
    getProductDataForCategory()
