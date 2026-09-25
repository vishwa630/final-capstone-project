import sqlite3
import pandas as pd


# ============================================================
# STEP 1: Connect to SQLite database
# ============================================================

database_file = "data_pipeline/data/books.db"

connection = sqlite3.connect(database_file)

print("=" * 60)
print("SQL QUERY EXECUTION")
print("=" * 60)


# ============================================================
# QUERY 1
# SELECT + WHERE
# Find books with a rating of 5
# ============================================================

query1 = """
SELECT title, rating
FROM books
WHERE rating = 5;
"""

result1 = pd.read_sql(query1, connection)

print("\nQUERY 1 - SELECT + WHERE")
print(query1)
print(result1.head(10))


# ============================================================
# QUERY 2
# ORDER BY
# Find books ordered by price from highest to lowest
# ============================================================

query2 = """
SELECT title, price_gbp
FROM books
ORDER BY price_gbp DESC;
"""

result2 = pd.read_sql(query2, connection)

print("\nQUERY 2 - ORDER BY")
print(query2)
print(result2.head(10))


# ============================================================
# QUERY 3
# LIMIT
# Display the 10 most expensive books
# ============================================================

query3 = """
SELECT title, price_gbp
FROM books
ORDER BY price_gbp DESC
LIMIT 10;
"""

result3 = pd.read_sql(query3, connection)

print("\nQUERY 3 - LIMIT")
print(query3)
print(result3)


# ============================================================
# QUERY 4
# DISTINCT
# Find all unique book categories
# ============================================================

query4 = """
SELECT DISTINCT category_name
FROM categories
ORDER BY category_name;
"""

result4 = pd.read_sql(query4, connection)

print("\nQUERY 4 - DISTINCT")
print(query4)
print(result4)


# ============================================================
# QUERY 5
# BETWEEN
# Find books with prices between £20 and £30
# ============================================================

query5 = """
SELECT title, price_gbp
FROM books
WHERE price_gbp BETWEEN 20 AND 30
ORDER BY price_gbp;
"""

result5 = pd.read_sql(query5, connection)

print("\nQUERY 5 - BETWEEN")
print(query5)
print(result5)


# ============================================================
# QUERY 6
# JOIN
# Join books and categories
# ============================================================

query6 = """
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

result6 = pd.read_sql(query6, connection)

print("\nQUERY 6 - JOIN")
print(query6)
print(result6.head(10))


# ============================================================
# Save query outputs
# ============================================================

result1.to_csv(
    "data_pipeline/data/query1_output.csv",
    index=False
)

result2.to_csv(
    "data_pipeline/data/query2_output.csv",
    index=False
)

result3.to_csv(
    "data_pipeline/data/query3_output.csv",
    index=False
)

result4.to_csv(
    "data_pipeline/data/query4_output.csv",
    index=False
)

result5.to_csv(
    "data_pipeline/data/query5_output.csv",
    index=False
)

result6.to_csv(
    "data_pipeline/data/query6_join_output.csv",
    index=False
)


# ============================================================
# Close database
# ============================================================

connection.close()

print("\n" + "=" * 60)
print("ALL SQL QUERIES EXECUTED SUCCESSFULLY!")
print("=" * 60)

print("\nQuery output files saved in:")
print("data_pipeline/data/")