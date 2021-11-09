#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Isaac Brocklesby

09/11/2021

Investigation of robotics data set for Karakuri
"""


###
# ~ Libaries ~ #
###

import numpy as np
import pandas as pd

###
# ~ Load data ~ #
###

d_fails = pd.read_csv(r"/Users/isaacbrocklesby/Documents/karakuri_2021/data_v1/Dispenser_fails.csv")

d_logs = pd.read_csv(r"/Users/isaacbrocklesby/Documents/karakuri_2021/data_v1/Dispenser_logs.csv")
 
t_items = pd.read_csv(r"/Users/isaacbrocklesby/Documents/karakuri_2021/data_v1/ticket_items_manipulated.csv")

###
# ~ Investigation ~ #
###

