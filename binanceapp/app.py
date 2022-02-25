from binance import Client
from config.config import API_KEY, API_SECRET
import pandas as pd
from pprint import pprint
from helpers import get_quantity_per_usdt, get_data
from coins import *

import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

client = Client(API_KEY, API_SECRET)

if __name__ == '__main__':
    # Run strategy buy/sale
    # run_strategy(client, 'BTCUSDT', 0.00001)

    # check data
    df = get_data("EGLDUSDT", Client.KLINE_INTERVAL_1DAY, "90 days", see=True)

    # Get quantity per USDT
    # get_quantity_per_usdt(usdt=30.19, symbol=ADA)

    # Create order
    # order = client.create_order(symbol='SHIBUSDT', side='BUY', type='MARKET', quantity=buy_quantity)
    # print(order)

    # # Graphic representation
    # plt.style.use('ggplot')
    #
    # def animate(i):
    #     asset = "BTCUSDT"
    #     data = get_data(asset, '1m', "120 min")
    #     plt.cla()
    #     plt.plot(data.index, data.Close)
    #     plt.xlabel('Time')
    #     plt.ylabel('Price')
    #     plt.title(asset)
    #     plt.gcf().autofmt_xdate()
    #     plt.tight_layout()
    #
    # ani = FuncAnimation(plt.gcf(), animate, 1000)
    #
    # plt.tight_layout()
    # plt.show()



