# product-price-tracker
A tool for predicting prices of Amazon Products.

# Getting Set up for dev:
1. Run ``virtualenv -p `which python3` env`` in root directory of project to create virtual environment.
2. Run `source env/bin/activate` to enter your virtual environment. Do this every time you wish to enter it for development.
  * If you want to exit the virtual environment, run `deactivate`.
3. Run `pip install -r requirements.txt` to download all dependencies for project.
4. Start Coding!
5. If you install any additional dependencies, run `pip freeze > requirements.txt` to keep track of the libraries in your updated environment.

# Structure of Data:

```
{ 
  Price: number[],
  Category: string,
  Reviews: Review[],
  Average Current Rating: number,
  Number of Ratings: number,
  ASIN: string,
  Amazon Name: string,
  Date first Listed: date,
  Manufacturer: string,
  Item Weight: number,
  Dimensions: number[],

}
```

We have a number of Python files with functions that perform analyses on
 any given Amazon product. Most of these take as a parameter an ASIN or other
 Amazon identifier, but also can be run as scripts that perform the same
 function on a default product or category.
As of November 4, we have the following functions:

getAccessKey:
	Our system makes use of the Keepa API for getting our Amazon price data.
	This function reads a file for the secure key needed to access the
	 Keepa API.

getProductData:
	This function gets all historical price data for the input ASIN
	 on one-day intervals.

getProductsForCategory:
	This function returns the ASINs of all products in a category specified
	 by the Amazon Category ID input.

predictNextPrice:


ratePrice:
	For the ASIN input, this function calculated a historical average price,
	 and returns a rating of the current price in reference to the historical
	 price. The rating is simply currentPrice / historicalMeanPrice. A lower
	 rating implies a better current price for a buyer.
	If the price dataset received is empty, returns -1.

getMostUnderpriced:
	Takes a list of ASINs and ranks the products by price rating as per the
	 ratePrice method. Returns a list of pairs (ASIN, priceRating) ordered
	 by priceRating ascending (best deals first). If ratePrice returns -1
	 for any ASIN, i.e. no price data is received, then that result is omitted.

mainScript:
	Runs a command-line interface from which functions can be called.
	Syntax is "py mainScript.py <command> <ASIN> <time>"
