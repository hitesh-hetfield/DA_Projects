#!/usr/bin/env python
# coding: utf-8

# # Welcome to the Notebook

# ### Importing modules

# ### Task 1

# In[1]:


import pandas as pd
import numpy as np
import plotly.express as px
import matplotlib.pyplot as plt 
import seaborn as sns
print('modules are imported')


# ### Task 1.1: 
# #### Loading the Dataset

# In[2]:


dataset_url = r'https://raw.githubusercontent.com/datasets/covid-19/master/data/countries-aggregated.csv'

df = pd.read_csv(dataset_url)


# ### Task 1.2:
# #### let's check the dataframe 

# In[3]:


df.head()


# In[4]:


df.tail()


# In[5]:


df.info()


# #### let's check the shape of the dataframe 

# In[6]:


df.shape


# ### Task 2.1 :
# #### let's do some processing

# In[7]:


# # Changing the date column dtype to datetime
df['Date'] = pd.to_datetime(df['Date'])

# # Getting the index of the first confirmed case in each country
# first_confirmed_case = df.query('Confirmed > 0').groupby('Country')['Date'].idxmin()

# # Getting the values corresponding to the above.
# df.loc[first_confirmed_case]

df = df.query('Confirmed > 0')


# #### let's see data related to a country for example Italy 
# 

# In[8]:


df[df['Country'] == 'Italy']


# #### let's see Global spread of Covid19

# In[9]:


fig = px.choropleth(df, locations='Country', locationmode='country names', color = 'Confirmed')
fig.update_layout(title_text = 'Global Spread of Covid-19')
fig.show()


# ### Task 2.2 : Exercise 
# #### Let's see Global deaths of Covid19

# In[10]:


fig = px.choropleth(df, locations='Country', locationmode='country names', 
                   color = 'Deaths')
fig.update_layout(title_text = 'Global Deaths of Covid-19')
fig.show()


# ### Task 3.1:
# #### Let's Visualize how intensive the Covid19 Transmission has been in each of the country
# let's start with an example:

# In[11]:


df_china = df[df['Country'] == 'China']
df_china.head()


# let's select the columns that we need

# In[12]:


df_china = df_china[['Date', 'Confirmed']]


# In[13]:


df_china.head()


# calculating the first derivation of confrimed column

# In[14]:


df_china['Infection Rate'] = df_china['Confirmed'].diff()


# In[15]:


df_china.head()


# In[16]:


px.line(df_china, x = 'Date', y = ['Confirmed', 'Infection Rate'],
                  title='Infection Rate Intensity')


# In[17]:


df_china['Infection Rate'].max()


# ### Task 3.2:
# #### Let's Calculate Maximum infection rate for all of the countries

# In[18]:


df.head()


# ### Task 3.3:
# #### let's create a new Dataframe 

# In[19]:


countries = list(df['Country'].unique())
max_infection_rates = []

for country in countries:
    mir = df[df['Country'] == country]['Confirmed'].diff().max()
    max_infection_rates.append(mir)


# In[20]:


df_mir = pd.DataFrame()
df_mir['Country'] = countries
df_mir['Max Infection Rate'] = max_infection_rates
df_mir.head()


# #### Let's plot the barchart : maximum infection rate of each country

# In[21]:


plt.figure(figsize=(15,10), dpi=500)

px.bar(df_mir, x='Country', y='Max Infection Rate', color = 'Country',
      title='Global Maximum Infection Rate', log_y=True)


# ### Task 4: Let's See how National Lockdowns Impacts Covid19 transmission in Italy

# ### COVID19 pandemic lockdown in Italy 
# On 9 March 2020, the government of Italy under Prime Minister Giuseppe Conte imposed a national quarantine, restricting the movement of the population except for necessity, work, and health circumstances, in response to the growing pandemic of COVID-19 in the country. <a href="https://en.wikipedia.org/wiki/COVID-19_pandemic_lockdown_in_Italy#:~:text=On%209%20March%202020%2C%20the,COVID%2D19%20in%20the%20country.">source</a>

# In[22]:


italy_lockdown_start_date = '2020-03-09'
italy_lockdown_a_month_later = '2020-04-09'


# In[23]:


df.head()


# let's get data related to italy

# In[24]:


df_italy = df[(df['Country'] == 'Italy')]


# lets check the dataframe

# In[25]:


df_italy.head()


# let's calculate the infection rate in Italy

# In[26]:


df_italy['Infection Rate'] = df_italy['Confirmed'].diff()

df_italy.tail()


# ok! now let's do the visualization

# In[27]:


fig = px.line(df_italy, x='Date', y='Infection Rate', title='Before and After Lockdown in Italy')
fig.add_shape(
dict(
type='line', 
    x0=italy_lockdown_start_date,
    y0=0,
    x1=italy_lockdown_start_date,
    y1=df_italy['Infection Rate'].max(),
    line = dict(color = 'red', width=2))
)

fig.add_annotation(
dict(
    x = italy_lockdown_start_date,
    y= df_italy['Infection Rate'].max(),
    text = 'Starting Date of the Lockdown'
)
)

fig.add_shape(
dict(
type='line', 
    x0=italy_lockdown_a_month_later,
    y0=0,
    x1=italy_lockdown_a_month_later,
    y1=df_italy['Infection Rate'].max(),
    line = dict(color = 'orange', width=2)
)
)

fig.add_annotation(
dict(
    x = italy_lockdown_a_month_later,
    y= 0,
    text = 'A month later'
)
)


# ### Task 5: Let's See how National Lockdowns Impacts Covid19 active cases in Italy

# In[28]:


df_italy.head()


# let's calculate number of active cases day by day 

# In[29]:


df_italy['Active Cases'] = (df_italy['Confirmed']) - (df_italy['Recovered'].diff() + df_italy['Deaths'].diff())


# let's check the dataframe again

# In[30]:


df_italy


# now let's plot a line chart to compare COVID19 national lockdowns impacts on spread of the virus and number of active cases

# In[31]:


fig = px.line(df_italy, x='Date', y=['Infection Rate', 'Active Cases'], title='Number of Active Cases')
fig.show()


# #### 
# let's normalise these columns for a better visualisation

# In[32]:


df_italy['Infection Rate']= df_italy['Infection Rate']/df_italy['Infection Rate'].max()

df_italy['Active Cases']= df_italy['Active Cases']/df_italy['Active Cases'].max()


# In[33]:


fig = px.line(df_italy, x='Date', y=['Infection Rate', 'Active Cases'], title='Number of Active Cases')


fig.add_shape(
dict(
type='line', 
    x0=italy_lockdown_start_date,
    y0=0,
    x1=italy_lockdown_start_date,
    y1=df_italy['Infection Rate'].max(),
    line = dict(color = 'black', width=2))
)

fig.add_annotation(
dict(
    x = italy_lockdown_start_date,
    y= df_italy['Infection Rate'].max(),
    text = 'Starting Date of the Lockdown'
)
)

fig.add_shape(
dict(
type='line', 
    x0=italy_lockdown_a_month_later,
    y0=0,
    x1=italy_lockdown_a_month_later,
    y1=df_italy['Infection Rate'].max(),
    line = dict(color = 'yellow', width=2)
)
)

fig.add_annotation(
dict(
    x = italy_lockdown_a_month_later,
    y= 0,
    text = 'A month later'
)
)


# ### COVID19 pandemic lockdown in Germany 
# Lockdown was started in Freiburg, Baden-Württemberg and Bavaria on 20 March 2020. Three days later, it was expanded to the whole of Germany

# In[34]:


Germany_lockdown_start_date = '2020-03-23' 
Germany_lockdown_a_month_later = '2020-04-23'


# let's select the data related to Germany

# In[35]:


df_germany = df[df['Country'] == 'Germany']


# let's check the dataframe 

# In[36]:


df_germany.head()


# let's calculate the infection rate and death rate in Germany

# In[37]:


df_germany['Infection Rate'] = df_germany['Confirmed'].diff()
df_germany['Death Rate'] = df_germany['Deaths'].diff()


# let's check the dataframe

# In[38]:


df_germany.head()


# now let's plot the line chart

# In[39]:


fig = px.line(df_germany, x='Date', y=['Infection Rate', 'Death Rate'], title='Comparison of Infection and Death Rate')


fig.add_shape(
dict(
type='line', 
    x0=Germany_lockdown_start_date,
    y0=0,
    x1=Germany_lockdown_start_date,
    y1=df_germany['Infection Rate'].max(),
    line = dict(color = 'black', width=2))
)

fig.add_annotation(
dict(
    x = Germany_lockdown_start_date,
    y= df_germany['Infection Rate'].max(),
    text = 'Starting Date of the Lockdown'
)
)

fig.add_shape(
dict(
type='line', 
    x0= Germany_lockdown_a_month_later,
    y0=0,
    x1=Germany_lockdown_a_month_later, 
    y1=df_germany['Infection Rate'].max(),
    line = dict(color = 'yellow', width=2)
)
)

fig.add_annotation(
dict(
    x = Germany_lockdown_a_month_later,
    y= 0,
    text = 'A month later'
)
)


# let's do some scaling for better visualisation

# In[40]:


df_germany['Infection Rate'] = df_germany['Infection Rate']/df_germany['Infection Rate'].max()
df_germany['Death Rate'] = df_germany['Death Rate']/df_germany['Death Rate'].max()


# let's plot the line chart

# In[41]:


fig = px.line(df_germany, x='Date', y=['Infection Rate', 'Death Rate'], title='Comparison of Infection and Death Rate')


fig.add_shape(
dict(
type='line', 
    x0=Germany_lockdown_start_date,
    y0=0,
    x1=Germany_lockdown_start_date,
    y1=df_germany['Infection Rate'].max(),
    line = dict(color='black', width=2))
)

fig.add_annotation(
dict(
    x = Germany_lockdown_start_date,
    y= df_germany['Infection Rate'].max(),
    text = 'Starting Date of the Lockdown'
)
)

fig.add_shape(
dict(
type='line', 
    x0= Germany_lockdown_a_month_later,
    y0=0,
    x1=Germany_lockdown_a_month_later, 
    y1=df_germany['Infection Rate'].max(),
    line = dict(color = 'yellow', width=2)
)
)

fig.add_annotation(
dict(
    x = Germany_lockdown_a_month_later,
    y= 0,
    text = 'A month later'
)
)

