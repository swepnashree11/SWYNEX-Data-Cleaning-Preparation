# SWYNEX Technologies Internship — Task 1
## Data Cleaning and Preparation

### Project Overview
This project focuses on cleaning and preparing a dirty cafe sales dataset using Python and Pandas. The goal is to improve data quality while preserving the original dataset.

### Dataset
- **Dataset name:** Cafe Sales — Dirty Data for Cleaning Training
- **Original file:** `data/raw/dirty_cafe_sales.csv`
- **Original records:** 10,000
- **Columns:** 8

### Tools Used
- Python
- Pandas
- NumPy
- Visual Studio Code

### Data Cleaning Steps
1. Loaded and inspected the original CSV dataset.
2. Identified missing values and placeholder text such as `ERROR` and `UNKNOWN`.
3. Converted `Quantity`, `Price Per Unit`, and `Total Spent` to numeric data types.
4. Recovered missing numeric values where the other values and the verified sales formula were available.
5. Replaced missing values in `Item`, `Payment Method`, and `Location` with `Unknown`.
6. Converted `Transaction Date` to datetime format and invalid dates to missing values.
7. Checked transaction IDs and duplicate rows.
8. Saved the cleaned dataset as a separate CSV file.

### Results
- Original dataset: 10,000 rows and 8 columns.
- Cleaned dataset: 10,000 rows and 8 columns.
- Exact duplicate rows: 0.
- Missing values in category columns after cleaning: 0.
- Remaining missing values:
  - Quantity: 38
  - Price Per Unit: 38
  - Total Spent: 40
  - Transaction Date: 460

### Output File
`data/processed/dirty_cafe_sales_cleaned.csv`

### Note
The original dataset is preserved in `data/raw/`. Values that could not be reliably recovered remain missing instead of being guessed. The cleaned dataset is saved separately for transparency and reproducibility.
