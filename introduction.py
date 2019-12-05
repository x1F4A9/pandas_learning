"""
Basic pandas dataset manipulation

Requires kaggle avocado dataset

Loads a dataset
Creates a subdataset from a main dataset
Reindex a dataset
"""

#basic data manipulation

import pandas as pd
import os

avocado_data = os.path.join('/home' ,'abc-123','kaggle','avocado.csv')

df = pd.read_csv(avocado_data)

#print first three dataset heads
print(df.head(3))

#print last two dataset tail
print(df.tail(2))

#print average price column
print(df["AveragePrice"].head())

#do not use this format -- it makes the column names appear as methods
print(df.AveragePrice.head())

#dataframe [where the dataframe [region]] == 'Albany'
albany_df = df[df['region'] == 'Albany']
print(albany_df.head())

#worthless with csv files -- columns do not relate to each other
print(albany_df.index)

#need to reindex by something useful, such as date
#the index is dataset dependent
#reset the index
#set index RETURNS a dataframe -- will display the dataframe
#called in place! Returns a new dataframe
albany_df.set_index("Date")


#called in place! Assigns returned dataframe to a new dataframe
albany_df = albany_df.set_index("Date")
#not printed out in standard console -- reassigned

#called in place
albany_df.head()

#modifies the albany dataframe INPLACE
albany_df.set_index("Date", inplace=True)

#in jupyter -- certain options can display the output immediately. Can plot specific columns
albany_df.plot()

#incorrect plot -- other issues
albany_df["AveragePrice"].plot()