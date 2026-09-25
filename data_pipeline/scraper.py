import requests
from bs4 import BeautifulSoup
import pandas as pd

# Website pages
base_url = "https://books.toscrape.com/catalogue/page-{}.html"

# Store all scraped books
all_books = []

# Scrape first 5 pages
for page in range(1, 6):

    url = base_url.format(page)

    print(f"Scraping page: {page}")

    response = requests.get(url)

    # Check that the website responded successfully
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")

    books = soup.select("article.product_pod")

    # Process each book
    for book in books:

        # Title
        title = book.h3.a["title"]

        # Price
        price = book.select_one(
            ".price_color"
        ).get_text(strip=True)

        # Rating
        rating = book.select_one(
            ".star-rating"
        )["class"][1]

        # Availability
        availability = book.select_one(
            ".availability"
        ).get_text(strip=True)

        # Individual book page
        book_link = book.h3.a["href"]

        book_url = (
            "https://books.toscrape.com/catalogue/"
            + book_link
        )

        # Request individual book page
        book_response = requests.get(book_url)

        book_response.raise_for_status()

        book_soup = BeautifulSoup(
            book_response.text,
            "html.parser"
        )

        # Get category from breadcrumb
        breadcrumb = book_soup.select(
            ".breadcrumb li"
        )

        category = breadcrumb[-2].get_text(
            strip=True
        )

        # Store the book
        all_books.append({
            "title": title,
            "price": price,
            "star_rating": rating,
            "availability": availability,
            "category": category
        })


# Convert to pandas DataFrame
df = pd.DataFrame(all_books)

print()
print("=" * 50)
print("SCRAPING COMPLETED")
print("=" * 50)

print("Total books collected:", len(df))

print(
    "Number of categories:",
    df["category"].nunique()
)

print()
print("Categories:")
print(df["category"].unique())

print()
print("Dataset shape:")
print(df.shape)

print()
print("First 5 books:")
print(df.head())


# Save raw data
df.to_csv(
    "data_pipeline/data/raw_books.csv",
    index=False
)

print()
print("Raw data saved successfully!")