from numpy import DataSource
import bot
# import bot2
from bot import run
from bot import select_crypto
from bot import get_results
from bot import update_graph
import bot_API
from bot_API import bot_api
# from bot_API import stop
import tkinter as tk 
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import requests
from PIL import Image
from PIL import ImageTk
from twisted.internet import task, reactor

timeout = 60.00
#promise 

##TO DO:

#run_forever runs literally forever and can't be stopped from the GUI
#Entry connect to socket
#Button connect to frame via label (only display closing values)
#Show historical data from a certain crypto
#Connect to API's

root = tk.Tk()

global data 
canvas = tk.Canvas(root, height = 700, width = 900)
canvas.pack()

# background_image = Image.open('background_image.png')
# background_image = ImageTk.PhotoImage(background_image)
# background_label = tk.Label(root, image=background_image)
# background_label.place(relwidth = 1, relheight = 1)

frame = tk.Frame(root, bg='#80c1ff', bd = 5)
frame.place(relx = 0.5, rely = 0.05, relwidth=1, relheight=0.1, anchor = 'n')

entry = tk.Entry(frame, bg='green', font = 20)
entry.place(relwidth=0.75, relheight=1)

label = tk.Label(frame, bg= "darkgray", font = 50, text = "Type your crypto symbol")
label.place(relx = 0.75, relwidth=0.25, relheight=1)

SOCKET = f"wss://stream.binance.com:9443/ws/{entry.get}t@kline_1m"

# button_start = tk.Button(root, text = "Get your crypto price", command = lambda: bot.run(entry.get()))
button_start = tk.Button(root, text = "Get your crypto price", command = lambda: bot_API.crypto_price(entry.get()))
button_start.place(relx = 0.5, rely = 0.5,relwidth = 0.6, relheight=0.1, anchor = 'n')

entry_results = tk.Entry(root)
entry_results.place(relx = 0.5,rely = 0.4, relwidth= 0.5, relheight = 0.1, anchor = 'n')

# frame_image = tk.Frame(root)
# frame_image.place(relx = 0.75, rely = 0.4, relwidth = 0.25, relheight = 0.1, anchor = 'n')

# img = tk.PhotoImage(file = 'ethereum.gif', format='gif')
# label_image = tk.PhotoImage(root, image = img)
# label_image.place(relx = 0.5, rely = 0.4, relwidth = 0.25, relheight = 0.25, anchor = 'n')

# fig = plt.figure()
# ax = fig.add_subplot(111)
# bar = FigureCanvasTkAgg(fig, root)
# bar.get_tk_widget().pack(side=tk.BOTTOM, fill=tk.BOTH)

button_stop = tk.Button(root, text = "Stop", command = lambda: bot_API.stop())
button_stop.place(relx = 0.5, rely = 0.9, relwidth = 0.5, relheight = 0.1, anchor = 'n')

button_graph = tk.Button(root, text = "Live Graph", command = lambda: bot.update_graph())
button_graph.place(relx = 0.5, rely = 0.7, relwidth = 0.5, relheight = 0.1, anchor = 'n')

# xdata = []
# ydata = []

# frame2 = tk.Frame(root, bg='#80c1ff', bd = 5)
# frame2.place(relx = 0.5, rely = 0.25, relwidth = 0.75, relheight=0.6, anchor = 'n')

# button2 = tk.Button(root, text = "See live graph", background = '#3968b3', font = 40, command=lambda:bot.update_graph(xdata, ydata))
# button2.place(relx = 0.1, rely = 0.4, relwidth=0.75, relheight=0.1)

# label = tk.Label(frame2, bg= "darkgray", font = 50, text = "Closing values should appear here")
# label.place(rely= 0.25, relwidth=1, relheight=0.2)

root.mainloop() 
