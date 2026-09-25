import sqlite3
import pandas as pd


# ============================================================
# STEP 1: Load cleaned dataset
# ============================================================

input_file = "data_pipeline/data/cleaned_books.csv"

df = pd.read_csv(input_file)

print("=" * 60)
print("CLEANED DATASET LOADED")
print("=" * 60)

print("Rows:", len(df))
print("Columns:", len(df.columns))


# ============================================================
# STEP 2: Connect to SQLite database
# ============================================================

database_file = "data_pipeline/data/books.db"

connection = sqlite3.connect(database_file)

# Enable foreign key support
connection.execute("PRAGMA foreign_keys = ON")

print("\nSQLite database connected successfully!")


# ============================================================
# STEP 3: Create categories table
# ============================================================

connection.execute("""
CREATE TABLE IF NOT EXISTS categories (
    category_id INTEGER PRIMARY KEY AUTOINCREMENT,
    category_name TEXT UNIQUE NOT NULL
)
""")


# ============================================================
# STEP 4: Create books table
# ============================================================

connection.execute("""
CREATE TABLE IF NOT EXISTS books (
    book_id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    price_gbp REAL,
    price_inr REAL,
    rating INTEGER,
    in_stock INTEGER,
    category_id INTEGER,
    FOREIGN KEY (category_id)
        REFERENCES categories(category_id)
)
""")

connection.commit()

print("Database tables created successfully!")


# ============================================================
# STEP 5: Insert categories
# ============================================================

categories = df["category"].drop_duplicates()

for category in categories:

    connection.execute(
        """
        INSERT OR IGNORE INTO categories (category_name)
        VALUES (?)
        """,
        (category,)
    )

connection.commit()

print("Categories inserted successfully!")


# ============================================================
# STEP 6: Insert books
# ============================================================

for _, row in df.iterrows():

    # Find category ID
    category_result = connection.execute(
        """
        SELECT category_id
        FROM categories
        WHERE category_name = ?
        """,
        (row["category"],)
    ).fetchone()

    category_id = category_result[0]

    # Insert book
    connection.execute(
        """
        INSERT INTO books (
            title,
            price_gbp,
            price_inr,
            rating,
            in_stock,
            category_id
        )
        VALUES (?, ?, ?, ?, ?, ?)
        """,
        (
            row["title"],
            row["price_gbp"],
            row["price_inr"],
            row["rating"],
            int(row["in_stock"]),
            category_id
        )
    )

connection.commit()

print("Books inserted successfully!")


# ============================================================
# STEP 7: Verify database
# ============================================================

category_count = connection.execute(
    "SELECT COUNT(*) FROM categories"
).fetchone()[0]

book_count = connection.execute(
    "SELECT COUNT(*) FROM books"
).fetchone()[0]


print("\n" + "=" * 60)
print("DATABASE VERIFICATION")
print("=" * 60)

print("Categories in database:", category_count)
print("Books in database:", book_count)


# ============================================================
# STEP 8: Display sample records
# ============================================================

print("\nFirst 5 books:")

sample = connection.execute(
    """
    SELECT
        book_id,
        title,
        price_gbp,
        price_inr,
        rating,
        in_stock,
        category_id
    FROM books
    LIMIT 5
    """
).fetchall()

for book in sample:
    print(book)


# ============================================================
# STEP 9: Close database
# ============================================================

connection.close()

print("\nDatabase connection closed.")

print("\n" + "=" * 60)
print("DATABASE CREATION COMPLETED SUCCESSFULLY!")
print("=" * 60)