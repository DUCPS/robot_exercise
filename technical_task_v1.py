#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Isaac Brocklesby

09/11/2021

Investigation of robotics data set
"""


###
# ~ Libaries ~ #
###

import numpy as np
import pandas as pd
import matplotlib as plt
import seaborn as sns

###
# ~ Load data ~ #
###

d_fails = pd.read_csv(r"./data_v1/Dispenser_fails.csv")

d_logs = pd.read_csv(r"./data_v1/Dispenser_logs.csv")
 
t_items = pd.read_csv(r"./data_v1/ticket_items_manipulated.csv")

###
# ~ Investigation ~ #
###

### d_logs

# Check for NAs
d_logs.isna().sum()

# Select non NA columns and renamed Unnamed: 0 for convenience
d_logs_small = (d_logs[['Unnamed: 0',
                       'id',
                       'created_at',
                       'updated_at',
                       'log_type',
                       'description',
                       'meta_data']].
                rename(columns={'Unnamed: 0': 'unnamed_0'}))

# Examine variables types
d_logs_small.dtypes

# Count unnamed_0
(d_logs_small
    .groupby('unnamed_0')
    .size()
    .reset_index(name = 'count')
    .sort_values('count', ascending=False))

# Count id
(d_logs_small
    .groupby('id')
    .size()
    .reset_index(name = 'count')
    .sort_values('count', ascending=False))

# Filter for how many created_at are different to updated_at
d_logs_small.query('created_at != updated_at')

# Count log_type
(d_logs_small
    .groupby('log_type')
    .size()
    .reset_index(name = 'count')
    .sort_values('count', ascending=False))

# Count description
d_logs_desc_count = (d_logs_small
    .groupby('description')
    .size()
    .reset_index(name = 'count')
    .sort_values('count', ascending=False))

# Investigate the descriptions
d_logs_desc_count.iloc[0,0]

# Removing moving and dispensing jobs from description
d_logs_small.loc[~d_logs_small.description.str.contains("Dispensing|Moving")]



### t_items

# Check for NAs
t_items.isna().sum()

# Count columns (using loop)
column_names = t_items.columns

for i in column_names:
    print('   ')
    print(i)
    print('----')
    cur_count = (t_items
                 .groupby(i)
                 .size()
                 .reset_index(name = 'count')
                 .sort_values('count', ascending=False))
    print(cur_count)
    print('   ')
    
# Check if started_at is the same as started_move ( note they look the similar but appear like they may have slightly different formats)
t_items.query('started_at != started_move')

# Filter ticket_id_counts for 2 and examine results to identify which the column means
t_items.query('ticket_id_counts == 2')
# Look at ticket_id 098de96b-8dea-459f-a838-dda7211527dd to see if there are only two entries for this id
t_items.query('ticket_id == "098de96b-8dea-459f-a838-dda7211527dd"')
# Look at ticket_id bed0f732-dd83-41f3-9a6d-b51874f2ada2 to see if there are only two entries for this id
t_items.query('ticket_id == "bed0f732-dd83-41f3-9a6d-b51874f2ada2"')
# This test has down ticket_id_counts does not appear to relate to the number of ticket_id's

# Change data and time columns from objects to datatime
dt_columns = ['created_at',
              'updated_at',
              'started_at',
              'started_move',
              'finished_move',
              'started_dispense',
              'finished_dispense']
for i in dt_columns:
    t_items[i] =  pd.to_datetime(t_items[i], format='%Y-%m-%d %H:%M:%S.%f')

###
# ~ Statistics ~ #
###

# How many meals were made per day?  How many overall?

# Per day
t_items['finished_dispense_date'] = t_items['finished_dispense'].dt.date
t_items_per_day = t_items[['finished_dispense_date','ticket_id']].drop_duplicates()
t_items_per_day.groupby('finished_dispense_date').nunique('ticket_id')
"""
2021-09-20                     35
2021-09-21                     37
2021-09-22                     35
2021-09-23                     30
2021-09-24                     16
2021-09-27                     43
"""

# Overall
t_items.ticket_id.nunique()
# 196

# What was the most popular ingredient?

(t_items
 .groupby("ingredient_id")
 .size()
 .reset_index(name = 'count')
 .sort_values('count', ascending=False))

# What was the most popular meal combination?

# It's a shame ingredient_list is missing
# Sort ingredient_id, group by ticket_id, group into tuple, then count for the most common list

meal_combinations = (t_items
 .sort_values('ingredient_id')
 .groupby('ticket_id')['ingredient_id']
 .apply(tuple)
 .reset_index()
 .groupby('ingredient_id')
 .size()
 .reset_index(name = 'count')
 .sort_values('count', ascending=False))
 
meal_combinations.iloc[0,0]
# ('2d7f72ae-7a99-4538-b178-eb280b16ec25',
# '85e5083f-1736-4922-9bf7-1cf7da802d64',
# '87941a51-fd64-4171-95b9-db76bd4465f0',
# 'bfe9f09a-4bfd-4504-a024-8b7cad14407d',
# 'dd565e5e-13a7-4379-9fc8-b9221fae01cf',
# 'e1d855b2-f0b5-45d8-a1f8-a10ba21eed20',
# 'e31c5ea0-00ba-4fb3-9bd6-185237ca1ceb')

# How long did each meal take to make on average?
 
# Assuming the meal starts being "made" when the ticket is created and is finished when the final dispense is done
(t_items
 .groupby('ticket_id')
 .agg({'created_at': 'min', 'finished_dispense': 'max'})
 .reset_index()
 .assign(time_taken = lambda x: x['finished_dispense'] - x['created_at'])['time_taken']
 .mean())

# Is there any relationship between ingredient and meal prep time? What about meal popularity and prep time? 

meal_prep_time = (t_items
 .groupby('ticket_id')
 .agg({'created_at': 'min', 'finished_dispense': 'max'})
 .reset_index()
 .assign(time_taken = lambda x: x['finished_dispense'] - x['created_at'])
 .drop(columns={'created_at','finished_dispense'}))

t_items_prep_time = (t_items
                    .merge(meal_prep_time, how='left')
                    .assign(time_taken_seconds = lambda x: x['time_taken'] / np.timedelta64(1, 's')))

# Ingredient and time taken to make meal

sns.boxplot(y='ingredient_id',
            x='time_taken_seconds',
            data=t_items_prep_time,
            orient='h')

# Meal popularity and time taken to make meal

t_items_meal = (t_items
 .sort_values('ingredient_id')
 .groupby('ticket_id')['ingredient_id']
 .apply(tuple)
 .reset_index())

t_items_meal_pop = (t_items_meal
                    .merge(meal_combinations, how = 'left')
                    .merge(t_items_prep_time[['ticket_id', 'time_taken_seconds']].drop_duplicates(), how = 'left')
                    .rename(columns={'count':'popularity'}))

sns.scatterplot(x = 'time_taken_seconds',
         y = 'popularity',
         data = t_items_meal_pop)


