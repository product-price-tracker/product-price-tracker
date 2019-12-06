# product-price-tracker
A tool for predicting prices of Amazon Products.

# Getting Set up for dev:
1. Run ``virtualenv -p `which python3` env`` in root directory of project to create virtual environment.
2. Run `source env/bin/activate` to enter your virtual environment. Do this every time you wish to enter it for development.
  * If you want to exit the virtual environment, run `deactivate`.
3. Run `pip install -r requirements.txt` to download all dependencies for project.
4. Start Coding!
5. If you install any additional dependencies, run `pip freeze > requirements.txt` to keep track of the libraries in your updated environment.

# Running the CLI:
1. In a command line, navigate to `Python Scripts`
2. Run `python mainScript` with appropriate arguments. Running with no arguments will give help on what arguments are possible.

# Running the Web App:
## Running the Front End
1. Make sure Node/NPM are installed on your computer from https://nodejs.org/en/download/
2. Navigate into `Frontend/ppt-frontend`
3. Run `npm install` to install dependencies
4. Run `npm run serve` to run the server! The terminal output should say on which IP/port the server is running. By default, you can access it at `localhost:8080`.

## Running the Back End
1. Create and activate the python environment as specified above in *Getting Set up for dev*.
2. Navigate into `Python Scripts`
3. Run `source configFlaskMac.bat` on Mac or `configFlaskWind.bat` on Windows to run the server!. *Note*: Currently, the server must be run on the port 5000 (default) on the same IP as the front end in order for the front end to be able to communicate with the back end. 


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
As of November 4, we have the following scripts:

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
  The purpose of this script is to make multiple predictions, one for each
    day from 1 to n days in the future using an LSTM. Doing this, we create a
    sequence of predicted prices for the next n days in the future, and can
    predict both the minimum and maximum prices and when they will occur within
    this time period.

predictSequence:
 The purpose of this script is to make a single prediction of the sequence of
   next prices. Doing this, we create a sequence of predicted prices for the
   next n days in the future, and can use this prediction to predict both the
   minimum and maximum prices and when they will occur within this time period.
   Outputs prediction and MSE.

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

predictBayes:
  Uses a linear point estimation to predict the sequence of next prices for n
    days in the future, which we can use to predict both the maximum and minimum
    prices and when they will occur. Outputs the prediction, MSE, along with 95%
    CIs for the prediction.

mainScript:
	Runs a command-line interface from which functions can be called.
	Syntax is "python mainScript.py <command> <ASIN or "category"> <time period> [number of products] [-h]".  
	Run "python mainScript.py -h" for help.
