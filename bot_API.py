#LAST

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



# ---------------- FUNCTIONS --------------------- #
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

#Get the result printed in the entrybox
def crypto_price(coin):
    result = bot_api(coin)
    entry_results.delete(0, END)
    entry_results.insert(0, str(result))

def quit(self):
       root.destroy 

def add_image(coin):
    global my_image
    initial_coin = coin
    coin_path = 'logos/'
    index = '.png'
    final_coin =  coin_path + coin + index
    filepath = final_coin
    if coin == 'eth' or coin == 'btc' or coin == 'doge' or coin == 'ada' or coin == 'ltc':
        my_image = tk.PhotoImage(file=filepath)
        coin_image.delete('1.0', END)
        coin_image.image_create(END, image = my_image)
    else:
        my_image = tk.PhotoImage(file='logos/white.png')
        coin_image.delete('1.0', END)
        coin_image.image_create(END, image = my_image)

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
    plt.show()
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

def do_rsi(symbol, prices): 
    result = rsi(symbol, prices) 
    entry_rsi.delete(0, END)
    rsi_value = result[0]
    decision = result[1]
    entry_rsi.insert(0, ('RSI value: {}, {}').format(rsi_value, decision))


# rsi('btc', 15) #'1d', 2020,4,1,2020,5,1)



# ------------------ GUI ---------------------- #

root = tk.Tk()


#Canvas size
canvas = tk.Canvas(root, height = 700, width = 900)
canvas.pack()

#Frame for crypto price
frame = tk.Frame(root, bg='#80c1ff', bd = 5)
frame.place(relx = 0.5, rely = 0.075, relwidth=1, relheight=0.1, anchor = 'n')

label_coins = tk.Label(root, bg= 'white', font = 10, text = "Bitcoin = btc; Ethereum = eth; Cardano = ada; Dogecoin = doge; Litecoin = ltc")
label_coins.place(relx = 0, rely = 0.025, relwidth= 1, relheight= 0.025)

entry = tk.Entry(frame, bg='green', font = 20)
entry.place(relx = 0.25, relwidth=0.75, relheight=1)

label = tk.Label(frame, bg= "darkgray", font = 50, text = "Type your cryptocoin here")
label.place(relx = 0, relwidth=0.25, relheight=1)

SOCKET = f"wss://stream.binance.com:9443/ws/{entry.get}t@kline_1m"

#Get crypto price and image button
button_start = tk.Button(root, text = "Get your live crypto price", command = lambda: [crypto_price(entry.get()), add_image(entry.get())])
button_start.place(relx = 0, rely = 0.2,relwidth = 0.2, relheight=0.1)

#Result will be displayed here
entry_results = tk.Entry(root)
entry_results.place(relx = 0.25, rely = 0.2, relwidth= 0.4, relheight = 0.1)

#Calculates RSI value and suggests decision
button_rsi = tk.Button(root, text = "Sell, buy or relax", command = lambda: do_rsi(entry.get(), 16)) #entry_interval.get(), int(entry_startYear.get()), int(entry_startMonth.get()), int(entry_startDay.get()), int(entry_endYear.get()), int(entry_endMonth.get()), int(entry_endDay.get())))
button_rsi.place(relx = 0, rely = 0.3,relwidth = 0.2, relheight=0.1)

entry_rsi = tk.Entry(root)
entry_rsi.place(relx = 0.25, rely = 0.3, relwidth= 0.4, relheight = 0.1)

photo_frame = tk.Frame(root)
photo_frame.place(relx = 0.8, rely = 0.2, relwidth = 0.12, relheight = 0.155)

coin_image = tk.Text(photo_frame)
coin_image.place(relwidth = 1, relheight = 1)

frame_graph = tk.Frame(root, bg='#80c1ff', bd = 5)
frame_graph.place(relx = 0.5, rely = 0.5, relwidth=1, relheight=0.2, anchor = 'n')

#Information for the historical graph
label_interval = tk.Label(frame_graph, bg= "darkgray", font = 50, text = "Interval")
label_interval.place(relx = 0, relwidth=0.15, relheight=1)

entry_interval = tk.Entry(frame_graph, bg='green', font = 20)
entry_interval.place(relx = 0.15, relwidth= 0.15, relheight = 1)

label_startYear = tk.Label(frame_graph, bg= "darkgray", font = 40, text = "Start Year")
label_startYear.place(relx = 0.3, rely= 0, relwidth=0.15, relheight=0.5)

entry_startYear = tk.Entry(frame_graph, bg='green', font = 20)
entry_startYear.place(relx = 0.45, rely = 0, relwidth= 0.15, relheight = 0.5)

label_startMonth = tk.Label(frame_graph, bg= "darkgray", font = 50, text = "Start Month")
label_startMonth.place(relx = 0.6, rely= 0, relwidth=0.1, relheight=0.5)

entry_startMonth = tk.Entry(frame_graph, bg='green', font = 20)
entry_startMonth.place(relx = 0.7, rely = 0, relwidth= 0.1, relheight = 0.5)

label_startDay = tk.Label(frame_graph, bg= "darkgray", font = 50, text = "Start Day")
label_startDay.place(relx = 0.8, rely= 0, relwidth=0.1, relheight=0.5)

entry_startDay = tk.Entry(frame_graph, bg='green', font = 20)
entry_startDay.place(relx = 0.9, rely = 0, relwidth= 0.1, relheight = 0.5)

label_endYear = tk.Label(frame_graph, bg= "darkgray", font = 70, text = "End Year")
label_endYear.place(relx = 0.3, rely= 0.5, relwidth=0.15, relheight=0.5)

entry_endYear = tk.Entry(frame_graph, bg='green', font = 20)
entry_endYear.place(relx = 0.45, rely = 0.5, relwidth= 0.15, relheight = 0.5)

label_endMonth = tk.Label(frame_graph, bg= "darkgray", font = 50, text = "End Month")
label_endMonth.place(relx = 0.6, rely= 0.5, relwidth=0.1, relheight=0.5)

entry_endMonth = tk.Entry(frame_graph, bg='green', font = 20)
entry_endMonth.place(relx = 0.7, rely = 0.5, relwidth= 0.1, relheight = 0.5)

label_endDay = tk.Label(frame_graph, bg= "darkgray", font = 50, text = "End Day")
label_endDay.place(relx = 0.8, rely= 0.5, relwidth=0.1, relheight=0.5)

entry_endDay = tk.Entry(frame_graph, bg='green', font = 20)
entry_endDay.place(relx = 0.9, rely = 0.5, relwidth= 0.1, relheight = 0.5)

#Information about possible intervals and limit values
label_info = tk.Label(root, bg= 'white', font = 10, text = "Available intervals: 1m, 3m, 5m, 15m, 1h, 2h, 3h, 4h, 8h, 12h, 1d, 3d, 1w, 1M")
label_info.place(relx = 0, rely = 0.7, relwidth= 1, relheight= 0.05)
label_info2 = tk.Label(root, bg= 'white', font = 10, text = "Maximum ammount of historical timepoints is 1000")
label_info2.place(relx = 0, rely = 0.75, relwidth= 1, relheight= 0.05)
     
button_history = tk.Button(root, text = "See Historical Graph", command = lambda: historical(entry.get(), entry_interval.get(), int(entry_startYear.get()), int(entry_startMonth.get()), int(entry_startDay.get()), int(entry_endYear.get()), int(entry_endMonth.get()), int(entry_endDay.get())))
button_history.place(rely = 0.8, relwidth = 1, relheight = 0.1)

#Exit the GUI
button_stop = tk.Button(root, text = "Stop", command = root.quit)
button_stop.place(relx = 0.5, rely = 0.9, relwidth = 0.5, relheight = 0.1, anchor = 'n')

root.mainloop()
