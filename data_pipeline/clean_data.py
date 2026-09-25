import pandas as pd


# ============================================================
# STEP 1: Load the raw dataset
# ============================================================

input_file = "data_pipeline/data/raw_books.csv"

df = pd.read_csv(input_file)

print("=" * 60)
print("RAW DATA LOADED SUCCESSFULLY!")
print("=" * 60)

print("Number of rows:", len(df))
print("Number of columns:", len(df.columns))

print("\nRaw columns:")
print(df.columns.tolist())


# ============================================================
# STEP 2: Clean the price column
# ============================================================

# Remove currency symbols and unwanted characters
df["price_gbp"] = (
    df["price"]
    .astype(str)
    .str.replace("£", "", regex=False)
    .str.replace("Â", "", regex=False)
    .str.strip()
)

# Convert price to numeric
df["price_gbp"] = pd.to_numeric(
    df["price_gbp"],
    errors="coerce"
)


# ============================================================
# STEP 3: Convert star rating to numbers
# ============================================================

rating_map = {
    "One": 1,
    "Two": 2,
    "Three": 3,
    "Four": 4,
    "Five": 5
}

df["rating"] = df["star_rating"].map(rating_map)


# ============================================================
# STEP 4: Convert availability to Boolean
# ============================================================

df["in_stock"] = (
    df["availability"]
    .astype(str)
    .str.strip()
    .str.lower()
    .eq("in stock")
)


# ============================================================
# STEP 5: Convert GBP to INR
# ============================================================

# Fixed project conversion rate
GBP_TO_INR = 105.50

df["price_inr"] = df["price_gbp"] * GBP_TO_INR


# ============================================================
# STEP 6: Check for missing values
# ============================================================

print("\n" + "=" * 60)
print("MISSING VALUES AFTER CONVERSION")
print("=" * 60)

missing_values = df[
    ["price_gbp", "rating", "in_stock", "price_inr"]
].isnull().sum()

print(missing_values)


# ============================================================
# STEP 7: Remove rows with invalid required numeric values
# ============================================================

before = len(df)

df = df.dropna(
    subset=[
        "price_gbp",
        "rating",
        "price_inr"
    ]
)

after = len(df)

print("\n" + "=" * 60)
print("CLEANING RESULTS")
print("=" * 60)

print("Rows before cleaning:", before)
print("Rows after cleaning:", after)
print("Rows removed:", before - after)


# ============================================================
# STEP 8: Select final cleaned columns
# ============================================================

cleaned_df = df[
    [
        "title",
        "price_gbp",
        "price_inr",
        "rating",
        "in_stock",
        "category"
    ]
].copy()


# ============================================================
# STEP 9: Display cleaned data
# ============================================================

print("\n" + "=" * 60)
print("FIRST 5 CLEANED BOOKS")
print("=" * 60)

print(cleaned_df.head())


# ============================================================
# STEP 10: Display data types
# ============================================================

print("\n" + "=" * 60)
print("CLEANED DATA TYPES")
print("=" * 60)

print(cleaned_df.dtypes)


# ============================================================
# STEP 11: Save cleaned dataset
# ============================================================

output_file = "data_pipeline/data/cleaned_books.csv"

cleaned_df.to_csv(
    output_file,
    index=False
)


# ============================================================
# STEP 12: Verify that the file was saved
# ============================================================

print("\n" + "=" * 60)
print("CLEANED DATA SAVING")
print("=" * 60)

print("Cleaned data saved successfully!")
print("File:", output_file)

print("\nFinal number of rows:", len(cleaned_df))
print("Final number of columns:", len(cleaned_df.columns))


# ============================================================
# STEP 13: Final confirmation
# ============================================================

print("\n" + "=" * 60)
print("CLEANING PROCESS COMPLETED SUCCESSFULLY!")
print("=" * 60)