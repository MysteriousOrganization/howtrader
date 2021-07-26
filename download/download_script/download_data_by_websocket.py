import websocket
import os
import json
import csv
import datetime
try:
    import thread
except ImportError:
    import _thread as thread
import time
SYMBOL = "btcusdt"
DEPTH_STREAM = "{}@depth20@100ms".format(SYMBOL)
TRADE_STREAM = "{}@aggTrade".format(SYMBOL)

def on_message(ws, message):
    res = dict(json.loads(message))
    filename = ""
    today = (datetime.datetime.now() + datetime.timedelta(hours=-12)).strftime('%Y%m%d')
    if res["stream"] == DEPTH_STREAM :
        filename = '../data/{}_future_depth.csv.{}'.format(SYMBOL, today)
    else:
        filename = '../data/{}_future_trade.csv.{}'.format(SYMBOL, today)
    file_exist = os.path.exists(filename)
    with open(filename, 'a') as f:
        data = res['data']
        #f.write(str(data)+'\n')
        w = csv.DictWriter(f, data.keys())
        if not file_exist:
            w.writeheader()
        w.writerow(data)


def on_error(ws, error):
    print("error")
    print(error)

def on_close(ws, *close_args):
    print(close_args)
    print("### closed ###")

def on_ping(ws, msg):
    print("Got a ping!")
    ws.send('', 0xa)
    print("Sent a pong!")

#websocket.enableTrace(True)
ws = websocket.WebSocketApp("wss://fstream.binance.com/stream?streams={}/{}".format(DEPTH_STREAM, TRADE_STREAM),
                          on_message = on_message,
                          on_error = on_error,
                          on_close = on_close,
                          on_ping = on_ping)
ws.run_forever(sslopt={"check_hostname": False})
