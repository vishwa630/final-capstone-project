import sqlite3
import pandas as pd


# ============================================================
# STEP 1: Connect to SQLite database
# ============================================================

database_file = "data_pipeline/data/books.db"

connection = sqlite3.connect(database_file)

print("=" * 60)
print("PANDAS SQL VALIDATION")
print("=" * 60)


# ============================================================
# STEP 2: Read SQL Query 1 using pd.read_sql()
# ============================================================

query1 = """
SELECT title, price_gbp, rating
FROM books
WHERE rating = 5;
"""

df_sql_1 = pd.read_sql(query1, connection)

print("\nSQL QUERY 1 RESULT")
print(df_sql_1.head())

print("\nNumber of rows:", len(df_sql_1))


# ============================================================
# STEP 3: Read SQL Query 2 using pd.read_sql()
# ============================================================

query2 = """
SELECT title, price_gbp
FROM books
ORDER BY price_gbp DESC
LIMIT 10;
"""

df_sql_2 = pd.read_sql(query2, connection)

print("\nSQL QUERY 2 RESULT")
print(df_sql_2)

print("\nNumber of rows:", len(df_sql_2))


# ============================================================
# STEP 4: Read the books table into pandas
# ============================================================

books_df = pd.read_sql(
    "SELECT * FROM books",
    connection
)

print("\nBooks DataFrame:")
print(books_df.head())


# ============================================================
# STEP 5: Read the categories table into pandas
# ============================================================

categories_df = pd.read_sql(
    "SELECT * FROM categories",
    connection
)

print("\nCategories DataFrame:")
print(categories_df.head())


# ============================================================
# STEP 6: Reproduce SQL JOIN using pandas merge
# ============================================================

merged_df = pd.merge(
    books_df,
    categories_df,
    on="category_id",
    how="inner"
)

print("\n" + "=" * 60)
print("PANDAS MERGE RESULT")
print("=" * 60)

print(
    merged_df[
        [
            "title",
            "price_gbp",
            "rating",
            "category_name"
        ]
    ].head(10)
)


# ============================================================
# STEP 7: Create equivalent SQL JOIN result
# ============================================================

sql_join_query = """
SELECT
    books.title,
    books.price_gbp,
    books.rating,
    categories.category_name
FROM books
JOIN categories
    ON books.category_id = categories.category_id
ORDER BY books.title;
"""

sql_join_df = pd.read_sql(
    sql_join_query,
    connection
)


# ============================================================
# STEP 8: Create equivalent pandas result
# ============================================================

pandas_join_df = pd.merge(
    books_df,
    categories_df,
    on="category_id",
    how="inner"
)

pandas_join_df = pandas_join_df[
    [
        "title",
        "price_gbp",
        "rating",
        "category_name"
    ]
].sort_values(
    by="title"
).reset_index(drop=True)


# Reset SQL result index
sql_join_df = sql_join_df.reset_index(drop=True)


# ============================================================
# STEP 9: Compare SQL JOIN and pandas merge
# ============================================================

print("\n" + "=" * 60)
print("JOIN VALIDATION")
print("=" * 60)

print("SQL JOIN rows:", len(sql_join_df))
print("Pandas merge rows:", len(pandas_join_df))


if sql_join_df.equals(pandas_join_df):

    print("\nSUCCESS!")
    print("SQL JOIN and pandas merge produce equivalent results.")

else:

    print("\nWARNING!")
    print("SQL JOIN and pandas merge are not exactly identical.")


# ============================================================
# STEP 10: Save validation results
# ============================================================

sql_join_df.to_csv(
    "data_pipeline/data/sql_join_validation.csv",
    index=False
)

pandas_join_df.to_csv(
    "data_pipeline/data/pandas_merge_validation.csv",
    index=False
)


# ============================================================
# STEP 11: Close database
# ============================================================

connection.close()

print("\nValidation files saved successfully.")

print("\n" + "=" * 60)
print("PANDAS VALIDATION COMPLETED!")
print("=" * 60)