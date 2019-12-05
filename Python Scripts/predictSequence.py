
import keras
import pandas as pd
import numpy as np

from keras.layers import Input, LSTM, Dense, Activation
from keras.models import Model
from keras.regularizers import l2
from keras.optimizers import Adam

from sklearn.preprocessing import MinMaxScaler

import datetime

import matplotlib.pyplot as plt

from cleanProductData import get_clean_data_for_product

import os


def createSeq2SeqModel(n_input, n_output, time_steps=50, lstm_units=10, reg_param=1e-4):
    dropout = 0.5

    # Encoder
    encoder_inputs = Input(shape=(None, n_input))
    encoder = LSTM(lstm_units, dropout=dropout, return_state=True)
    encoder_outputs, state_h, state_c = encoder(encoder_inputs)

    encoder_states = [state_h, state_c]

    # Decoder
    decoder_inputs = Input(shape=(None, n_input))

    decoder_lstm = LSTM(lstm_units, dropout=dropout, return_sequences=True, return_state=True)
    decoder_outputs, _, _ = decoder_lstm(decoder_inputs, initial_state=encoder_states)

    decoder_dense = Dense(n_input) # Should be n_output??
    decoder_outputs = decoder_dense(decoder_outputs)

    model = Model([encoder_inputs, decoder_inputs], decoder_outputs)

    model.compile(optimizer='adam', loss='mse')


    encoder_model = Model(encoder_inputs, encoder_states)

    decoder_state_input_h = Input(shape=(lstm_units,))
    decoder_state_input_c = Input(shape=(lstm_units,))
    decoder_states_inputs = [decoder_state_input_h, decoder_state_input_c]

    decoder_outputs, state_h, state_c = decoder_lstm(decoder_inputs, initial_state=decoder_states_inputs)
    decoder_states = [state_h, state_c]
    decoder_outputs = decoder_dense(decoder_outputs)
    decoder_model = Model([decoder_inputs] + decoder_states_inputs, [decoder_outputs] + decoder_states)

    return model, encoder_model, decoder_model

def trainSeq2SeqModel(model, x_train, y_train, decoder_input, num_epochs=10, batch_size=128):
    model.fit([x_train, decoder_input], y_train, batch_size=batch_size, epochs=num_epochs, validation_split=0.2)
    return model

def getData(productDf, price='NEW'):
    # print(productDf)
    # y = np.array(productDf['Next '+price]).reshape(len(productDf['Next '+price]),1)
    # print(y_train[50:60])
    # print(np.array(productDf['NEW'][50:60]))

    cols = ['AMAZON', 'NEW', 'SALES', 'MIN_UNUSED']
    data = np.zeros((len(productDf.index), len(cols)))
    for i in range(len(cols)):
        data[:, i] = productDf[cols[i]]

    return data

def getSequencesFromData(data, time_steps, days_ahead, train_split=0.8):

    num_sequences = data.shape[0]-time_steps-days_ahead+1
    if (num_sequences <= 0):
        print(data.shape)
        print(num_sequences)
        assert num_sequences > 0
    x = np.zeros((num_sequences, time_steps, data.shape[1]))
    y = np.zeros((num_sequences, days_ahead, data.shape[1]))

    for offset in range(num_sequences):
        x[offset,:,:] = data[offset:offset+time_steps,:]
        y[offset,:,:] = data[offset+time_steps:offset+time_steps+days_ahead,:]

    # Splitting
    split_index = int(num_sequences*train_split)

    x_train = x[:split_index]
    x_test = x[split_index:]

    y_train = y[:split_index]
    y_test = y[split_index:]


    return x_train, y_train, x_test, y_test

def prepData(df, days_ahead=1, price='NEW'):
    df['Next '+price] = df[price].shift(-1*days_ahead)
    df = df.fillna(0)
    return df

def create_train_predict(asin, time_steps=150, days_ahead=1, num_epochs=2, price='NEW'):
    df = get_clean_data_for_product(asin)
    df = prepData(df, days_ahead=days_ahead, price=price)

    data = getData(df, price=price)
    # TODO: Fit on only train data!
    data_scaler = MinMaxScaler()
    # y_scaler = MinMaxScaler()
    data_scaler.fit(data)
    # y_scaler.fit(y_raw)
    data = data_scaler.transform(data)
    # y = y_scaler.transform(y_raw)
    x_train, y_train, x_test, y_test = getSequencesFromData(data, time_steps = time_steps, days_ahead=days_ahead)

    decoder_input_train = np.zeros(y_train.shape)
    decoder_input_train[:,1:,:] = y_train[:,:-1,:]
    decoder_input_train[:,0,:] = x_train[:,-1,:]


    n_input = x_train.shape[2]
    n_output = y_train.shape[1]

    model, encoder_model, decoder_model = createSeq2SeqModel(n_input, n_output, time_steps = time_steps, lstm_units=200)
    model = trainSeq2SeqModel(model, x_train, y_train, decoder_input_train, num_epochs=num_epochs)
    print('done training.')
    predictions = []
    scaled_predictions = []
    abs_errors = []
    for x, y in zip(x_test, y_test):
        prediction = decode_sequence(x.reshape(1, x.shape[0], x.shape[1]), encoder_model, decoder_model, days_ahead, n_input)
        predictions.append(prediction)
        scaled_prediction = data_scaler.inverse_transform(prediction[0])
        scaled_predictions.append(scaled_prediction)
        scaled_truth = data_scaler.inverse_transform(y)
        abs_errors.append(abs(scaled_prediction-scaled_truth))

    prediction = scaled_predictions[-1]
    price_index = ['AMAZON', 'NEW', 'SALES', 'MIN_UNUSED'].index(price)
    # print('SQUARED ERRORS!')
    # print(squared_errors[0].shape)
    mae = np.asarray(abs_errors)[:-1,:,price_index].mean()
    return prediction, mae


    # print(model.evaluate(x_test, y_test))
def decode_sequence(input_sequence, encoder_model, decoder_model, days_ahead, num_features):
    states_value = encoder_model.predict(input_sequence)

    target_seq = np.zeros((1, 1, num_features))

    target_seq[0, 0, :] = input_sequence[0, -1, :]

    decoded_seq = np.zeros((1, days_ahead, num_features))

    for i in range(days_ahead):
        output, h, c = decoder_model.predict([target_seq] + states_value)
        decoded_seq[0, i, :] = output[0, 0, :]

        # update target sequence
        target_seq = np.zeros((1, 1, num_features))
        target_seq[0, 0, :] = output[0, 0, :]

        # update states
        states_value = [h, c]
    return decoded_seq

def predict_upcoming_prices(days_ahead=3, time_steps=150, num_epochs=10, asin='B00BWU3HNY', price='NEW'):
    predictions, mae = create_train_predict(asin, time_steps=time_steps, days_ahead=days_ahead, num_epochs=num_epochs, price=price)
    return predictions, mae

def get_plottable_data_and_predictions(predictions, asin='B00BWU3HNY', price='NEW'):
    df = get_clean_data_for_product(asin)
    # df = prepData(df)

    price_index = ['AMAZON', 'NEW', 'SALES', 'MIN_UNUSED'].index(price)

    prediction_length = len(predictions)


    data_times = list(df['Time'])
    data_values = list(df[price])

    prediction_times = [data_times[-1] + datetime.timedelta(days=days) for days in range(prediction_length+1)]
    prediction_values = [data_values[-1]] + list(predictions[:,price_index])

    return data_times, data_values, prediction_times, prediction_values

def plot_data_and_predictions(predictions, asin='B00BWU3HNY', price='MIN_UNUSED'):
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
    price='MIN_UNUSED'
    asin='B0047E0EII'
    # predictions = predict_upcoming_prices(3, time_steps=365, num_epochs=10, price=price, asin=asin)
    predictions, mae = predict_upcoming_prices(days_ahead=20, time_steps=200, num_epochs=10, price=price, asin=asin)

    plot_data_and_predictions(predictions, asin=asin, price=price)
    print(mae)


if __name__ == "__main__":
    main()
