import pandas as pd
import numpy as np
import joblib

from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, r2_score

# ============================
# LOAD DATA
# ============================

df = pd.read_csv("bengaluru_house_prices.csv")
print("Original shape:", df.shape)

# ============================
# BASIC CLEANING
# ============================

df = df.dropna(subset=["location", "size", "total_sqft", "bath", "price"])

# Extract BHK
df["bhk"] = df["size"].apply(lambda x: int(x.split()[0]))

# Convert sqft to number
def convert_sqft_to_num(x):
    try:
        if "-" in x:
            a, b = x.split("-")
            return (float(a) + float(b)) / 2
        return float(x)
    except:
        return None

df["total_sqft"] = df["total_sqft"].apply(convert_sqft_to_num)
df = df.dropna(subset=["total_sqft"])

# Remove unrealistic entries
df = df[df["total_sqft"] / df["bhk"] >= 300]

# Price per sqft (used only for outlier removal)
df["price_per_sqft"] = df["price"] * 100000 / df["total_sqft"]

# Remove location outliers
location_stats = df["location"].value_counts()
df["location"] = df["location"].apply(
    lambda x: "other" if location_stats[x] <= 10 else x
)

print("Cleaned data shape:", df.shape)

# ============================
# FEATURE ENGINEERING (FINAL)
# ============================

y = df["price"]

X = df[
    [
        "total_sqft",
        "bath",
        "bhk",
        "location"
    ]
]

# One-hot encode location
X = pd.get_dummies(X, columns=["location"], drop_first=True)

print("Final feature shape:", X.shape)

# ============================
# TRAIN / TEST SPLIT
# ============================

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

print("Train size:", X_train.shape)
print("Test size:", X_test.shape)

# ============================
# MODEL EVALUATION FUNCTION
# ============================

def evaluate_model(name, model):
    model.fit(X_train, y_train)
    preds = model.predict(X_test)

    rmse = np.sqrt(mean_squared_error(y_test, preds))
    r2 = r2_score(y_test, preds)

    print(f"\n{name}")
    print("RMSE:", rmse)
    print("R2:", r2)

    return model, rmse

# ============================
# TRAIN MODELS
# ============================

lr_model, lr_rmse = evaluate_model(
    "Linear Regression",
    LinearRegression()
)

rf_model, rf_rmse = evaluate_model(
    "Random Forest",
    RandomForestRegressor(
        n_estimators=100,
        random_state=42,
        n_jobs=-1
    )
)

# ============================
# MODEL SELECTION
# ============================

best_model = rf_model if rf_rmse < lr_rmse else lr_model
model_name = "RandomForest" if rf_rmse < lr_rmse else "LinearRegression"

print(f"\nBest model selected: {model_name}")

# ============================
# SAVE MODEL + COLUMNS
# ============================

joblib.dump(
    {
        "model": best_model,
        "columns": X.columns.tolist()
    },
    "bangalore_price_model.pkl"
)

print("\nModel saved as bangalore_price_model.pkl")
