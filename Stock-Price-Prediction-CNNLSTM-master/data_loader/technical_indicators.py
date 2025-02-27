
"""

Pandas wrapper of TA-lib functions

Technical indicators:

MA - moving average
EMA - exponential moving average
MOM - momentum
ROC - rate of change
ATR - average true range
BBands - bollinger bands
RSI - relative strength index
MACD - Moving Average Convergence Divergencew
william_r_% - Williams Percent Range
k% - slow stochastic indicator
D% - fast stochastic indicator
A/D - accumulation/distribution


"""
import os
import numpy as np
import pandas as pd
import talib as ta

def moving_average(df, small_win, big_win):

    MA_s = ta.SMA(df['Close'], timeperiod=small_win)
    MA_b = ta.SMA(df['Close'], timeperiod=big_win)

    MA = pd.Series((MA_b-MA_s)/MA_s, name='SMA_{}_{}'.format(small_win, big_win))
    df = df.join(MA)
    return df


def exponential_moving_average(df, small_win, big_win):
    """

    :param df: pandas.DataFrame
    :param n:
    :return: pandas.DataFrame
    """
    EMA_2 = df['Close'].ewm(span=small_win, min_periods=small_win).mean()
    EMA_n = df['Close'].ewm(span=big_win, min_periods=big_win).mean()

    EMA = pd.Series((EMA_n-EMA_2)/EMA_2, name='EMA_{}_{}'.format(small_win, big_win))
    df = df.join(EMA)
    return df


# def future_moving_average(df, n):
#     # reverse the series to get future moving aveerage
#     f_MA_n = ta.SMA(df['Close'][::-1], timeperiod=n)
#     MA_shift = df['Close'][::-1].shift(-1, axis=0)
#
#     fMA = pd.Series((f_MA_n-MA_shift)/MA_shift, name='f_MA_{}'.format(n))
#     df = df.join(fMA)
#     return df


def future_moving_average(df, n):
    # reverse the series to get future moving aveerage
    f_MA_n = df['Close'][::-1].rolling(window=n).mean()
    MA_shift = df['Close'][::-1].shift(-1, axis=0)

    fMA = pd.Series((f_MA_n-MA_shift)/MA_shift, name='FSMA_{}'.format(n))
    df = df.join(fMA)
    return df


# def future_exponential_moving_average(df, n):
#     # reverse the series to get future moving aveerage
#     f_MA_n = ta.EMA(df['Close'][::-1], timeperiod=n)
#     EMA_shift = df['Close'][::-1].shift(-1, axis=0)
#
#     fMA = pd.Series((f_MA_n-EMA_shift)/EMA_shift, name='f_EMA_{}'.format(n))
#     df = df.join(fMA)
#     return df


def future_exponential_moving_average(df, n):
    # reverse the series to get future moving aveerage
    f_MA_n = df['Close'][::-1].ewm(span=n, min_periods=n).mean()
    EMA_shift = df['Close'][::-1].shift(-1, axis=0)

    fMA = pd.Series((f_MA_n-EMA_shift)/EMA_shift, name='FEMA_{}'.format(n))
    df = df.join(fMA)
    return df


def momentum(df, n):
    """

    :param df: pandas.DataFrame
    :param n:
    :return: pandas.DataFrame
    """
    M = pd.Series(df['Close'].diff(n), name='MOM_' + str(n))
    df = df.join(M)
    return df


def rate_of_change(df, n):
    """

    :param df: pandas.DataFrame
    :param n:
    :return: pandas.DataFrame
    """
    # M = df['Close'].diff(n - 1)
    # N = df['Close'].shift(n - 1)
    # this function can also calculate n-day return

    ROC = pd.Series(df['Close'].pct_change(n)*100, name='ROC_' + str(n))
    if n >= 5: # make timeframe match
        ROC[4] = 0.1
    if not 'ROC_' + str(n) in df:
        df = df.join(ROC)

    return df


def average_true_range(df, n):
    """

    The average true range (ATR) is a technical analysis indicator that measures market volatility
    by decomposing the entire range of an asset price for that period.
    """
    # Result a little different from that of Yahoo Finance

    ATR = pd.Series(ta.ATR(df['High'], df['Low'], df['Close']), name='ATR_' + str(n))
    df = df.join(ATR)
    return df


def bollinger_bands_ub(df, n):
    """

    A Bollinger Band® is a technical analysis tool defined by a set of lines plotted two standard deviations (positively and negatively)
     away from a simple moving average (SMA) of the security's pric
    """
    upperband, middleband, lowerband = ta.BBANDS(df['Close'], timeperiod=n, nbdevup=2, nbdevdn=2, matype=0)

    ub = pd.Series(upperband, name='BB_'+'UB_' + str(n))
    # mb = pd.Series(middleband, name='mb_' + str(n))
    # lb = pd.Series(lowerband, name='lb_' + str(n))

    df = df.join(ub)
    # df = df.join(mb)
    # df = df.join(lb)

    return df


def bollinger_bands_mb(df, n):
    """

    A Bollinger Band® is a technical analysis tool defined by a set of lines plotted two standard deviations (positively and negatively)
     away from a simple moving average (SMA) of the security's pric
    """
    upperband, middleband, lowerband = ta.BBANDS(df['Close'], timeperiod=n, nbdevup=2, nbdevdn=2, matype=0)

    mb = pd.Series(middleband, name='BB_'+'MB_' + str(n))

    df = df.join(mb)

    return df


def bollinger_bands_lb(df, n):
    """

    A Bollinger Band® is a technical analysis tool defined by a set of lines plotted two standard deviations (positively and negatively)
     away from a simple moving average (SMA) of the security's pric
    """
    upperband, middleband, lowerband = ta.BBANDS(df['Close'], timeperiod=n, nbdevup=2, nbdevdn=2, matype=0)

    lb = pd.Series(lowerband, name='BB_'+'LB_' + str(n))

    df = df.join(lb)

    return df


def relative_strength_index(df, n):
    """Calculate Relative Strength Index(RSI) for given data.

    :param df: pandas.DataFrame
    :param n:
    :return: pandas.DataFrame
    """
    RSI = pd.Series(ta.RSI(df['Close'],n),name = 'RSI_'+str(n))

    df = df.join(RSI)

    return df


def MACD_macd(df):
    """
        The MACD is the difference between a 26-day and 12-day exponential moving average of closing prices.
        A 9-day EMA, called the "signal" line is plotted on top of the MACD to show buy/sell opportunities.
    """
    macd, macdsignal, macdhist = ta.MACD(df['Close'], fastperiod=12, slowperiod=26, signalperiod=9)

    Macd = pd.Series(macd, name="MACD_" + 'MACD')

    df = df.join(Macd)
    return df


def MACD_signal(df):
    """
        The MACD is the difference between a 26-day and 12-day exponential moving average of closing prices.
        A 9-day EMA, called the "signal" line is plotted on top of the MACD to show buy/sell opportunities.
    """
    macd, macdsignal, macdhist = ta.MACD(df['Close'], fastperiod=12, slowperiod=26, signalperiod=9)

    Macdsignal = pd.Series(macdsignal, name='MACD_' + 'SIGNAL')

    df = df.join(Macdsignal)
    return df


def MACD_hist(df):
    """
        The MACD is the difference between a 26-day and 12-day exponential moving average of closing prices.
        A 9-day EMA, called the "signal" line is plotted on top of the MACD to show buy/sell opportunities.
    """
    macd, macdsignal, macdhist = ta.MACD(df['Close'], fastperiod=12, slowperiod=26, signalperiod=9)

    Macdhist = pd.Series(macdhist, name='MACD_' + 'HIST')

    df = df.join(Macdhist)
    return df



def william_r(df,n):
    """
    The Williams Percent Range, also called Williams %R, is a momentum indicator that shows you
    where the last closing price is relative to the highest and lowest prices of a given time period.
    """
    # real = WILLR(high, low, close, timeperiod=14)
    w_r = pd.Series(ta.WILLR(df['High'],df['Low'],df['Close'],timeperiod=n),name = "WR_" + str(n))
    df  = df.join(w_r)
    return df


def stocha_osc_k(df):
    """

    A stochastic oscillator is a momentum indicator comparing a particular closing price of a security
    to a range of its prices over a certain period of time.

    slowk, slowd = STOCH(high, low, close, fastk_period=5, slowk_period=3, slowk_matype=0, slowd_period=3, slowd_matype=0)

    %K is referred to sometimes as the slow stochastic indicator.
    The "fast" stochastic indicator is taken as %D = 3-period moving average of %K.

    """
    slowk,slowd = ta.STOCH(df['High'],df['Low'],df['Close'],fastk_period=5, slowk_period=3, slowk_matype=0, slowd_period=3,slowd_matype=0)

    k_line = pd.Series(slowk,name = "STOCHA_" + "K")

    return df.join(k_line)



def stocha_osc_d(df):
    """
    A stochastic oscillator is a momentum indicator comparing a particular closing price of a security
    to a range of its prices over a certain period of time.

    slowk, slowd = STOCH(high, low, close, fastk_period=5, slowk_period=3, slowk_matype=0, slowd_period=3, slowd_matype=0)

    %K is referred to sometimes as the slow stochastic indicator.
    The "fast" stochastic indicator is taken as %D = 3-period moving average of %K.

    """
    slowk,slowd = ta.STOCH(df['High'],df['Low'],df['Close'],fastk_period=5, slowk_period=3, slowk_matype=0, slowd_period=3,slowd_matype=0)

    d_line = pd.Series(slowd,name = "STOCHA_" +"D")

    return df.join(d_line)



def acc_dist(df):
    """
    Accumulation/distribution is a cumulative indicator that uses volume and price to assess whether a stock is being accumulated or distributed.
    The accumulation/distribution measure seeks to identify divergences between the stock price and volume flow
    This value is different from that of Yahoo Finance
    """

    CMFV = pd.Series(ta.AD(df['High'], df['Low'], df['Close'],df['Volume']), name="ACC")
    df = df.join(CMFV)
    return df