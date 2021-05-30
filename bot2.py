import websockets
import asyncio
import json
import time
import matplotlib.pyplot as plt

fig = plt.figure()
ax = fig.add_subplot(111)
fig.show()

xdata = []
ydata = []
symbol = "eth"

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


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main(symbol))


