from tkinter.constants import END
from requests import Session
import json
import time
import tkinter as tk
import talib
import numpy as np
from numpy import DataSource
import pandas as pd
import datetime as dt
import matplotlib.pyplot as plt
import requests
import websockets
import asyncio

RSI_PERIOD = 14
RSI_OVERBOUGHT = 70
RSI_OVERSOLD = 30
# TRADE_SYMBOL = 'BTCUSD'
# TRADE_QUANTITY = 0.05

results = []
xdata = []
ydata = []

url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest'

coin = 'litecoin'
def bot_api(coin):
    """
    A function that retrieves the latest price of the selected cryptocurrency from the API 
    of coinmarketcap.

    If an unexistent symbol is computed, no value is retrieved

    Properties
    -----------
    coin : str
        the symbol of a cryptocurrency

    Returns
    --------
    str
        A string with the latest value of the specified cryptocurrency

    """

    global data

    parameters = {
        'symbol': coin,
        'convert': "usd"
    }

    headers = {
        'Accepts': 'application/json',
        'X-CMC_PRO_API_KEY': '31233140-af13-4dd0-ad7e-1bdb98b80470'
    }

    session = Session()
    session.headers.update(headers)

    response = session.get(url, params = parameters)

    result = json.loads(response.text)['data']
    result = list(result)
    number = result[0]

    result = json.loads(response.text)['data'][str(number)]['quote']['USD']['price']

    return(result)


async def main(symbol, prices):

    global xdata
    global results

    url = "wss://stream.binance.com:9443/stream?streams=" + symbol + "usdt@miniTicker"
    async with websockets.connect(url) as client:
        global xdata
        for x in range(prices):
        # while len(xdata) < prices:
            data = json.loads(await client.recv())['data']

            event_time = time.localtime(data['E'] // 1000)
            event_time = f"{event_time.tm_hour}:{event_time.tm_min}:{event_time.tm_sec}"

            print(event_time, data['c'])
            a = data['c']
            results.append(a)

            print(x)
        return(results)

def run_bot2(symbol, prices):
    """
    This function can obtain real-live prices of cryptos every second.

    This function contains the asynchronous function main(), which uses the
    Binance websocket in order to retrieve the latest cryptocurrency from
    its platform each second. With this, a loop is set to run 15 times (enough 
    values to calculate the RSI of 14 timepoints). The results from the 15 
    values are stored within the 'results' object.
    It is important to note that, while the values are being calculated, it 
    is not possible to use anything else from the GUI.

    If an unexistent symbol is specified, no value is retrieved.

    Properties
    -----------
    symbol : str
        the symbol of a cryptocurrency
    prices : int 
        The ammount of prices you want to retrieve

    Returns
    -------
    list
        A list with the ammount of cryptocurrency values specified
    """

    if __name__ == '__main__':
        loop = asyncio.get_event_loop()
        loop.run_until_complete(main(symbol, prices))
        return(results)


def historical(symbol, interval, startYear, startMonth, startDay, endYear, endMonth, endDay):
    """
    This function can retrieve historical data of any crypto in a graph

    It connect with the API from Binance and it appends the closing candlestick
    values of the crypto, with a specified interval.

    Properties
    ----------
    symbol : str
        A cryptocurrency symbol
    interval : str
        Interval of closing candlesticks
    startYear : str
        The year of the starting date
    startMonth : str
        The month of the starting date
    startDay : str
        The day of the starting date
    endYear : str
        The year for the ending date
    endMonth : str
        The month for the ending date
    endDay : str
        The day for the ending date

    Returns
    --------
    dataframe
        A dataframe with all the values that appear in the graph
    plot
        A graph with the crpto values (x_axis = date, y_axis = price)
    """

    global df

    url = 'https://api.binance.com/api/v3/klines'

    symbol = symbol.upper()
    startTime = str(int(dt.datetime(startYear,startMonth,startDay).timestamp() * 1000))
    endTime = str(int(dt.datetime(endYear,endMonth,endDay).timestamp() * 1000))
    limit = '1000'

    req_params = {'symbol': symbol + 'USDT', 'interval': interval, 'startTime': startTime, 
    'endTime': endTime, 'limit': limit}

    df = pd.DataFrame(json.loads(requests.get(url, params = req_params).text))

    df = df.iloc[:, 0:6]

    df.columns =  ['datetime', 'open', 'high', 'low', 'close', 'volume']

    df.index = [dt.datetime.fromtimestamp(x / 1000.0) for x in df.datetime]
    df['close'] = df['close'].astype(float)
    df['close'].plot()
    # plt.show()
    return df

def rsi(symbol, prices):
    """
    This function calculate the Relative Strength Index (RSI) from live crypto
    prices

    It uses the run_bot2 function to communicate with the websocket from 
    Binance, and after 15 values have been obtained, it calculates the RSI,
    and it displays a message with a suggestion to buy/sell/retain:
    - If RSI > 70 = Market is bearish/overbought, you should sell now
    - If 30 < RSI > 70 = Market is stable, you should not do anything
    - If RSI < 30 = Market is bullish/oversold, you should buy now  

    Properties
    ----------
    symbol : str
        a crypto symbol
    prices : int
        (optional) it is set to 15 as default

    Returns
    -------
    float
        The RSI value
    str
        The buying/selling/retaining decision
    """

    df = run_bot2(symbol, prices)
    print(df)
    df = np.array(df, dtype='f8')

    #Buy or sell, depending on the RSI value
    rsi = talib.RSI(df, RSI_PERIOD)
    # print(rsi)
    last_rsi = rsi[-1]
    print(last_rsi)
    if last_rsi > RSI_OVERBOUGHT:
        decision = "BEARISH: SELL YOUR CRYPTO NOW"
        # if in_position:
        #     print("Bearish: But, you can't sell what you don't have")
        #     # Binance selling order

    if last_rsi < RSI_OVERSOLD:
        decision = "BULLISH: BUUUUY, TO THE MOON"
        # if in_position:
        #     print("Bullish: You have some already, move on")
        #     # Binance buying order

    if last_rsi > RSI_OVERSOLD and last_rsi < RSI_OVERBOUGHT:
        decision = "RELAX AND DO NOTHING"
    
    print(decision)

    last_rsi = round(last_rsi, 2)
    return(last_rsi, decision)

