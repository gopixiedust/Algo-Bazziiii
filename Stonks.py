
returnVal=0
symbol=input()
from datetime import  date,timedelta
from jugaad_data.nse import  stock_df

# Download as pandas dataframe
df = stock_df(symbol=symbol, from_date=date.today()-timedelta(days=200),
            to_date=date.today(), series="EQ")
# df.head(10)
df.drop(['SERIES', 
       'VWAP', '52W H', '52W L', 'VOLUME', 'VALUE', 'NO OF TRADES', 'SYMBOL'],inplace=True,axis=1)
df=df[::-1]
# df=df[0:101]
# df=df.reset_index()
df=df.reset_index()
# print(df.tail(10))
# retreiving and storing data - changed source of data, this one is old
import numpy as np
import pandas as pd

pd.options.display.max_columns = None

# import requests

# key = 'ZZW44UFCBUQQUQLP'
# symbol = 'INFY'

# url = f'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={symbol}&apikey={key}'
# r = requests.get(url)
# data = r.json()['Time Series (Daily)']

# df = pd.DataFrame(columns = ['Date', 'Open', 'High', 'Low', 'Close'])

# for day in data.keys():
#   df = df.append({'Date': day, 'Open': data[day]['1. open'], 'High': data[day]['2. high'], 'Low': data[day]['3. low'], 'Close': data[day]['4. close']}, ignore_index=True)
# df['Open'] = pd.to_numeric(df['Open'])
# df['High'] = pd.to_numeric(df['High'])
# df['Low'] = pd.to_numeric(df['Low'])
# df['Close'] = pd.to_numeric(df['Close'])

# df = df[::-1]
# df = df.reset_index()
# del df['index']

# df
# calculating EMAs - works
emadf = pd.DataFrame({'CLOSE':df['CLOSE']})

emadf['EMA100'] = emadf['CLOSE'].ewm(span=100, min_periods=0, adjust=True).mean()
emadf['EMA50'] = emadf['CLOSE'].ewm(span=50, min_periods=0, adjust=True).mean()

ema100 = emadf['EMA100'].iloc[-1]
ema50 = emadf['EMA50'].iloc[-1]

# if (ema50>ema100):
#   returnVal+=1

# print(returnVal)
# print('ema100: ', ema100)
# print('ema50: ', ema50)
# calculating RSI - works
rsidf = pd.DataFrame({'CLOSE':df['CLOSE']})

def rma(x, n, y0):
    a = (n-1) / n
    ak = a**np.arange(len(x)-1, -1, -1)
    return np.r_[np.full(n, np.nan), y0, np.cumsum(ak * x) / ak / n + y0 * a**np.arange(1, len(x)+1)]

n=14

rsidf['change'] = rsidf['CLOSE'].diff()
rsidf['change'][0] = 0
rsidf['gain'] = rsidf.change.mask(rsidf.change < 0, 0.0)
rsidf['loss'] = -rsidf.change.mask(rsidf.change > 0, -0.0)
rsidf['avg_gain'] = rma(rsidf.gain[n+1:].to_numpy(), n, np.nansum(rsidf.gain.to_numpy()[:n+1])/n)
rsidf['avg_loss'] = rma(rsidf.loss[n+1:].to_numpy(), n, np.nansum(rsidf.loss.to_numpy()[:n+1])/n)
rsidf['rs'] = rsidf.avg_gain / rsidf.avg_loss
rsidf['rsi_14'] = 100 - (100 / (1 + rsidf.rs))

rsi = rsidf['rsi_14'][99]
# print('rsi: ', rsi)
# calculating stochastic oscillator - works

sodf = pd.DataFrame(df[-14::]) # get latest 14 days

c = sodf['CLOSE'].iloc[-1]
l = sodf['LOW'].min()
h = sodf['HIGH'].max()

so = (c-l)/(h-l) * 100

# print('so: ', so)
# redundant (?)

delta = df['CLOSE'].diff()
up = delta.clip(lower=0)
down = -1*delta.clip(upper=0)
ema_up = up.ewm(com=13, adjust=True).mean()
ema_down = down.ewm(com=13, adjust=True).mean()
rs = ema_up/ema_down

df['RSI'] = 100 - (100/(1 + rs))
df.RSI
if (ema50>ema100):
      returnVal+=1
if (rsi<30):
  returnVal+=1
if (so<20):
  returnVal+=1
print(returnVal);
