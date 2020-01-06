import datetime

import numpy as np
import tensorflow as tf
import matplotlib.pyplot as plt
plt.style.use('fivethirtyeight')
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
from keras.models import Sequential
from keras.layers import Dense,LSTM,Dropout,GRU,Bidirectional
import math
from sklearn.metrics import mean_squared_error
import datetime


dataset = pd.read_csv('C:\\shihua.csv',index_col=0)
dataset.head()
train_set = dataset[:'2016'].iloc[:,1:2].values
test_set = dataset['2017':].iloc[:,1:2].values
dataset["High"][:'2016'].plot(figsize=(16,4),legend =True)
dataset["High"][:'2017'].plot(figsize=(16,4),legend =True)
plt.legend(['Training set (Before 2017)','Test set(2017 and beyond)'])
plt.title('pufa stock price')
plt.show()
sc = MinMaxScaler(feature_range=(0,1))
train_set_scalared = sc.fit_transform(train_set)
X_train = []
y_train = []
for i in range(60,710):
    X_train.append(train_set_scalared[i-60:i,0])
    y_train.append(train_set_scalared[i,0])
X_train,y_train = np.array(X_train),np.array(y_train)
X_train = np.reshape(X_train,(X_train.shape[0],X_train.shape[1],1))
regressor = Sequential()
regressor.add(LSTM(units=50,return_sequences=True,input_shape=(X_train.shape[1],1)))
regressor.add(Dropout(0.2))
regressor.add(LSTM(units=50,return_sequences=True))
regressor.add(Dropout(0.2))
regressor.add(LSTM(units=50))
regressor.add(Dropout(0.2))
regressor.add(Dense(units=1))
regressor.compile(optimizer='rmsprop',loss='mean_squared_error')
regressor.fit(X_train,y_train,epochs=50,batch_size=32)
dataset_total = pd.concat((dataset['High'][:'2016'],dataset['High']['2017':]),axis=0)
inputs = dataset_total[len(dataset_total)-len(test_set)-60:].values
inputs =inputs.reshape(-1,1)
inputs = sc.transform(inputs)
X_test = []
for i in range(60,3110):
    X_test.append(inputs[i-60:i,0])
X_test = np.array(X_test)
X_test = np.reshape(X_test,(X_test.shape[0],X_test.shape[1],1))
predicted_stock_price = regressor.predict(X_test)
predicted_stock_price = sc.inverse_transform(predicted_stock_price)
plt.plot(test_set,color='red',label = 'Real ZhongGuoShiHua Price')
plt.plot(predicted_stock_price,color='blue',label = 'Predocted ZhongGuoShiHua Stock price')
plt.title('ZhongGuoShiHua Stock Price Prediction(LSTM')
plt.xlabel('Time')
plt.ylabel('ZhongGuoShiHua Stock Price')
plt.legend()
plt.show()
