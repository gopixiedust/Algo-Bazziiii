from flask import Blueprint, render_template, request, redirect, url_for, flash
from datetime import  date
from dateutil.relativedelta import relativedelta
from jugaad_data.nse import stock_df,index_df
import pandas as pd
import numpy as np
from nsetools import Nse
import plotly.graph_objects as go
import plotly.io as pio
pio.templates.default = "plotly_dark"

views = Blueprint('views', __name__)
nse = Nse()


def stonks(df):        
    returnVal=0
    df.drop(['SERIES', 
        'VWAP', '52W H', '52W L', 'VOLUME', 'VALUE', 'NO OF TRADES', 'SYMBOL'],inplace=True,axis=1)
    df=df[::-1]
    df=df.reset_index()
    pd.options.display.max_columns = None
    emadf = pd.DataFrame({'CLOSE':df['CLOSE']})
    emadf['EMA100'] = emadf['CLOSE'].ewm(span=100, min_periods=0, adjust=True).mean()
    emadf['EMA50'] = emadf['CLOSE'].ewm(span=50, min_periods=0, adjust=True).mean()
    ema100 = emadf['EMA100'].iloc[-1]
    ema50 = emadf['EMA50'].iloc[-1]
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
    sodf = pd.DataFrame(df[-14::]) # get latest 14 days
    c = sodf['CLOSE'].iloc[-1]
    l = sodf['LOW'].min()
    h = sodf['HIGH'].max()
    so = (c-l)/(h-l) * 100
    delta = df['CLOSE'].diff()
    up = delta.clip(lower=0)
    down = -1*delta.clip(upper=0)
    ema_up = up.ewm(com=13, adjust=True).mean()
    ema_down = down.ewm(com=13, adjust=True).mean()
    df['RSI'] = 100 - (100/(1 + (ema_up/ema_down)))
    if (ema50>ema100):
        returnVal+=1
    if (rsi<30):
        returnVal+=1
    if (so<20):
        returnVal+=1
    return returnVal

def chart(df,query):
    fig = go.Figure(data=[go.Candlestick(x=df['DATE'],
                open=df['OPEN'], high=df['HIGH'],
                low=df['LOW'], close=df['CLOSE'])])
   
    fig.update_layout(xaxis_rangeslider_visible=False,title= query+' Candlestick Plot')
    
    return fig
def nifty_chart(df):
    fig = go.Figure(data=[go.Candlestick(x=df['HistoricalDate'],
                open=df['OPEN'], high=df['HIGH'],
                low=df['LOW'], close=df['CLOSE'])
                     ])
    
    fig.update_layout(xaxis_rangeslider_visible=False,title='Nifty 50 Candlestick Plot')
    
    return fig
    
@views.route('/')
def index():
    return render_template('index.html')


@views.route('/about')
def about():
    return render_template('about.html')

@views.route('/stock',methods=['GET','POST'])
def stock():
    query=""
    data=pd.DataFrame()
    res=-1
    check=0
    if request.method == 'POST':
        query=request.form.get('query').upper()

        if nse.is_valid_code(query)==False:
            flash('Invalid Stock Code',category='error')
            return render_template('stockstats.html',query=query,data=data,res=res,check=check)
        elif nse.is_valid_code(query)==True:
            data=stock_df(symbol=query, from_date=date.today()-relativedelta(months=6),to_date=date.today(), series="EQ")
            res=stonks(data) 
            check=1       
            # print(res)
            return render_template('stockstats.html',query=query,res=res,chart=chart(data,query).to_html(),check=check)
        
    return render_template('stockstats.html',query=query,data=data,res=res,check=check)
    


@views.route('/nifty',methods=['GET','POST'])
def nifty():
    data=index_df(symbol="NIFTY 50", from_date=date.today()-relativedelta(months=6),to_date=date.today())    
    return render_template('nifty.html',chart=nifty_chart(data).to_html())

@views.route('/portfolio')
def portfolio():
    return render_template('portfolio.html')
