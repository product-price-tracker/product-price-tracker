import keepa
import matplotlib.pyplot as plt

from getAccessKey import getAccessKey


def get_data_for_product(asin):
    accesskey = getAccessKey()
    print(accesskey)
    api = keepa.Keepa(accesskey)

    products = api.query()

    print(products[0].keys())
