#!/usr/bin/env python
# coding: utf-8

# In[42]:


##libraries to use ##
import pandas as pd
import numpy as np
import datetime as dt
import matplotlib.pyplot as plt
import plotly as py
import plotly.graph_objs as go

from plotly.offline import download_plotlyjs, init_notebook_mode, plot, iplot


# In[43]:


init_notebook_mode(connected=True)


# In[44]:


## user input -- read files ##
## Source of Info: https://oui.doleta.gov/unemploy/DataDownloads.asp
file_location = r"ar539.csv"
data = pd.read_csv(file_location, usecols=['st','rptdate','c1','c2','c3','c17','c19'])


# In[45]:


## data cleaning - header mapping ## 
data ['c2']=pd.to_datetime(data ['c2'])
data ['Year'] = pd.DatetimeIndex(data ['c2']).year
data ['rptdate']=pd.to_datetime(data ['rptdate'])
most_recent_reportdate=data ['rptdate'].max()
data ['c19'] = pd.to_numeric(data ['c19'])
data = data.set_axis(['State','ReportDate','Week_Number','Reflected_Week_Ending','Initial_Claims','Arg_Total_Weeks_Claimed','Rate_Insured_Unemployment','Year'], axis=1, inplace=False)


# In[47]:


## Method to get sum and average data in a period ## 

def get_data_range(begin, end):
    Criteria=(data ['Year']>=begin)&(data ['Year']<=end)
    data_static = data.loc[Criteria]
    total_claims = data_static['Initial_Claims'].sum()
    df1 = data_static.groupby(['Reflected_Week_Ending']).sum().reset_index()
    df2 = data_static.groupby(['Reflected_Week_Ending']).mean().reset_index()
    result = pd.merge(df1, df2, on='Reflected_Week_Ending',how='outer',suffixes=('_sum','_mean'))
    result = result[['Reflected_Week_Ending','Week_Number_mean','Initial_Claims_sum','Rate_Insured_Unemployment_mean']]
    return result

set1=get_data_range(2007,2015)
set2=get_data_range(2016,2020)


plt.figure(figsize=(10,8))
plt.plot(set1.Reflected_Week_Ending,set1.Initial_Claims_sum)
plt.plot(set2.Reflected_Week_Ending,set2.Initial_Claims_sum)
plt.title("US Unemployment Initial Claims Analysis")
plt.show()


# In[50]:


plt.figure(figsize=(10,8))
plt.plot(set1.Reflected_Week_Ending,set1.Rate_Insured_Unemployment_mean)
plt.plot(set2.Reflected_Week_Ending,set2.Rate_Insured_Unemployment_mean)
plt.title("US Unemployment Initial Claims/Unemployment Rate Analysis")
plt.show()


# In[11]:


## Geographic Most Recent ## 
Most_Recent_Criteria=(data ['ReportDate']==most_recent_reportdate)
df = data.loc[Most_Recent_Criteria]
df = df.drop(['ReportDate'],axis=1)
df.head()


# In[52]:


data = dict(type='choropleth',
            colorscale = 'Portland',
            locations = df['State'],
            z = df['Initial_Claims'],
            locationmode = 'USA-states',
            text = df['Rate_Insured_Unemployment'],
            marker = dict(line = dict(color = 'rgb(255,255,255)',width = 2)),
            colorbar = {'title':"Percentage"}
            )

lyt = dict(title = '2020 Most Recent Unemployment State Distribution',
              geo = dict(scope='usa'))

map = go.Figure(data=[data], layout = lyt)
plot(map)


# In[ ]:





# In[ ]:




