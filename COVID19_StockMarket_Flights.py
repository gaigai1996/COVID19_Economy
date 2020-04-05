#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import os
from datetime import date
from datetime import datetime
from time import strptime
import numpy as np

today = datetime.today()


# In[2]:


path='D:\Professional Development\Personal Projects\COVID-19-master\COVID-19-master\csse_covid_19_data\csse_covid_19_time_series'
os.chdir(path)

global_cc_ts=pd.read_csv(r'time_series_covid19_confirmed_global.csv')
us_cc_ts=pd.read_csv(r'time_series_covid19_confirmed_us.csv')


# In[5]:


path_dr='D:\Professional Development\Personal Projects\COVID-19-master\COVID-19-master\csse_covid_19_data\csse_covid_19_daily_reports'
os.chdir(path_dr)

global_dr=pd.read_csv(r'04-04-2020.csv')


# In[11]:


us_cc_ts_agg=global_cc_ts[global_cc_ts['Country/Region']=='US']
us_cc_ts_agg


# In[19]:



us_cc_ts_agg_t=us_cc_ts_agg.drop(['Province/State','Country/Region','Lat','Long'], axis=1)
us_cc_ts_agg_t=us_cc_ts_agg_t.transpose().reset_index()
us_cc_ts_agg_t.columns=['date','cummulative_count']
us_cc_ts_agg_t.date = pd.to_datetime(us_cc_ts_agg_t.date)


# In[92]:


temp=list(us_cc_ts_agg_t['cummulative_count'])
us_cc_ts_agg_t=us_cc_ts_agg_t.drop(0,axis=0)
us_cc_ts_agg_t['prev_day_cumm']=temp[:-1]
us_cc_ts_agg_t['daily_count']=us_cc_ts_agg_t['cummulative_count']-us_cc_ts_agg_t['prev_day_cumm']
us_cc_ts_agg_t=us_cc_ts_agg_t.drop('prev_day_cumm',axis=1)
# us_cc_ts_agg_t.head(10)


# In[113]:


## Weekly Aggregation
# us_cc_ts_agg_t.iloc[::7, :]
# us_cc_ts_agg_wkly = us_cc_ts_agg_t.groupby(np.arange(len(us_cc_ts_agg_t[['date','daily_count']]))//7).sum().reset_index()


# ### Importing NASDAQ Data

# In[106]:


import yfinance as yf
df_nasdaq = yf.download("^IXIC", start="2020-01-21", end="2020-04-4")


# In[107]:



df_nasdaq=df_nasdaq.reset_index()
df_nasdaq['Date'] = pd.to_datetime(df_nasdaq['Date'])


# In[110]:


df_covid_nasdaq=us_cc_ts_agg_t.merge(df_nasdaq[['Date','Close']], left_on='date', right_on='Date', how='left')
df_covid_nasdaq.head(10)


# In[117]:


#weekly aggregation
# df_week = df_nasdaq[['Date','Close']].groupby(np.arange(len(df_nasdaq[['Date','Close']]))//5).mean().reset_index()

df_covid_nasdaq=df_covid_nasdaq.dropna()
df_covid_nasdaq=df_covid_nasdaq.drop('Date',axis=1)
df_covid_nasdaq.head(10)


# In[123]:


import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from sklearn.preprocessing import MinMaxScaler


# In[124]:


scaler=MinMaxScaler()

df_covid_nasdaq_sc = scaler.fit_transform(df_covid_nasdaq[['daily_count','Close']])


# In[156]:


plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%m-%d'))
plt.gca().xaxis.set_major_locator(mdates.DayLocator())
plt.rcParams["figure.figsize"] = (30,20)
plt.plot(df_covid_nasdaq['date'],df_covid_nasdaq_sc)
plt.gcf().autofmt_xdate()


# In[ ]:





# In[ ]:




