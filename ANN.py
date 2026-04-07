# pip install pandas tensorflow scikit-learn matplotlib

import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder, normalize
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
import matplotlib.pyplot as plt

data = pd.read_csv("your_dataset.csv")

X = data.iloc[:,:-1]
y = LabelEncoder().fit_transform(data.iloc[:,-1])

X_train,X_test,y_train,y_test = train_test_split(X,y,test_size=0.3)

X_train,X_test = normalize(X_train), normalize(X_test)

model = Sequential([
    Dense(10, activation='relu', input_dim=X.shape[1]),
    Dense(len(set(y)), activation='softmax')
])

model.compile(loss='sparse_categorical_crossentropy', optimizer='adam', metrics=['accuracy'])

history = model.fit(X_train,y_train,epochs=20,batch_size=16,verbose=0)

print("Train Acc:", model.evaluate(X_train,y_train,verbose=0)[1])
print("Test Acc:", model.evaluate(X_test,y_test,verbose=0)[1])

plt.plot(history.history['loss']); plt.show()