import numpy as np
import matplotlib.pyplot as plt
from tensorflow import keras

plt.style.use('fivethirtyeight')
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense,LSTM,Dropout,GRU,Bidirectional


dataset = pd.read_csv('C:\\Users\\qinxin\\PycharmProjects\\gupiao\\baiduocpc0.csv',index_col=0)
dataset.head()
train_set = dataset[:'2020/5/15'].iloc[:,0:1].values
test_set = dataset['2020/3/16':].iloc[:,0:1].values
dataset["sum"][:'2020/5/15'].plot(figsize=(16,4),legend =True)
dataset["sum"]['2020/3/16':].plot(figsize=(16,4),legend =True)
plt.legend(['train is  2020/5/4 ','test is 2020/5/4 after'])
plt.title('all price')
plt.xlabel('Time')
plt.show()
sc = MinMaxScaler(feature_range=(0,1))
train_set_scalared = sc.fit_transform(train_set)
X_train = []
y_train = []
for i in range(10,50):
    X_train.append(train_set_scalared[i-10:i,0])
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
regressor.fit(X_train,y_train,epochs=10,batch_size=30)


#根据HIGH来预测close
dataset_total = pd.concat((dataset["sum"][:'2020/5/15'],dataset["sum"]['2020/3/16':]),axis=0)

inputs = dataset_total[len(dataset_total)-len(test_set)-10:].values

inputs =inputs.reshape(-1,1)

inputs = sc.transform(inputs)

X_test = []
for i in range(10,73):
    X_test.append(inputs[i-10:i,0])
X_test = np.array(X_test)

print(X_test.shape[0])
print(X_test.shape[1])

X_test = np.reshape(X_test,(X_test.shape[0],X_test.shape[1],1))

predicted_stock_price = regressor.predict(X_test)
predicted_stock_price = sc.inverse_transform(predicted_stock_price)
plt.plot(test_set,color='red',label = 'Real Price')
plt.plot(predicted_stock_price,color='blue',label = 'Predocted  price')
plt.title('Price Prediction(LSTM')
plt.xlabel('Time')
plt.ylabel('Price')
plt.legend()
plt.show()
