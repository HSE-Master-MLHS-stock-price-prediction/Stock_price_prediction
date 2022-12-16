import pandas as pd
import numpy as np
#
import yfinance as yf


class Config:
    OUTPUT_WINDOW_SIZE = 30
    INPUT_WINDOW_SIZE = 60
    RANDOM_STATE = 7575


def _transform_to_DOIU(prices):
    '''
    Transform a timeseries of actual prices to the DOIU format.

    :param prices: prices timeseries to transform.
    :return:
    '''
    arr = pd.DataFrame(prices).pct_change().to_numpy()[1:]
    x = [1]
    for el in arr:
        x.append(x[-1] * (1 + el))
    return np.array(x)


def prepare_data(prices,
                 output_window_size=Config.OUTPUT_WINDOW_SIZE,
                 input_window_size=Config.INPUT_WINDOW_SIZE):
    '''
    Create a list of windows possible to use to train/validate a model.

    :param prices: a whole timeseries of prices.
    :param output_window_size: the delay for which a prediction is made.
    :param input_window_size: the size of the train timeseries.
    '''
    X = []
    y = []
    for i in range(0,
                   len(prices) - output_window_size - input_window_size,
                   output_window_size):
        current_selection = prices[i:input_window_size + i
                                     + output_window_size]
        tr_x = _transform_to_DOIU(current_selection)
        y.append(tr_x[-1].reshape(1, -1))
        X.append(tr_x[:input_window_size].reshape(1, -1))

    X = np.concatenate(X, axis=0)
    y = np.concatenate(y, axis=0)
    return X, y

if __name__ == '__main__':
    yndx = yf.Ticker("yndx")
    prices = yndx.history(start="2011-05-24", end="2016-12-31", interval='1d').Close
    print(pd.DataFrame(prices)[0])