import numpy as np
from sklearn.linear_model import LinearRegression
import joblib

# Dummy training data
X = np.array([[500], [800], [1000], [1200], [1500]])
y = np.array([50, 80, 100, 120, 150])  # price in lakhs

model = LinearRegression()
model.fit(X, y)

joblib.dump(model, "model.joblib")
print("Model trained and saved.")
