import keepa
import pandas
from getAccessKey import getAccessKey
from cleanProductData import get_clean_data_for_product

def predictBayes(asin): # predict one year from now

    df = get_clean_data_for_product(asin)
    dflength = len(df) - 1

    if dflength == -1:
        print("No price data for the product: " + asin)
        return -1
    elif dflength < 1095:
        print("Not enough price data for product " + asin + ". At least 3 years of data required")
        return -1
    else:
        return analyzeBayes(df)

def analyzeBayes(priceData):

    thisYear = priceData.tail(365)
    #print(thisYear[0:30])
    #print(thisYear[-30:])
    thisYearPrice = thisYear['NEW'].mean()
    thisMonthPrice = thisYear['NEW'][-30:].mean()
    thisDiff = thisMonthPrice - thisYearPrice

    lastYear = priceData.tail(730)[0:365]
    #print(lastYear[0:30])
    #print(lastYear[-30:])
    lastYearPrice = lastYear['NEW'].mean()
    prevMonthPrice = lastYear['NEW'][-30:].mean()
    prevDiff = prevMonthPrice - lastYearPrice

    thirdYearBack = priceData.tail(1095)[0:365]
    thirdYearPrice = thirdYearBack['NEW'].mean()
    thirdYMonthPrice = thirdYearBack['NEW'][-30:].mean()
    thirdYDiff = thirdYMonthPrice - thirdYearPrice

    yearlyChangeFactor = thisYearPrice - lastYearPrice - (lastYearPrice - thirdYearPrice)
    nextYearsPrice = thisYearPrice + (thisYearPrice - lastYearPrice) + yearlyChangeFactor
    diffFactor = thisDiff - prevDiff - (prevDiff - thirdYDiff)
    nextDiff = thisDiff + (thisDiff - prevDiff) + diffFactor
    #nextYearsPrice = lastYearPrice + 2*(thisYearPrice - lastYearPrice) # extend yearly avg price trend
    #nextDiff = prevDiff + 2*(thisDiff - prevDiff) # extend monthly variance from yearly avg price

    return nextYearsPrice + nextDiff # prediction

if __name__ == "__main__":
    print(predictBayes('B0001ARCFA'))#B0775451TT'))
