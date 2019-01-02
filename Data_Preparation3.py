# Joint Deep Learning and Auction for Congestion-based Caching in Named Data Networking
# Author: Anselme
# Python 3.6.4
########################################################################################################################
# Needed packages
from __future__ import division
from matplotlib import pyplot
import random
import time
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt;

# Starting time
start_time = time.time()
np.random.seed(100)

# Loading the dataset
# To created dataset, we use GEANT2  topology with NDNSIM 2.5
# Loading topology
data_frame_test1 = pd.read_csv("topology.csv")
# print(data_frame1.head(10))
# Loading generated network traffic
data_frame_test2 = pd.read_csv("traffic_dataset_4_test3.csv")
# print(data_frame2.head(10))
# In NDN data are requested by names. However, we know the connection been nodes
# We can updated the traffic dataset based on  connection between nodes.

# Updated data_frame for network traffic
df_test = pd.merge(data_frame_test1, data_frame_test2, on=['Node'])
print(df_test.head(10))
print(df_test.describe())
test_dataset = df_test.to_csv('testing_dataset3.csv')
data_test = df_test.groupby('Time').agg({'Kilobytes':[np.sum]})

#####################################################
# For training

# Loading the dataset
# To created dataset, we use GEANT2  topology with NDNSIM 2.5
# Loading topology
data_frame_train1 = pd.read_csv("topology.csv")
# print(data_frame1.head(10))
# Loading generated network traffic
data_frame_train2 = pd.read_csv("traffic_dataset_4_train3.csv")
# print(data_frame2.head(10))
# In NDN data are requested by names. However, we know the connection been nodes
# We can updated the traffic dataset based on  connection between nodes.

# Updated data_frame for network traffic
df_train = pd.merge(data_frame_train1, data_frame_train2, on=['Node'])
print(df_train.head(10))
print(df_train.describe())
train_dataset = df_train.to_csv('training_dataset3.csv')
data_train = df_train.groupby('Time').agg({'Kilobytes':[np.sum]})
# line plot of dataset
plt.plot(data_test, marker='o', markerfacecolor='coral', markersize=5, color='coral', linewidth=3.0, label="Testing dataset")
plt.plot(data_train, linewidth=3.0, marker='x', markerfacecolor='blue', markersize=7, color='yellowgreen', label="Training dataset")
plt.xticks(fontsize=18)
plt.yticks(fontsize=18)
plt.grid(color='gray')
plt.ticklabel_format( style='sci', axis='y', scilimits=(0,0))
plt.xlabel('Time', fontsize=18)
plt.ylabel('Throughput', fontsize=18)
plt.xlim(0, 164)
plt.legend(title='', fontsize=18)
pyplot.show()


