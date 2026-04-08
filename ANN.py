pip install pandas numpy matplotlib scikit-learn tensorflow keras
import pandas as pd
from keras.models import Sequential
from keras.layers import Dense
from keras.optimizers import Adam
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder, StandardScaler
import matplotlib.pyplot as plt

data = pd.read_csv("heart.csv")

le = LabelEncoder()
data['target'] = le.fit_transform(data['target'])

X = data.drop('target', axis=1)
y = data['target']

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.3, random_state=42
)

scaler = StandardScaler()
X_train = scaler.fit_transform(X_train)
X_test = scaler.transform(X_test)

model = Sequential()
model.add(Dense(16, activation='relu', input_dim=X.shape[1]))
model.add(Dense(8, activation='relu'))
model.add(Dense(1, activation='sigmoid'))

model.compile(
    loss='binary_crossentropy',
    optimizer=Adam(learning_rate=0.01),
    metrics=['accuracy']
)

history = model.fit(
    X_train, y_train,
    epochs=20,
    batch_size=16,
    verbose=1
)

train_acc = model.evaluate(X_train, y_train)[1]
test_acc = model.evaluate(X_test, y_test)[1]

print("Train Accuracy:", train_acc)
print("Test Accuracy:", test_acc)

plt.plot(history.history['loss'])
plt.show()

for layer in model.layers:
    w, b = layer.get_weights()
    print("\nLayer:", layer.name)
    print("Weights:\n", w)
    print("Biases:\n", b)
