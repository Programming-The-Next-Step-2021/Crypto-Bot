import websocket
import json
import pprint 
import talib
import numpy as np
import time
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from binance.client import Client
from binance.enums import *

#Select your favorite coin
cc = 'btcusd'

#Select how often do you want to get updates
interval = '1m'

#Specify the websocket to stream data
SOCKET = f"wss://stream.binance.com:9443/ws/{cc}t@kline_{interval}"

#Bot values (adjust as preferred)
RSI_PERIOD = 2
RSI_OVERBOUGHT = 70
RSI_OVERSOLD = 30
TRADE_SYMBOL = 'BTCUSD'
TRADE_QUANTITY = 0.05

# def stop():
#         print("Time to say goodbye")
#         ws = websocket.WebSocketApp(SOCKET)
#         ws.close = False
#Graphing function
def update_graph(xdata, ydaya):
    fig = plt.figure()
    ax = fig.add_subplot(111)
    fig.show()

    xdata = []
    ydata = []
    
    ax.plot(xdata, ydata, color='g')
    ax.legend([f"Last price: {ydata[-1]}$"])

    fig.canvas.draw()
    plt.pause(0.1)
    """
    This function will create a plot for obtained values
    """

def run():
    """
    This may be a class, instead of a function, and it will communicate 
    to the gui that the program wants to run
    """

    #empty list of closing values
    closes = []
    xdata = []
    ydata = []

    #In the beginning, God didn't give you any cryptos --> you have none
    in_position = False

    #Function
    def on_open(ws):
        """
        Display message when the websocket opens"
        """
        print('opened connection')

    def on_close(ws):
        print('closed connection')
        """
        Display message when thr websocket is closed
        """

    def on_message(ws, message): 
        """
        Function that cleans the json_message and return the crypto values everytime that
        a candlestick closes. It also returns the time that is occured
        """
        global closes

        print("received message")   
        json_message = json.loads(message)
        data = json_message
        # pprint.pprint(json_message)

        candle = json_message['k']
        is_candle_closed = candle['x']
        close = candle['c']
        # print(close)

        #Get the crypto value when the candle closes
        if is_candle_closed:
            print('candle( closed at {}'.format(close))
            closes.append(float(close))

            event_time = time.localtime(data['E'] // 1000)
            event_time = f"{event_time.tm_hour}:{event_time.tm_min}:{event_time.tm_sec}"
            print(event_time, close)

            xdata.append(event_time)
            ydata.append(float(close))
        #     print(closes)

            update_graph()


        #     #Buy or sell, depending on the RSI value
        #     if len(closes) > RSI_PERIOD:
        #         np_closes = np.array(closes)
        #         rsi = talib.RSI(np_closes, RSI_PERIOD)
        #         print("calculated rsis")
        #         print(rsi)
        #         last_rsi = rsi[-1]
        #         print("the current RSI is {}".format(last_rsi))

        #         if last_rsi > RSI_OVERBOUGHT:
        #             print("BEARISH: SELL YOUR CRYPTOS NOW")
        #             # if in_position:
        #             #     print("Bearish: But, you can't sell what you don't have")
        #             #     # Binance selling order

        #         if last_rsi < RSI_OVERSOLD:
        #             print("BULLISH: BUUUUY, TO THE MOON")
        #             # if in_position:
        #             #     print("Bullish: You have some already, move on")
        #             #     # Binance buying order



    #Assing functions to the websocket 
    ws = websocket.WebSocketApp(SOCKET, on_open=on_open, on_message = on_message, on_close = on_close)

    #Get information for my coin
    ws.run_forever()

