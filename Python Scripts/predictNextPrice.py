
import keras
import pandas as pd
import numpy as np

from keras.layers import Input, LSTM, Dense, Activation
from keras.models import Model
from keras.regularizers import l2

from sklearn.preprocessing import MinMaxScaler

import datetime

import matplotlib.pyplot as plt

from getProductData import save_data_for_product
from cleanProductData import save_clean_data_for_product

import os


def createNextPriceModel(n_input, n_output, time_steps=50, lstm_units=2, reg_param=1e-4):
    print(time_steps)
    print(n_input)
    in_layer = Input((time_steps, n_input))
    lstm = LSTM(lstm_units, return_sequences=False, activity_regularizer=l2(reg_param), dropout=0.0)(in_layer)
    # lstm = LSTM(lstm_units, return_sequences=False, activity_regularizer=l2(reg_param), dropout=0.0)(lstm)
    # lstm = LSTM(lstm_units*100, return_sequences=False, activity_regularizer=l2(reg_param), dropout=0.1)(lstm)
    dense = Dense(n_output)(lstm)
    activation = Activation('linear')(dense)

    model = Model(in_layer, [activation])

    model.compile(optimizer='adam', loss='mse')

    return model

def trainNextPriceModel(model, x_train, y_train, num_epochs=10):
    model.fit(x_train, y_train, epochs=num_epochs, validation_split=0.2)
    return model

def getProductDf(productDf, price='NEW'):
    # print(productDf)
    # TODO: implement MIN_UNUSED
    # productDf['MIN_UNUSED'] = np.min(productDf['NEW'], productDf['AMAZON'])
    y = np.array(productDf['Next '+price]).reshape(len(productDf['Next '+price]),1)
    # print(y_train[50:60])
    # print(np.array(productDf['NEW'][50:60]))

    x_cols = ['AMAZON', 'NEW', 'SALES']
    x = np.zeros((len(y), len(x_cols)))
    for i in range(len(x_cols)):
        x[:, i] = productDf[x_cols[i]]

    return x, y

def getSequencesFromData(x_raw, y_raw, time_steps, train_split=0.8):

    num_sequences = x_raw.shape[0]-time_steps+1
    if (num_sequences <= 0):
        print(x_raw.shape)
        print(num_sequences)
        assert num_sequences > 0
    x = np.zeros((num_sequences, time_steps, x_raw.shape[1]))
    y = np.zeros((num_sequences, y_raw.shape[1]))

    for offset in range(num_sequences):
        x[offset,:,:] = x_raw[offset:offset+time_steps,:]
        y[offset,:] = y_raw[offset+time_steps-1,:]

    # Splitting
    split_index = int(num_sequences*train_split)

    x_train = x[:split_index]
    x_test = x[split_index:]

    y_train = y[:split_index]
    y_test = y[split_index:]


    return x_train, y_train, x_test, y_test


def loadData(path):
    return pd.read_pickle(path)

def prepData(df, days_ahead=1, price='NEW'):
    df['Next '+price] = df[price].shift(-1*days_ahead)
    df = df.fillna(0)
    return df

def create_train_predict(path='../Data/Clean/B00BWU3HNY.pkl', time_steps=150, days_ahead=1, num_epochs=10, price='NEW'):
    df = loadData(path)
    df = prepData(df, days_ahead=days_ahead, price=price)

    x_raw, y_raw = getProductDf(df, price=price)
    # TODO: Fit on only train data!
    x_scaler = MinMaxScaler()
    y_scaler = MinMaxScaler()
    x_scaler.fit(x_raw)
    y_scaler.fit(y_raw)
    x = x_scaler.transform(x_raw)
    y = y_scaler.transform(y_raw)
    x_train, y_train, x_test, y_test = getSequencesFromData(x, y, time_steps = time_steps)


    n_input = x_train.shape[2]
    n_output = y_train.shape[1]

    model = createNextPriceModel(n_input, n_output, time_steps = time_steps)
    model = trainNextPriceModel(model, x_train, y_train, num_epochs=num_epochs)
    predictions = model.predict(x_test)


    scaled_predictions = y_scaler.inverse_transform(predictions)
    prediction = scaled_predictions[-1,0]
    return prediction


    # print(model.evaluate(x_test, y_test))

def predict_upcoming_prices(days_ahead=7, time_steps=150, num_epochs=10, asin='B00BWU3HNY', price='NEW'):
    path = '../Data/{}.pkl'.format(str(asin))
    clean_path = '../Data/Clean/{}.pkl'.format(str(asin))
    if not os.path.isfile(path):
        save_data_for_product(asin)
    if not os.path.isfile(clean_path):
        save_clean_data_for_product(asin)

    predictions = []
    for days_ahead in np.array(range(days_ahead))+1:
        print('Creating Model for {} days ahead.'.format(days_ahead))
        prediction = create_train_predict(path=clean_path, time_steps=time_steps, days_ahead=days_ahead, num_epochs=num_epochs, price=price)
        predictions.append(prediction)
    return predictions

def get_plottable_data_and_predictions(predictions, asin='B00BWU3HNY', price='NEW'):
    df = loadData('../Data/Clean/{}.pkl'.format(asin))
    # df = prepData(df)

    prediction_length = len(predictions)

    data_times = list(df['Time'])
    data_values = list(df[price])

    prediction_times = [data_times[-1] + datetime.timedelta(days=days) for days in range(prediction_length+1)]
    prediction_values = [data_values[-1]] + predictions

    return data_times, data_values, prediction_times, prediction_values

def plot_data_and_predictions(predictions, asin='B00BWU3HNY', price='NEW'):
    data_times, data_values, prediction_times, prediction_values = get_plottable_data_and_predictions(predictions, asin, price)

    print(prediction_values)

    plt.figure(figsize=(12,12))
    plt.title(price+' Prediction')
    plt.xlabel('Time')
    plt.ylabel(price+' Price')
    plt.plot(data_times, data_values, label='Data')
    plt.plot(prediction_times, prediction_values, label='Prediction')
    plt.legend()
    plt.show()

def main():
    price='NEW'
    asin='B0047E0EII'
    # predictions = predict_upcoming_prices(3, time_steps=365, num_epochs=10, price=price, asin=asin)
    predictions = predict_upcoming_prices(days_ahead=1, time_steps=100, num_epochs=3, price=price, asin=asin)

    plot_data_and_predictions(predictions, asin=asin, price=price)


if __name__ == "__main__":
    main()
