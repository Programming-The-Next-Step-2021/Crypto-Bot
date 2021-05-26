#### This script runs perfectly - for updates, see Final_GUI.py

# import bot_API
# from bot_API import bot_api
# from bot_API import stop
# import bot2
# from bot2 import update_graph
# from bot2 import main

import os
import sys
from tkinter.constants import END
from tkinter.constants import CENTER
from requests import Request, Session
import json
import pprint
import sched, time
import tkinter as tk
from twisted.internet import task, reactor
from requests.api import head
from numpy import DataSource
import pandas as pd
import datetime as dt
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import requests
from PIL import Image
from PIL import ImageTk
import bot
from bot import run
from bot import select_crypto
from bot import get_results
from bot import update_graph
import websockets
import asyncio



# ---------------- FUNCTIONS --------------------- #
url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest'

coin = 'litecoin'
def bot_api(coin):
    global data

    parameters = {
        'slug': coin,
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
    # print(result)
    # print(number)

    result = json.loads(response.text)['data'][str(number)]['quote']['USD']['price']

    # time.sleep(60)
    return(result)

#Get the result printed in the entrybox
def crypto_price(coin):
    result = bot_api(coin)
    entry_results.delete(0, END)
    entry_results.insert(0, str(result))


#Run the loop every 60 seconds (it freezes all other processes)
def run_button(coin):
    while True:
        sleep(60 - time() % 60)
        bot_api(coin)

def quit(self):
       root.destroy 

def bot2():
    os.system('python3 bot2.py')

def add_image(coin):
    global my_image
    initial_coin = coin
    coin_path = 'logos/'
    index = '.png'
    final_coin =  coin_path + coin + index
    filepath = final_coin
    my_image = tk.PhotoImage(file=filepath)
    coin_image.delete('1.0', END)
    coin_image.image_create(END, image = my_image)

def show_plot():
    global ax
    global fig

    fig = plt.figure()
    ax = fig.add_subplot(111)
    fig.show()

def update_graph():
    ax.plot(xdata, ydata, color='g')
    ax.legend([f"Last price: {ydata[-1]}$"])

    fig.canvas.draw()
    ax.axes.get_xaxis().set_visible(False)    
    plt.pause(0.1)

async def main(symbol):
    url = "wss://stream.binance.com:9443/stream?streams=" + symbol + "usdt@miniTicker"
    async with websockets.connect(url) as client:
        while True:
            data = json.loads(await client.recv())['data']

            event_time = time.localtime(data['E'] // 1000)
            event_time = f"{event_time.tm_hour}:{event_time.tm_min}:{event_time.tm_sec}"

            print(event_time, data['c'])

            xdata.append(event_time)
            ydata.append(int(float(data['c'])))

            update_graph()

def run_bot2(symbol):
    if __name__ == '__main__':
        loop = asyncio.get_event_loop()
        loop.run_until_complete(main(symbol))


def historical(symbol, interval, start, end):
    global df

    url = 'https://api.binance.com/api/v3/klines'

    symbol = symbol.upper()

    startTime = str(int(dt.datetime(2020,start,1).timestamp() * 1000))
    endTime = str(int(dt.datetime(2020,end,1).timestamp() * 1000))
    limit = '1000'

    req_params = {'symbol': symbol + 'USDT', 'interval': interval, 'startTime': startTime, 
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







# ------------------ GUI ---------------------- #


timeout = 60.00
xdata = []
ydata = []

##TO DO:

#run_forever runs literally forever and can't be stopped from the GUI
#Show historical data from a certain crypto
#Connect to API's

root = tk.Tk()


# global data 
canvas = tk.Canvas(root, height = 700, width = 900)
canvas.pack()

# background_image = Image.open('background_image.png')
# background_image = ImageTk.PhotoImage(background_image)
# background_label = tk.Label(root, image=background_image)
# background_label.place(relwidth = 1, relheight = 1)

frame = tk.Frame(root, bg='#80c1ff', bd = 5)
frame.place(relx = 0.5, rely = 0.075, relwidth=1, relheight=0.1, anchor = 'n')

entry = tk.Entry(frame, bg='green', font = 20)
entry.place(relx = 0.25, relwidth=0.75, relheight=1)

label = tk.Label(frame, bg= "darkgray", font = 50, text = "Type your cryptocoin here")
label.place(relx = 0, relwidth=0.25, relheight=1)

SOCKET = f"wss://stream.binance.com:9443/ws/{entry.get}t@kline_1m"

# button_start = tk.Button(root, text = "Get your crypto price", command = lambda: bot.run(entry.get()))
button_start = tk.Button(root, text = "Get your live crypto price", command = lambda: [crypto_price(entry.get()), add_image(entry.get())])
button_start.place(relx = 0, rely = 0.2,relwidth = 0.25, relheight=0.1)

entry_results = tk.Entry(root)
entry_results.place(relx = 0.25, rely = 0.2, relwidth= 0.5, relheight = 0.1)

photo_frame = tk.Frame(root)
photo_frame.place(relx = 0.8, rely = 0.2, relwidth = 0.12, relheight = 0.155)

# photo = tk.PhotoImage(file = "logos/ethereum.gif")
coin_image = tk.Text(photo_frame)
coin_image.place(relwidth = 1, relheight = 1)

button_stop = tk.Button(root, text = "Stop", command = root.quit)
button_stop.place(relx = 0.5, rely = 0.9, relwidth = 0.5, relheight = 0.1, anchor = 'n')

frame_graph = tk.Frame(root, bg='#80c1ff', bd = 5)
frame_graph.place(relx = 0.5, rely = 0.4, relwidth=1, relheight=0.2, anchor = 'n')

label_graph = tk.Label(frame_graph, bg= "darkgray", font = 50, text = "Type your crypto symbol here")
label_graph.place(relx = 0, relwidth=0.25, relheight=0.5)

entry_graph = tk.Entry(frame_graph, bg='green', font = 20)
entry_graph.place(relx = 0.25, relwidth= 0.25, relheight = 0.5)

label_interval = tk.Label(frame_graph, bg= "darkgray", font = 50, text = "Type your interval here")
label_interval.place(relx = 0, rely= 0.5, relwidth=0.25, relheight=0.5)

entry_interval = tk.Entry(frame_graph, bg='green', font = 20)
entry_interval.place(relx = 0.25, rely = 0.5, relwidth= 0.25, relheight = 0.5)

label_start = tk.Label(frame_graph, bg= "darkgray", font = 50, text = "Type your start date here")
label_start.place(relx = 0.5, rely= 0, relwidth=0.25, relheight=0.5)

entry_start = tk.Entry(frame_graph, bg='green', font = 20)
entry_start.place(relx = 0.75, rely = 0, relwidth= 0.25, relheight = 0.5)

label_end = tk.Label(frame_graph, bg= "darkgray", font = 50, text = "Type your end date here")
label_end.place(relx = 0.5, rely= 0.5, relwidth=0.25, relheight=0.5)

entry_end = tk.Entry(frame_graph, bg='green', font = 20)
entry_end.place(relx = 0.75, rely = 0.5, relwidth= 0.25, relheight = 0.5)


button_graph = tk.Button(root, text = "See Live Graph", command = lambda: [show_plot(), run_bot2(entry_graph.get())])
button_graph.place(relx = 0.25, rely = 0.75, relwidth = 0.5, relheight = 0.1, anchor = 'n')
        
button_history = tk.Button(root, text = "See Historical Graph", command = lambda: historical(entry_graph.get(), entry_interval.get(), int(entry_start.get()), int(entry_end.get())))
button_history.place(relx = 0.75, rely = 0.75, relwidth = 0.5, relheight = 0.1, anchor = 'n')
        

# label = tk.Label(frame2, bg= "darkgray", font = 50, text = "Closing values should appear here")
# label.place(rely= 0.25, relwidth=1, relheight=0.2)

root.mainloop()

    # interval = '1h'
    # startTime = dt.datetime(2020,1,1)
    # endTime = dt.datetime(2020,2,1)