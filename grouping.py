"""
Pandas grouping tutorial

Requires kaggle avocado dataset

Mapping functions to columns
Converting to datetime
Sort dates to be correct index
Create a column from calculated values
Suppress warnings with df.copy()
Identify unique values of a column to iterate over
multidimensional dataframes & restructuring dataframes (make a new column)
Optimization
Create a graph of regions and another value!
"""

import datetime
import pandas as pd
import os

avocado_data = os.path.join('/home' ,'abc-123','kaggle','avocado.csv')

df = pd.read_csv(avocado_data)

#convert dates to datetime
#maps function to column
df['Date'] = pd.to_datetime(df['Date'])

albany_df = df[df['region']=='Albany']
albany_df.set_index("Date", inplace=True)

#now with correct dates!
albany_df['AveragePrice'].plot()


#average price rolling over 25 values. Roll over mean. Plot
albany_df['AveragePrice'].rolling(25).mean().plot()
#looks ugly -- things are out of order?

print(albany_df.head())

#not in reverse chronological index!
print(albany_df.index)


#need to resort dataframe
albany_df.sort_index(inplace=True)
#looks much better!
#warning - pandas gives lots of warnings
#throw LOTS of warnings
#value is set on a copy of a slice of a dataframe
#for this case -- this warnings is NOT helpful
#lets you know that you FORKED the original dataframe into a new dataframe and modifying values in the copy
#if we move forward without remembering this -- we MAY screw up our analysis
albany_df['AveragePrice'].rolling(25).mean().plot()

#how do we get rid of this warning?
#make a COPY of a dataframe -- new object!
#same basic syntax. copy of df where.....
albany_df = df.copy()[df["region"]=='Albany']

#lets create a new column!
#notice there is no warning
albany_df['price25ma'] = albany_df['AveragePrice'].rolling(25).mean()

#drop the nas (missing data)
albany_df.dropna().head(3)

#how about averages of all regions?
#how do we find the values?
#all values
print(df.values)

#just region
print(df['region'].values)

#convert to list
#too many values!
print(df['region'].values.tolist())

#first convert to set!
set(df['region'].values.tolist())

#then convert to list! (or do it all at once)
#now we can iterate over this list!

#BUT ITS MESSY!
#is there a better way?
list(set(df['region'].values.tolist()))


#YES!
print(df['region'].unique())

#restructuring dataframe -- make regions into columns for graph

#make a dataframe
graph_df = pd.DataFrame()

#iterate and create the two dimensional dataframe
if False:
    for region in df['region'].unique():
        print(region)
        region_df = df.copy()[df['region'] == region]
        region_df.set_index("Date", inplace=True)
        region_df.sort_index(inplace=True)
        region_df['price25ma'] = region_df['AveragePrice'].rolling(25).mean()

        if graph_df.empty:
            #returns a series -- not what we want
            #we want a dataframe!
            #graph_df = region_df["price25ma"]
        #correct way -- returns dataframe
            graph_df = region_df[["price25ma"]]
        else:
            #if two dataframes are indexed the same way -- we can call and it will join on the index
            #see documentation

            #PROBLEM! If we do this THIS WAY we will have one column when we have MANY regions! We need something else
            #THIS WILL THROW AN ERROR!
            graph_df = graph_df.join(region_df["price25ma"])


#this is how we fix it -- there will still be a problem though!
start = datetime.datetime.now()
for region in df['region'].unique()[:16]:
    print(region)
    region_df = df.copy()[df['region'] == region]
    region_df.set_index("Date", inplace=True)
    region_df.sort_index(inplace=True)
    #use string formatting!
    region_df[f'{region}_price25ma'] = region_df['AveragePrice'].rolling(25).mean()
    if graph_df.empty:
        graph_df = region_df[[f'{region}_price25ma']]
    else:
        graph_df = graph_df.join(region_df[f'{region}_price25ma'])
print('TIME TO EXECUTE 16 REGIONS WITH DUPLICATE INDICES:  {}'.format(datetime.datetime.now()-start))
#THIS IS VERY SLOW FOR SOME REASON! IT EXPLODES RAM
#Garbage collection? Too many objects?
#if too slow -- start dropping unneeded columns
#in this dataset we have DUPLICATE DATES because of the non-unique column TYPE
#pandas does not know how to join it. There are many indices that are identical
#pandas gets confused with multiple non-unique indices. This can make things slow!
#here is how to fix it in THIS DATASET:

avocado_data = os.path.join('/home' ,'abc-123','kaggle','avocado.csv')

df = pd.read_csv(avocado_data)
df = df.copy()[df['type']=='organic']
df['Date'] = pd.to_datetime(df['Date'])
#sort a dataframe by a certain value, default ascending is false. Perform operation inplace on dataframe
df.sort_values(by="Date", ascending=True, inplace=True)

#verify
df.head()

#reset the graph_df..... we do NOT reset it in between loops
#this will give a value error for our loop if we do not reset
#ValueError: columns overlap but no suffix specified: Index(['California_price25ma'], dtype='object')
graph_df = pd.DataFrame()


albany_df = df[df['region']=='Albany']
albany_df.set_index("Date", inplace=True)
start = datetime.datetime.now()
for region in df['region'].unique()[:16]:
    print(region)
    region_df = df.copy()[df['region'] == region]
    region_df.set_index("Date", inplace=True)
    region_df.sort_index(inplace=True)
    #use string formatting!
    region_df[f'{region}_price25ma'] = region_df['AveragePrice'].rolling(25).mean()
    if graph_df.empty:
        graph_df = region_df[[f'{region}_price25ma']]
    else:
        graph_df = graph_df.join(region_df[f'{region}_price25ma'])
#much faster
print('TIME TO EXECUTE 16 REGIONS WITH UNIQUE INDICES:  {}'.format(datetime.datetime.now()-start))


graph_df = pd.DataFrame()


albany_df = df[df['region']=='Albany']
albany_df.set_index("Date", inplace=True)
start = datetime.datetime.now()
for region in df['region'].unique():
    print(region)
    region_df = df.copy()[df['region'] == region]
    region_df.set_index("Date", inplace=True)
    region_df.sort_index(inplace=True)
    #use string formatting!
    region_df[f'{region}_price25ma'] = region_df['AveragePrice'].rolling(25).mean()
    if graph_df.empty:
        graph_df = region_df[[f'{region}_price25ma']]
    else:
        graph_df = graph_df.join(region_df[f'{region}_price25ma'])
#much faster
print('TIME TO EXECUTE ALL REGIONS WITH UNIQUE INDICES:  {}'.format(datetime.datetime.now()-start))


#crazy plot! INSANE!
graph_df.plot()

#how do we make this better?
#figsize -- change the size of the graph 8 inches by 5 Inches
#legend - remove the legend
#still have a gap
graph_df.plot(figsize=(8,5), legend=False)

#add dropna method to remove
graph_df.dropna.plot(figsize(8,5), legend=False)

#still looks like shit, but better than it was before :(