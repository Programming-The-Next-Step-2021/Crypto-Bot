import tkinter as tk
import requests
from PIL import Image
from PIL import ImageTk
# import bot
from tkinter import Label
import websocket
import json
import pprint
import talib
import numpy as np
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
RSI_OVERBOUGHT = 10
RSI_OVERSOLD = 90
TRADE_SYMBOL = 'BTCUSD'
TRADE_QUANTITY = 0.05

def run():
    #empty list of closing values
    closes = []

    #In the beginning, God didn't give you any cryptos --> you have none
    in_position = False

    #Function
    def on_open(ws):
        print('opened connection')

    def on_close(ws):
        print('closed connection')

    def on_message(ws, message): 
        global closes

        print("received message")   
        json_message = json.loads(message)
        # pprint.pprint(json_message)

        candle = json_message['k']

        is_candle_closed = candle['x']
        close = candle['c']

        #Get the crypto value when the candle closes
        if is_candle_closed:
            print('candle( closed at {}'.format(close))
            closes.append(float(close))
            print("closes")

        #     print(closes)

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











root = tk.Tk()

canvas = tk.Canvas(root, height = 500, width = 700)
canvas.pack()

background_image = Image.open('background_image.png')
background_image = ImageTk.PhotoImage(background_image)
background_label = tk.Label(root, image=background_image)
background_label.place(relwidth = 1, relheight = 1)

frame = tk.Frame(root, bg='#80c1ff', bd = 5)
frame.place(relx = 0.5, rely = 0.1, relwidth=0.75, relheight=0.1, anchor = 'n')

entry = tk.Entry(frame, bg='green', font = 20)
entry.place(relwidth=0.85, relheight=1)

button = tk.Button(frame, text = "Crypto History", background = '#3968b3', font = 30, 
command = lambda:run())

button.place(relx = 0.7, relwidth=0.3, relheight=1)

frame2 = tk.Frame(root, bg='#80c1ff', bd = 5)
frame2.place(relx = 0.5, rely = 0.25, relwidth = 0.75, relheight=0.6, anchor = 'n')

label = tk.Label(frame2, bg= "darkgray", font = 50)
label.place(relx = 0.5, relwidth=1, relheight=1, anchor = 'n')

root.mainloop() 
