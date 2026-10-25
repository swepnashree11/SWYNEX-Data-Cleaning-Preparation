
import pandas as pd

file_path = "data/raw/dirty_cafe_sales.csv"

df = pd.read_csv(file_path)

print("Dataset loaded successfully!")
print("\nFirst 5 rows:")
print(df.head())

print("\nDataset shape:")
print(df.shape)

print("\nColumn names:")
print(df.columns.tolist())

print("\nMissing values in each column:")
print(df.isnull().sum())

print("\nDuplicate rows:")
print(df.duplicated().sum())

print("\nColumn data types:")
print(df.dtypes)


print("\n--- DATA QUALITY CHECK ---")

# Check special or suspicious text values
for col in df.columns:
    if df[col].dtype == "str" or df[col].dtype == "object":
        suspicious = df[col].astype(str).str.strip().str.upper()
        print(f"\n{col} - UNKNOWN values:", (suspicious == "UNKNOWN").sum())
        print(f"{col} - ERROR values:", (suspicious == "ERROR").sum())

# Check numeric columns for unexpected text values
for col in ["Quantity", "Price Per Unit", "Total Spent"]:
    converted = pd.to_numeric(df[col], errors="coerce")
    invalid = df[col].notna() & converted.isna()
    print(f"\n{col} - non-numeric values:", invalid.sum())
    if invalid.sum() > 0:
        print("Examples:", df.loc[invalid, col].unique()[:10])


print("\n--- INVALID VALUE COUNTS ---")

for col in ["Quantity", "Price Per Unit", "Total Spent"]:
    values = df[col].astype(str).str.strip().str.upper()

    print(f"\n{col}:")
    print("ERROR count:", (values == "ERROR").sum())
    print("UNKNOWN count:", (values == "UNKNOWN").sum())
    print("Blank strings:", (values == "").sum())


print("\n--- CONVERT INVALID VALUES ---")

import numpy as np

# Replace invalid text values with missing values
df = df.replace(["ERROR", "UNKNOWN"], np.nan)

# Convert numeric columns to numeric data types
numeric_columns = ["Quantity", "Price Per Unit", "Total Spent"]

for col in numeric_columns:
    df[col] = pd.to_numeric(df[col], errors="coerce")

print("\nUpdated data types:")
print(df[numeric_columns].dtypes)

print("\nMissing values after conversion:")
print(df.isnull().sum())


print("\n--- CATEGORY VALUE CHECK ---")

for col in ["Item", "Payment Method", "Location"]:
    print(f"\n{col} - value counts:")
    print(df[col].value_counts(dropna=False))


print("\n--- DATE VALIDATION ---")

dates = pd.to_datetime(df["Transaction Date"], errors="coerce")

print("Missing or invalid dates:", dates.isna().sum())
print("Earliest valid date:", dates.min())
print("Latest valid date:", dates.max())


print("\n--- NUMERIC VALUE RECOVERY CHECK ---")

# Rows where Total Spent is missing but Quantity and Price Per Unit exist
recover_total = (
    df["Total Spent"].isna()
    & df["Quantity"].notna()
    & df["Price Per Unit"].notna()
)

# Rows where Price Per Unit is missing but Quantity and Total Spent exist
recover_price = (
    df["Price Per Unit"].isna()
    & df["Quantity"].notna()
    & df["Total Spent"].notna()
    & (df["Quantity"] != 0)
)

print("Total Spent recoverable rows:", recover_total.sum())
print("Price Per Unit potentially recoverable rows:", recover_price.sum())



print("\n--- SALES FORMULA VALIDATION ---")

valid_rows = (
    df["Quantity"].notna()
    & df["Price Per Unit"].notna()
    & df["Total Spent"].notna()
)

expected_total = (
    df.loc[valid_rows, "Quantity"]
    * df.loc[valid_rows, "Price Per Unit"]
).round(2)

actual_total = df.loc[valid_rows, "Total Spent"].round(2)

mismatches = (expected_total - actual_total).abs() > 0.02

print("Rows available for validation:", valid_rows.sum())
print("Formula mismatches:", mismatches.sum())
print("Formula match percentage:",
      round((~mismatches).mean() * 100, 2), "%")

print("\n--- MISSING VALUE RECOVERY CHECK ---")

# Total Spent recover panna mudiyura rows
recover_total = (
    df["Total Spent"].isna()
    & df["Quantity"].notna()
    & df["Price Per Unit"].notna()
)

print(
    "Total Spent values that can be recovered:",
    recover_total.sum()
)

# Price Per Unit recover panna mudiyura rows
recover_price = (
    df["Price Per Unit"].isna()
    & df["Quantity"].notna()
    & df["Total Spent"].notna()
    & (df["Quantity"] != 0)
)

print(
    "Price Per Unit values that can be recovered:",
    recover_price.sum()
)

# Quantity recover panna mudiyura rows
recover_quantity = (
    df["Quantity"].isna()
    & df["Price Per Unit"].notna()
    & df["Total Spent"].notna()
    & (df["Price Per Unit"] != 0)
)

print(
    "Quantity values that can be recovered:",
    recover_quantity.sum()
)

print("\n--- RECOVERING NUMERIC VALUES ---")

# Total Spent = Quantity × Price Per Unit
recover_total = (
    df["Total Spent"].isna()
    & df["Quantity"].notna()
    & df["Price Per Unit"].notna()
)

df.loc[recover_total, "Total Spent"] = (
    df.loc[recover_total, "Quantity"]
    * df.loc[recover_total, "Price Per Unit"]
)

# Price Per Unit = Total Spent ÷ Quantity
recover_price = (
    df["Price Per Unit"].isna()
    & df["Quantity"].notna()
    & df["Total Spent"].notna()
    & (df["Quantity"] != 0)
)

df.loc[recover_price, "Price Per Unit"] = (
    df.loc[recover_price, "Total Spent"]
    / df.loc[recover_price, "Quantity"]
)

# Quantity = Total Spent ÷ Price Per Unit
recover_quantity = (
    df["Quantity"].isna()
    & df["Price Per Unit"].notna()
    & df["Total Spent"].notna()
    & (df["Price Per Unit"] != 0)
)

df.loc[recover_quantity, "Quantity"] = (
    df.loc[recover_quantity, "Total Spent"]
    / df.loc[recover_quantity, "Price Per Unit"]
)

print("Numeric recovery completed.")
print("\nRemaining missing numeric values:")
print(df[["Quantity", "Price Per Unit", "Total Spent"]].isna().sum())

print("\n--- CLEANING CATEGORY COLUMNS ---")

category_columns = [
    "Item",
    "Payment Method",
    "Location"
]

for col in category_columns:
    df[col] = df[col].fillna("Unknown")

print("Missing values after category cleaning:")
print(df[category_columns].isna().sum())

print("\nUnknown values in each category:")
for col in category_columns:
    print(f"{col}: {(df[col] == 'Unknown').sum()}")

    print("\n--- CLEANING TRANSACTION DATE ---")

df["Transaction Date"] = pd.to_datetime(
    df["Transaction Date"],
    errors="coerce"
)

print("Date column data type:")
print(df["Transaction Date"].dtype)

print(
    "Missing or invalid dates:",
    df["Transaction Date"].isna().sum()
)

print(
    "Earliest transaction date:",
    df["Transaction Date"].min()
)

print(
    "Latest transaction date:",
    df["Transaction Date"].max()
)

print("\n--- TRANSACTION ID DUPLICATE CHECK ---")

print(
    "Missing Transaction IDs:",
    df["Transaction ID"].isna().sum()
)

print(
    "Duplicate Transaction IDs:",
    df["Transaction ID"].duplicated().sum()
)

print(
    "Unique Transaction IDs:",
    df["Transaction ID"].nunique()
)