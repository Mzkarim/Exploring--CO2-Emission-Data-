
# coding: utf-8

# ## Exploring and Visualizing the Number of Out-of-School Children Around the World Using Python
# 

# ### Table of Contents 
# 
# * Getting Started with Data Scientist Workbench
# 
# * CO2 emissions by Country by Year
# 
# * Get the Data
# 
# * Import the data using Pandas
# 
# * Dataframe characteristics 
# 
# * Subsetting the Dataframe
# 
# * Conditional Subsetting
# 
# * Data Cleaning
# 
# * Data Exploration
# 
# * Creating an interactive searchable widget
# 
# * Resources
# * Other Datasets

# ## Getting Started with Data Scientist Workbench

# **To run a cell, press**
# 
# Ctrl+Enter or
# Shift+Enter

# **Print the current version of Python:**

# In[1]:

import sys
print sys.version


# ### Run bash commands using !

# In[2]:

get_ipython().system(u'ls')


# ### System Initialization

# In[3]:

reload(sys)
sys.setdefaultencoding('utf')


# ## CO2 emissions by Country by Year

# Carbon dioxide emissions are those stemming from the burning of fossil fuels and the manufacture of cement. They include carbon dioxide produced during consumption of solid, liquid, and gas fuels and gas flaring.
# 
# http://data.worldbank.org/indicator/EN.ATM.CO2E.PC/

# ## Get the Data
# 
# * The World Bank Data can be downloaded  
# [Here](http://data.worldbank.org/indicator/EN.ATM.CO2E.PC/)
# 

# ## Import the data using Pandas

# **Import required pandas library **

# In[4]:

import pandas as pd


# In[5]:

pd.__version__


# **Import data using pd.read_csv **

# In[6]:

data =pd.read_csv("E:/Data Collection/co2emissions.csv",skiprows =4)


# In[8]:

type(data)    # Checks the type of object


# In[9]:

data


# **Display first 5 rows of data using head**
# 

# In[10]:

data.head()


# **Take just the first two rows using head**

# In[11]:

data.head(2)


# In[12]:

data.head(n=1)


# ### When we don't remember what the parameters are for a function? Use ?

# In[13]:

#To close help window, press q
get_ipython().magic(u'pinfo data.hrad')


# **Display last 7 rows of data**

# In[14]:

data.tail(7)


# ##Dataframe characteristics

# **How many rows and columns are there?**

# In[15]:

data.shape   #(rows,columns)


# In[16]:

data.describe()


# **What are the column names?**

# In[17]:

data.columns


# **What is the first column name?**
# 

# In[18]:

data.columns[0]


# **What is the first and second column name?**

# In[19]:

data.columns[[0,1]]


# **Print the names of the first and last column names**

# In[21]:

data.columns[[0,-1]]


#    ##Subsetting the Dataframe

# ### Select columns 

# **Select columns ny name :**

# In[22]:

data['Country Name']


# **Select columns by column number:**

# In[23]:

data[data.columns[0]]


# **Select the last column:**

# In[24]:

data[data.columns[-1]]


# **Subset Multiple Columns by Name**

# In[25]:

data[['Country Name','Country Code']]


# ### Select rows

# ** A different ways : **

# In[26]:

data[0:1]     # First row


# In[28]:

data.iloc[[0]]   # First row


# ** Select the last row **

# In[29]:

data.iloc[-1]


#    ##Conditional Subsetting

# **Recall: there are various logical operators to create logical statements:**

# In[30]:

1==2


# In[31]:

"Me"!="You"


# In[32]:

1000>1


# When we apply a logical statement to an array, an array of Trues/Falses are returned, with respect to the logical statement.

# In[33]:

import numpy as np
my_range = np.array(range(1,100))
my_range


# In[34]:

truefalse = my_range > 50
truefalse


# In[35]:

my_range[truefalse]


# **Select rows based on a condition**

# In[36]:

#Data where the country name is Canada, Returns True/False
data['Country Name']=='Canada'


# In[38]:

data[data['Country Name']== 'Canada']  # Subset based on condition


# **Select rows based on multiple conditions**

# In[40]:

data[(data['Country Name'] == 'Canada') | (data['Country Code'] == 'JPN')]


# **Why does the following return no hits?**

# In[41]:

data[(data['Country Name'] =='Canada') & (data['Country Code'] =='JPN')]


# **Combining logical statements using &**

# In[42]:

data[(data['Country Name'] =='Canada') & (data['Country Code'] == 'CAN')]


# **Select data by row and column**

# In[43]:

data[['Country Name','Country Code','2010']][16:21]


# ## Data Cleaning

# **Look at the data. What problems do we have with the data quality and how do we solve them ? **

# In[44]:

data.loc[[93,151,174,242]]


# ## Problems with the data quality:
# 
# 1. Some rows are aggregates of countries rather than actual countries (e.g., "World").
# 2. Some columns are irrelevant and can be removed (e.g., "Indicator Name").
# 3. Some years have no data for any country (e.g., 2012 to 2015).
# 4. Some countries have no data for any year. (e.g., "Taiwan, China")
# 

# ###Solution : 
# 1. Some rows are aggregates of countries rather than actual countries (e.g., "World").

# ###Goals:
# **Remove rows that do not contain an actual country. Fortunately, the World Bank provides us with metadata on which rows are countries and which are aggregates.**
# * import countries_metadata.csv
# * merge metadata with data on Country Code

# **Get countries_metadata.csv**

# **Import countries_metadata.csv**

# In[45]:

metadata =pd.read_csv("E:/Data Collection/countries_metadata.csv",encoding = "utf-8")


# In[46]:

metadata.head(10)


# **How do we identify when a listed "Country Name" is a country or an aggregated region?**

# Notice when the row is an aggregate like "Arab World", the Region and IncomeGroup are consistently NaN (Not a Number). We can use this rule to remove all non-country regions.
# 
# **Merge data with metadata on the key, Country Code**

# In[47]:

merge = pd.merge(data,metadata, on = "Country Code")
merge.shape


# In[48]:

merge.head(10)


# **Note: The region values are NaN when the row is not a actual country.**

# ###Remove rows where Region is NaN

# In[49]:

merge = merge[pd.notnull(merge['Region'])]


# In[50]:

merge.head(2)


# ###Solution
# ### 2. Some columns are irrelevant and can be removed.

# ###Goals:
# **Remove the following irrelevant columns:**
# * Column 3: "Indicator Name"
# * Column 4: "Indicator Code"

# In[51]:

merge.columns


# In[52]:

merge = merge.drop(merge.columns[[60,61,64,65]],axis =1) # Note : Zero indexed
merge = merge.drop('Indicator Name', 1)
merge = merge.drop('Indicator Code',1)


# In[53]:

merge.columns


# ##3. Some years have no data for any country.
# 

# **Goals:**
# Count the number of rows for each year. NaN value does not get counted towards the total.

# In[54]:

merge.count()


# **Checking year 2015 because there seems to be no rows containing data.**

# In[55]:

merge['2015']


# ### Remove columns with no row data

# In[56]:

merge = merge.drop(['2012','2013','2014','2015'], 1)


# In[57]:

merge.count()  # double check that columns have been removed


# ## 4. Some countries have no data for any year.

# **Goals:**
# Use row means to determine which countries have no data.
# 
# Let's take the means for each row (on axis 1).

# In[58]:

merge.mean(axis=1) # Takes the mean of all numeric quantities by row


# **Now we can see that, the NaN appears when there is no data for that row.**

# **Remove rows where there are no values in any year**

# In[59]:

merge=merge[pd.notnull(merge.mean(axis=1))]


# In[60]:

merge.head(10)


# ## Data Cleaning ... done!

# ###Assign a new name for convenience

# In[61]:

mydf = merge


# In[62]:

mydf


# **Want to export as csv ?** 

# In[64]:

mydf.to_csv("E:/Data Collection/co2emissions_cleaned.csv",index=False)
#See Recent Data for exported as csv


# ##Data Exploration

# ##Which countries have the highest CO2 emissions per capita in 2011?

# In[65]:

mydf[['Country Name','2011']].sort('2011',ascending=False).head()


# **Qatar?** According to an article by the National Geographic
# [Here](http://on.natgeo.com/1K6Bh0d)
# 

# Why is Qatar highest on the list of consumers? The oil pumped from the desert country's rich sands isn't counted against the country's consumption (unless it's burned in-state), but energy usage is sky-high in this Middle Eastern country. Citizens are provided with free electricity and free water, which the Guardian's Fred Pearce described in a 2010 column as "liquid electricity," since water in the Middle East is often produced by desalinating seawater, an energy-intensive activity. (In this photo, taken in October 2011, window washers return to the ground along the facade of the 52-story Tornado Tower.)
# 
# Energy demand is rising by 7 percent a year to run the desalinators and air conditioners that maintain life in the desert and the natural gas production equipment that funds it.
# http://on.natgeo.com/1K6Bh0d

# ##Which countries have the lowest CO2 emissions per capita in 2011?

# In[66]:

mydf[['Country Name','2011']].sort('2011',ascending = True).head()


# ##Across all countries, how has CO2 emissions per capita changed over the years?

# **Plot the world averages across the years, from 1960 to 2011.**

# **Import matplotlib for plotting**

# In[67]:

import matplotlib.pyplot as plt
get_ipython().magic(u'matplotlib inline')


# **Create the Plot :** 

# In[68]:

#Assign x,y values
world_x = mydf[mydf.columns[2:54]].mean().index
world_y = mydf[mydf.columns[2:54]].mean()

# Plot
plt.plot(world_x,world_y)
plt.title("CO2 Emission per capita averaged accross all countries")
plt.ylabel("Mean CO2 Emission (Metric tons/capita)")
plt.xlabel("Year")


# ##Which regions had the highest CO2 emissions per capita in 2011?

# **What are all the regions?**

# In[69]:

mydf.Region


# **Return only a list of Unique regions :**

# In[70]:

mydf.Region.unique()


# **Group by region and aggregate using the mean function**

# In[71]:

#Groupby then aggregate
by_region = mydf.groupby('Region').agg('mean')
by_region['2011']


# **Check the aggregate values**

# In[72]:

by_region['2011']


# **Plot the Mean CO2 Emission by Region in 2011**

# In[73]:

plt.bar(range(len(by_region['2011'])),by_region['2011'].values)
plt.xticks(range(len(by_region['2011'])), by_region['2011'].index,rotation=70)
plt.ylabel('CO2 Emission (Metrin ton/capita)')
plt.title('Mean CO2 Emission by Region in 2011')


# ##Show the CO2 emissions trend for all countries from 1960 to 2011

# ###What are all the regions?

# In[74]:

mydf.Region


# **Return only a list of unique regions:**

# In[76]:

mydf.Region.unique()


# ###Group by region and aggregate using the mean function

# In[77]:

by_region = mydf.groupby('Region').agg('mean') # groupby then aggregate
by_region['2011']


# ##Show the CO2 emissions trend for all countries from 1960 to 2011

# **Can we create a line graph showing the trend of CO2 emissions across the years for each of the 199 countries?**

# In[78]:

def plot_countries(mydf):
    from pylab import rcParams
    rcParams['figure.figsize'] = (12,6)
    import numpy as np

    colormap = plt.cm.gist_ncar
    plt.gca().set_color_cycle([colormap(i) for i in np.linspace(0, 0.9, len(range(1960,2012)))])


    for i in range(0,len(mydf)):
        plt.plot(mydf.iloc[i,][2:54])
    plt.xticks(range(len(range(1960,2012))),mydf.columns.values[2:54], rotation = 70)
    #plt.legend(mydf["Country Name"].values, loc='upper left')
    plt.legend(mydf["Country Name"].values, ncol=4, loc='upper center', 
               bbox_to_anchor=[0.4, -0.1], 
               columnspacing=1.0, labelspacing=0.0,
               handletextpad=0.0, handlelength=1.0,
               fancybox=True)
    plt.ylabel("CO2 Emission (metric ton/capita)")
    plt.title("CO2 Emission Per Capita by Country and Year")
    plt.show()


# In[79]:

plot_countries(mydf)


# ###Create a search function that returns a subset of the dataframe

# In[80]:

def filter_country(search_term):
    '''
    Filters the medals_df DataFrame to only contain rows whose Sport or Discipline
    columns contain the given search_term.
    '''
    return mydf[mydf["Country Name"].str.contains(search_term, case=False)                      | mydf["Country Code"].str.contains(search_term, case=False)                     | mydf["Region"].str.contains(search_term, case=False)]


# ###Testing the search function, filter_country

# In[81]:

filter_country("Japan")


# ###Plotting the result of the search function

# In[82]:

plot_countries(filter_country("Japan"))


# ##Creating the interactive widget

# In[83]:

# import display to show DataFrame content
from IPython.display import display
# import the widgets interact function to automatically create interactive UI
from IPython.html.widgets import interact

# decorate the search_and_plot_medals function using interact
# to create text field UI for search term
@interact(search='')
def search_and_plot_countries(search):
    '''
    Display medals by country when given a search term.
    '''
    filtered_country = filter_country(search)
    if len(filtered_country) == 0:
        print 'No hits'
        return
    
    # show plot 
    plot_countries(filtered_country)
    # output results
    display(filtered_country)


# In[ ]:



