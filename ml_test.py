import numpy as np
from sklearn.linear_model import LinearRegression

# Fake temperature data
temps = [22, 23, 24, 26, 28, 30, 31]

X = np.array(range(len(temps))).reshape(-1, 1)
y = np.array(temps)

model = LinearRegression()
model.fit(X, y)

# Predict next temperature
next_temp = model.predict([[len(temps)]])
print(f"Next temperature will be: {next_temp[0]:.1f}C")
print("ML is working! ✅")