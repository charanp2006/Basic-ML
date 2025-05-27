# predict_stock.py

import yfinance as yf
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt

# 1. Download historical stock data
df = yf.download("AAPL", start="2018-01-01", end="2024-12-31")
df = df[['Close']]  # Use only the 'Close' price

# 2. Create features
df['SMA_5'] = df['Close'].rolling(window=5).mean()
df['SMA_10'] = df['Close'].rolling(window=10).mean()
df['Return'] = df['Close'].pct_change()
df['Target'] = df['Close'].shift(-1)  # Predict next day's close

# 3. Drop missing values
df.dropna(inplace=True)

# 4. Prepare training/test sets
features = ['Close', 'SMA_5', 'SMA_10', 'Return']
X = df[features]
y = df['Target']

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, shuffle=False
)

# 5. Train the model
model = RandomForestRegressor(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# 6. Predict
predictions = model.predict(X_test)

# 7. Evaluate
mse = mean_squared_error(y_test, predictions)
print("Mean Squared Error:", mse)

# 8. Plot results
plt.figure(figsize=(14, 6))
plt.plot(y_test.values, label='Actual Prices', linewidth=2)
plt.plot(predictions, label='Predicted Prices', linewidth=2)
plt.title('Stock Price Prediction (Simple ML Model)')
plt.xlabel('Time')
plt.ylabel('Price')
plt.legend()
plt.show()
