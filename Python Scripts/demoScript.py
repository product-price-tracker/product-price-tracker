import keepa

secureKey = open("secureKey.txt", 'r').read()
api = keepa.Keepa(secureKey)

product = api.query("B0775451TT")

product[0].keys() # pulls all the keys in the data object

print("Manufacturer: " + product[0]["manufacturer"])
print("Title:" + product[0]["title"])

# only works if matplotlib is installed
#keepa.plot_product(product[0])