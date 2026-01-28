import pandas as pd

# Load dataset
df = pd.read_csv("bengaluru_house_prices.csv")

# Basic inspection
print(df.head())
print(df.shape)
print(df.columns)
# Drop rows with missing essential values
df = df.dropna(subset=["location", "size", "total_sqft", "bath", "price"])

print(df.shape)
# Extract BHK from size column
df["bhk"] = df["size"].apply(lambda x: int(x.split()[0]))

print(df[["size", "bhk"]].head())
def convert_sqft_to_num(x):
    try:
        if "-" in x:
            a, b = x.split("-")
            return (float(a) + float(b)) / 2
        return float(x)
    except:
        return None

df["total_sqft"] = df["total_sqft"].apply(convert_sqft_to_num)

# Drop rows where conversion failed
df = df.dropna(subset=["total_sqft"])

print(df.shape)
df["price_per_sqft"] = df["price"] * 100000 / df["total_sqft"]
df = df[df["total_sqft"] / df["bhk"] >= 300]
location_stats = df["location"].value_counts()

# Mark rare locations as "other"
df["location"] = df["location"].apply(
    lambda x: "other" if location_stats[x] <= 10 else x
)

print(len(df["location"].unique()))
print(df.describe())
