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






