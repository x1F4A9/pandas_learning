"""
Sentdex python tutorial video 3
groupby data analysis

Does the SAME thing in problem set 2, but with less code
"""

import pandas as pd
import os

#if there is an encoding error, try an option of encoding='latin'
#engine = python also works sometimes
df = pd.read_csv(os.path.join('/home', 'abc-123', 'kaggle', 'Minimum Wage Data.csv'), engine='python')

df.head()

#we want to see some correlation
#how do we get correlations the pandas way?
#grouping etc
#group by!

#creates group by object
gb = df.groupby("State")
gb.get_group("Alabama").set_index("Year").head()

#we can iterate over the groups -- same thing as LAST tutorial but in less code

act_min_wage = pd.DataFrame()

#iterate!
#name -> specific name
#group -> dataframe
for name, group in df.groupby("State"):
    if act_min_wage.empty:
        #rename -> renames columns to what we want
        #renames the column low.2018 to the name of the state -> lets us group by STATE by YEAR
        #columns are states, indices are year, low minimum wage is the column
        act_min_wage = group.set_index("Year")[["Low.2018"]].rename(columns={"Low.2018":name})
    else:
        #same as above but we JOIN before setting the index
        act_min_wage = act_min_wage.join(group.set_index("Year")[["Low.2018"]].rename(columns={"Low.2018":name}))

act_min_wage.head()

#what can we do?
#describe the data -> basic stats
print(act_min_wage.describe())

#correlation & covariance is builtin!
print(act_min_wage.corr().head())

#so many NaNs. How do we know if we screwed up?
#nope not in this case! the data is ... -> not a number


#create id the data
#issue df = a df[where df[low.2018'] == 0
issue_df = df[df['Low.2018']==0]
issue_df.head()

#which states are in the no data!
print(issue_df["State"].unique())

#how do we fix this? numpy isnan & replace
import numpy as np

#replace all 0s with numpy NaN then drop them and if axis=1. Gets rid of columns with axis=1 to get rid of rows, axis=0
#returns dataframe, dont forget to define
min_wage_corr = act_min_wage.replace(0, np.NaN).dropna(axis=1)

act_min_wage.head()

#what if we dont want to drop ALL of it, just the years without min wage
for problem in issue_df['State'].unique():
    if problem in min_wage_corr.columns:
        print("problem")

#group the issues
grouped_issues = issue_df.groupby("State")
grouped_issues.get_group("Alabama").head()

#do we get minwage data EVER?
print(grouped_issues.get_group("Alabama")['Low.2018'].sum())

#NOPE! Alabama never has minimum wage data

for state, data in grouped_issues:
    if data['Low.2018'].sum() != 0.0:
        print('problem')



