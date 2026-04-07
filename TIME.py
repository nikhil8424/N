# pip install pandas numpy matplotlib statsmodels scikit-learn

import pandas as pd, numpy as np, matplotlib.pyplot as plt
from statsmodels.tsa.arima.model import ARIMA
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error

data = pd.read_csv("your_dataset.csv")

date_col = data.columns[0]
value_col = data.columns[1]

data[date_col] = pd.to_datetime(data[date_col], errors='coerce')
data = data.sort_values(date_col).dropna()

y = data[value_col].values
X = np.arange(len(y)).reshape(-1,1)

split = int(len(y)*0.8)
Xtr, Xte = X[:split], X[split:]
ytr, yte = y[:split], y[split:]

lr_pred = LinearRegression().fit(Xtr,ytr).predict(Xte)
rf_pred = RandomForestRegressor().fit(Xtr,ytr).predict(Xte)
arima_pred = ARIMA(ytr, order=(1,1,1)).fit().forecast(len(yte))

print("LR:", mean_squared_error(yte, lr_pred))
print("ML:", mean_squared_error(yte, rf_pred))
print("ARIMA:", mean_squared_error(yte, arima_pred))

plt.plot(yte,label="Actual")
plt.plot(lr_pred,label="LR")
plt.plot(rf_pred,label="ML")
plt.plot(arima_pred,label="ARIMA")
plt.legend(); plt.show()