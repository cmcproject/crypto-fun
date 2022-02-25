from binance import Client
from config.config import API_KEY, API_SECRET
import pandas as pd

client = Client(API_KEY, API_SECRET)


def get_data(symbol, interval, start, see=False):
    df = pd.DataFrame(client.get_historical_klines(symbol, interval, start + ' ago UTC'))
    df = df.iloc[:, :5]
    df.columns = ["Time", "Open", "High", "Low", "Close"]
    df[["Open", "High", "Low", "Close"]] = df[["Open", "High", "Low", "Close"]].astype(float)
    df.Time = pd.to_datetime(df.Time, unit='ms')

    # Cumulative Return
    # Rc = (Pcurrent – Pinitial) / Pinitial
    # Rc = (Pcurrent / Pinitial) - 1
    df['Compared with prev [%]'] = df.Close.pct_change() * 100
    df['Cumulative Return [%]'] = ((df.Close.pct_change() + 1).cumprod() - 1) * 100

    if see:
        print(df)
    df.to_csv('BTC.csv')
    return df


def run_strategy(symbol, quantity, entried=False):
    """
    Buy if asset falls by more than 0.2%
    Sell if asset rises by more then 0.15% or falls further by 0.15%
    """
    df = get_data(symbol, '1m', '30m')
    cumulret = (df.Open.pct_change() + 1).cumprod() - 1
    cumulret = cumulret.iloc[-1]
    if not entried:
        if cumulret < -0.002:
            order = client.create_test_order(symbol=symbol, side='BUY', type='MARKET', quantity=quantity)
            print('BUY: \n', order)
            entried = True
        else:
            print('No trade has been executed')

    if entried:
        while True:
            df = get_data(symbol, '1m', '30m')
            sincebuy = df.loc[df.index > pd.to_datetime(order['transactTime'], unit='ms')]

            if len(sincebuy) > 0:
                sincebuyret = (sincebuy.Open.pct_change() + 1).cumprod() - 1
                sincebuyret = sincebuyret.iloc[-1]
                if sincebuyret[-1] > 0.0015 or sincebuyret[-1] < -0.0015:
                    order = client.create_test_order(symbol=symbol, side='SELL', type='MARKET', quantity=quantity)

                    print('SELL :\n', order)


def get_quantity_per_usdt(usdt, symbol):
    info = client.get_symbol_info(symbol=symbol + 'USDT')
    price = client.get_symbol_ticker(symbol=symbol + 'USDT')

    # print("Minimum quantity: ", info['filters'][2]['minQty'])

    return_1_position = info['filters'][2]['minQty'].replace(".", "").split("0").index("1")
    if return_1_position:
        quantity = round(usdt / float(price['price']), return_1_position)
    else:
        quantity = round(usdt / float(price['price']))

    print(f"Quantity for {usdt} USDT: {quantity} {symbol}")
