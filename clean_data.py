
import pandas as pd
import numpy as np
from pathlib import Path

# Project folder paths
input_file = Path("data/raw/dirty_cafe_sales.csv")
output_file = Path("data/processed/dirty_cafe_sales_cleaned.csv")

# Load original dataset
df = pd.read_csv(input_file)

print("Original dataset shape:", df.shape)

# Clean text values
df = df.replace(r"^\s*$", np.nan, regex=True)

df = df.replace(
    ["ERROR", "UNKNOWN"],
    np.nan
)

# Clean numeric columns
numeric_columns = [
    "Quantity",
    "Price Per Unit",
    "Total Spent"
]

for col in numeric_columns:
    df[col] = pd.to_numeric(df[col], errors="coerce")

# Recover missing numeric values using verified formula
recover_total = (
    df["Total Spent"].isna()
    & df["Quantity"].notna()
    & df["Price Per Unit"].notna()
)

df.loc[recover_total, "Total Spent"] = (
    df.loc[recover_total, "Quantity"]
    * df.loc[recover_total, "Price Per Unit"]
)

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

# Clean category columns
category_columns = [
    "Item",
    "Payment Method",
    "Location"
]

for col in category_columns:
    df[col] = df[col].fillna("Unknown")

# Convert transaction dates
df["Transaction Date"] = pd.to_datetime(
    df["Transaction Date"],
    errors="coerce"
)

# Save cleaned dataset
output_file.parent.mkdir(parents=True, exist_ok=True)
df.to_csv(output_file, index=False)

# Final report
print("\n--- CLEANING SUMMARY ---")
print("Cleaned dataset shape:", df.shape)
print("\nMissing values after cleaning:")
print(df.isna().sum())

print("\nCleaned file saved to:", output_file)

# Verify the saved cleaned dataset
print("\n--- SAVED FILE VERIFICATION ---")

cleaned_df = pd.read_csv(
    output_file,
    parse_dates=["Transaction Date"]
)

print("File exists:", output_file.exists())
print("Shape:", cleaned_df.shape)

print("\nColumn data types:")
print(cleaned_df.dtypes)

print("\nExact duplicate rows:")
print(cleaned_df.duplicated().sum())

print("\nMissing values:")
print(cleaned_df.isna().sum())