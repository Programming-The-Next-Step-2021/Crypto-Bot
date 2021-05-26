import json
from pandas.core.indexes import interval
import requests
import json
import matplotlib
import pandas as pd
import datetime as dt
import qgrid
import matplotlib.pyplot as plt
import pprint

def historical(symbol, interval, startTime, endTime):
    global df
    url = 'https://api.binance.com/api/v3/klines'

    interval = '1h'
    startTime = dt.datetime(2020,1,1)
    endTime = dt.datetime(2020,2,1)
    symbol = symbol.upper()

    startTime = str(int(startTime.timestamp() * 1000))
    endTime = str(int(endTime.timestamp() * 1000))
    limit = '1000'

    req_params = {'symbol': symbol + 'T', 'interval': interval, 'startTime': startTime, 
    'endTime': endTime, 'limit': limit}

    df = pd.DataFrame(json.loads(requests.get(url, params = req_params).text))

    df = df.iloc[:, 0:6]

    df.columns =  ['datetime', 'open', 'high', 'low', 'close', 'volume']

    df.index = [dt.datetime.fromtimestamp(x / 1000.0) for x in df.datetime]
    # del df['datetime']
    # print(df.head())
    # print(df['close'])
    df['close'] = df['close'].astype(float)
    df['close'].plot()
    plt.show()
    return df


historical("BTCUSDT", '1h', dt.datetime(2020,1,1), dt.datetime(2020,2,1))



