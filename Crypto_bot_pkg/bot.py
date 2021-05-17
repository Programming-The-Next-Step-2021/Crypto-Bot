import websocket

cc = 'btcusd'
interval = '1m'
SOCKET = f"wss://stream.binance.com:9443/ws/{cc}t@trade"

def on_message(ws, message): 
    print("received message")   
    print(message)

def on_open(ws):
    print('opened connection')

def on_close(ws):
    print('closed connection')

ws = websocket.WebSocketApp(SOCKET, on_open=on_open, on_message = on_message, on_close = on_close)

ws.run_forever()

# ws = websocket.WebSocketApp(SOCKET, on_open=on_open, on_close=on_close, on_message=on_message)
# ws.run_forever()