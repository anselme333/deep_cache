# Joint Deep Learning and Auction for Congestion-based Caching in Named Data Networking
# Author: Anselme
# Python 3.6.4
########################################################################################################################
# Needed packages
from __future__ import division
from sklearn.preprocessing import MinMaxScaler
from keras.models import Sequential
from keras.layers import Dense
from keras.layers import LSTM
from keras.layers import Dropout
from statsmodels.tsa.arima_model import ARIMA
from fbprophet import Prophet
from matplotlib import cm
from matplotlib.ticker import LinearLocator, FormatStrFormatter
from mpl_toolkits.mplot3d import Axes3D
from sklearn.metrics import mean_squared_error, mean_absolute_error
from mpl_toolkits.mplot3d import axes3d
import matplotlib.pyplot as plt
import numpy as np
import random
import time
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import warnings
warnings.filterwarnings("ignore")
# Starting time
start_time = time.time()
np.random.seed(100)
# Loading the dataset
data_frame = pd.read_csv("training_dataset3.csv")
data_frame.drop(['Unnamed: 0', 'metric', 'queue', 'FaceId'], axis=1, inplace=True)
data_frame0 = data_frame.groupby(['dstNode'])['Packets','Kilobytes'].sum().reset_index()
data_frame = data_frame.groupby('Time').agg({'Node':'first','dstNode':'first', 'bandwidth':'first', 'delay':'first', 'OutInterestName':'first','InInterestName':'first', 'OutDataName':'first', 'InDataName':'first', 'Packets':'sum', 'Kilobytes':'sum'}).reset_index()

dataset_train = data_frame
# We use  the last two columns: Packets and Kilobytes
data_frame0 = data_frame0.sort_values('dstNode', ascending=True).reset_index(drop=True)
data_frame0.to_csv('TrafficGR.csv')
data_frame0.plot(kind='bar', x='dstNode', y='Kilobytes', legend=False)
plt.xticks(fontsize=18)
plt.yticks(fontsize=18)
plt.grid(color='gray')
plt.xlabel('Routers (GRs)', fontsize=18)
plt.ylabel('Total traffic per GR', fontsize=18)
plt.ticklabel_format( style='sci', axis='y', scilimits=(0,0))
plt.show()
print(data_frame.head())
training_set = data_frame.iloc[:, 10:11].values

# Scale the last two column values in range between zero and one.
sc = MinMaxScaler(feature_range=(0, 1))
training_set_scaled = sc.fit_transform(training_set)
print("Size of training dataset", len(training_set_scaled))
X_train = []
y_train = []
for i in range(20, len(training_set_scaled)):
    X_train.append(training_set_scaled[i-20:i, 0])
    y_train.append(training_set_scaled[i, 0])
X_train, y_train = np.array(X_train), np.array(y_train)
X_train = np.reshape(X_train, (X_train.shape[0], X_train.shape[1], 1))

dataset_test = pd.read_csv('testing_dataset3.csv')

dataset_test.drop(['Unnamed: 0', 'metric', 'queue', 'FaceId'], axis=1, inplace=True)
dataset_test = dataset_test.groupby('Time').agg({'Node':'first','dstNode':'first', 'bandwidth':'first', 'delay':'first','OutInterestName':'first','InInterestName':'first', 'OutDataName':'first', 'InDataName':'first', 'Packets':'sum', 'Kilobytes':'sum'}).reset_index()
# dataset_test = dataset_test.groupby(['Time','dstNode'])['Packets','Kilobytes'].sum().reset_index()
print(dataset_test.head())
dataset_test_unmodified = dataset_test
print("Size of testing dataset", len(dataset_test))

real_network_traffic = dataset_test.iloc[:, 10:11].values
dataset_total = pd.concat((dataset_train['Kilobytes'], dataset_test['Kilobytes']), axis=0)
inputs = dataset_total[len(dataset_total) - len(dataset_test) - 20:].values
inputs = inputs.reshape(-1, 1)
inputs = sc.transform(inputs)
##############################
# Using LSTM
model = Sequential()
model.add(LSTM(units=128, return_sequences=True, input_shape=(X_train.shape[1], 1)))
model.add(Dropout(0.2))
model.add(LSTM(units=128, return_sequences=True))
model.add(Dropout(0.2))
model.add(LSTM(units=128, return_sequences=True))
model.add(Dropout(0.2))
model.add(LSTM(units=128, return_sequences=True))
model.add(Dropout(0.2))
model.add(LSTM(units=128))
model.add(Dense(units=1))
model.summary()
model.compile(optimizer='Adam', loss='mean_squared_error', metrics=['acc'])
model.fit(X_train, y_train, epochs=300, batch_size=32)
# Testing  data
X_test = []
for i in range(20, len(dataset_test)):
    X_test.append(inputs[i-20:i, 0])
X_test = np.array(X_test)
X_test = np.reshape(X_test, (X_test.shape[0], X_test.shape[1], 1))
predicted_network_traffic = model.predict(X_test)
predicted_network_traffic = sc.inverse_transform(predicted_network_traffic)
predicted_traffic = predicted_network_traffic

i = 0
future_traffic = []
for x in range(len(predicted_traffic)):
    t = predicted_traffic[x]
    t = np.asarray(t)
    t = t[0]
    t = float("{0:.2f}".format(t))
    future_traffic.append(t)
    #print(t)
print(len(predicted_traffic))
append_size =len(dataset_test_unmodified)-len(future_traffic)
for n in range(append_size):
    future_traffic.insert(0, 0)
#print(future_traffic)
#print(len(future_traffic))

##############################
# Using ARIMA

history = []
for x in range(len(training_set)):
    y = training_set[x]
    y = np.asarray(y)
    y = y[0]
    y = float("{0:.2f}".format(y))
    history.append(y)

predictions_ARIMA = list()
for t in range(len(real_network_traffic)):
    model2 = ARIMA(history, order=(5,1,0))
    model_fit = model2.fit(disp=0)
    output = model_fit.forecast()
    yhat = output[0]
    predictions_ARIMA.append(yhat)
    obs = real_network_traffic[t]
    history.append(obs)
    print('predicted=%f, expected=%f' % (yhat, obs))
error = mean_squared_error(real_network_traffic, predictions_ARIMA)
print('Test MSE: %.3f' % error)
dataset_test_unmodified['PredictedTraffic'] = future_traffic
dataset_test_unmodified.to_csv('network_traffic_prediction.csv')
plt.plot(real_network_traffic, color='blue', linewidth=4.0, label='Network throughput (Ground truth)')
plt.plot(predicted_network_traffic, linewidth=4.0, color='yellowgreen', label='Predicted network throughput (LSTM)')
plt.plot(predictions_ARIMA, linewidth=4.0, color='red', label='Predicted network throughput (ARIMA)')
plt.xticks(fontsize=18)
plt.yticks(fontsize=18)
plt.grid(color='gray')
plt.xlabel('Time', fontsize=18)
plt.ylabel('Throughput', fontsize=18)
plt.ticklabel_format( style='sci', axis='y', scilimits=(0,0))
plt.legend(title='', fontsize=18)
plt.show()

