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
