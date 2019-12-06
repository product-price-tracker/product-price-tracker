import keepa
import pandas
import numpy
import statsmodels.api as sm
from getAccessKey import getAccessKey
from cleanProductData import get_clean_data_for_product

def predictBayes(asin, daysAhead=60, price='NEW'):

    df = get_clean_data_for_product(asin)
    dflength = len(df) - 1

    if dflength == -1:
        print("No price data for the product: " + asin)
        return -1
    else:
        return analyzeBayes(df, daysAhead, price)

def analyzeBayes(priceData, daysAhead, price):
    y = priceData[price]
    x = list(priceData.index)
    x = sm.add_constant(x)
    model = sm.OLS(y, x).fit()
    model.predict(x)
    daysFromStart = int(x[-1][1])
    pastPrediction = model.get_prediction(x).summary_frame(alpha=0.05)
    predictions = model.get_prediction(mutate(x, daysAhead)).summary_frame(alpha=0.05)
    #print(predictions[['mean', 'obs_ci_lower']])
    results = (predictions[['mean', 'obs_ci_lower','obs_ci_upper']], pastPrediction['mean_se'])
    return results

def mutate(x, daysAhead):
    arr = []
    end = int(x[-1][1])
    for i in range(end+1, end+1+daysAhead):
        arr.append([1.0, i])
    return numpy.array(arr)

def analyzeBayes1(priceData):

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
    #x = [[1, 20], [1, 21], [1, 22]]
    #print(mutate(x, 3))
    print(predictBayes('B0001ARCFA')) #'B0775451TT'
