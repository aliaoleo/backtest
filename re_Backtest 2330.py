# -*- coding: utf-8 -*-
"""
Created on Thu Jan  4 15:53:10 2018

@author: hh
"""

import pandas as pd
import datetime as dt
import os
import matplotlib.pyplot as plt

def plot_data(df, title="Stock prices", xlabel="Date", ylabel="Price"):
    """Plot stock prices with a custom title and meaningful axis labels."""
    ax = df.plot(title=title, fontsize=12)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    plt.show()
    
path = "/Users/hh/Document_lc/PythonWorkspace/Input/2330.txt"
end = dt.date(2015,6,30)
begin = end - dt.timedelta(days = 250)
date_range = pd.date_range(begin, end)
file = pd.read_csv(path,index_col="date",parse_dates=True,na_values=["nan"])
df = pd.DataFrame(index = date_range)
df = df.join(file)
df = df.dropna()
df['close'].plot()
plt.show()

len = 60
df["ma"] = df["close"].rolling(window = len).mean()
print(df.tail())

condition1 = (df["close"].shift(2) < df["ma"].shift(2)) & (df["close"].shift(1) > df["ma"].shift(1))
condition2 = (df["close"].shift(2) > df["ma"].shift(2)) & (df["close"].shift(1) < df["ma"].shift(1))

df["idx"] = 0
df["entry"] = 0
df["exit"] = 0
df["equity"] = 0.
df["cum_rtn"] = 0.
df["daily_pnl_pct"] = 0.

df["idx"][condition1] = 1
df["entry"][condition1] = (df["high"] + df["low"])/2

i =0
for i in range(df.size):
    i = i + 1
    while [df.idx ==1]:
        df["idx"][df.idx.shift(1) == 1] = 1
        df["entry"][(df.idx.shift(1) == 1) & (df.idx!=0)] = df.entry.shift(1)
        df["entry"][condition1] = (df["high"] + df["low"])/2
        
        if [condition2]:
            df["idx"][condition2] = 0
            break
df["exit"][(df.idx.shift(1) == 1) & (df.idx == 0)] = (df["high"] + df["low"]) /2
df["equity"][(df.idx.shift(1) == 0) & (df.idx ==1)] = df.idx * (df.close - df.entry)
df["equity"][(df.idx.shift(1) == 1) & (df.idx ==1)] = df.idx * (df.close - df.close.shift(1))
df["equity"][(df.idx.shift(1) == 1) & (df.idx == 0)] = df.exit - df.entry.shift(1)
df["daily_pnl_pct"][(df.entry !=0)] = df["equity"] / df["entry"]
df["cum_rtn"] = df["daily_pnl_pct"].cumsum()
df["cum_rtn"].plot()
plt.show()

