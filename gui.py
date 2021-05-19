import bot
from bot import run
from bot import update_graph
import tkinter as tk 
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import requests
from PIL import Image
from PIL import ImageTk

##TO DO:

#run_forever runs literally forever and can't be stopped form the GUI
#Entry connect to socket
#Button connect to frame via label (only display closing values)
#Show historical data from a certain crypto
#Connect to API's

root = tk.Tk()

canvas = tk.Canvas(root, height = 500, width = 700)
canvas.pack()

background_image = Image.open('Crypto_bot_pkg/background_image.png')
background_image = ImageTk.PhotoImage(background_image)
background_label = tk.Label(root, image=background_image)
background_label.place(relwidth = 1, relheight = 1)

frame = tk.Frame(root, bg='#80c1ff', bd = 5)
frame.place(relx = 0.5, rely = 0.1, relwidth=0.75, relheight=0.1, anchor = 'n')

entry = tk.Entry(frame, bg='green', font = 20)
entry.place(relwidth=0.85, relheight=1)

button = tk.Button(frame, text = "See your crypto", background = '#3968b3', font = 30, command = lambda:[bot.update_graph(),bot.run()])
button.place(relx = 0.7, relwidth=0.3, relheight=1)

fig = plt.figure()
ax = fig.add_subplot(111)
bar = FigureCanvasTkAgg(fig, root)
bar.get_tk_widget().pack(side=tk.BOTTOM, fill=tk.BOTH)


# frame2 = tk.Frame(root, bg='#80c1ff', bd = 5)
# frame2.place(relx = 0.5, rely = 0.25, relwidth = 0.75, relheight=0.6, anchor = 'n')

button2 = tk.Button(root, text = "See live graph", background = '#3968b3', font = 40)
button2.place(relx = 0.1, rely = 0.4, relwidth=0.75, relheight=0.1)

# label = tk.Label(frame2, bg= "darkgray", font = 50, text = "Closing values should appear here")
# label.place(rely= 0.25, relwidth=1, relheight=0.2)

root.mainloop() 
