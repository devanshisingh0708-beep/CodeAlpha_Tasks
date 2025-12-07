import requests
from bs4 import BeautifulSoup
import pandas as pd

# Base URL
base_url = "https://books.toscrape.com/catalogue/page-{}.html"

# Lists to store scraped data
titles = []
prices = []
availability_list = []
ratings = []
links = []

# Function to convert rating text to number (optional)
def convert_rating(text):
    ratings_dict = {
        "One": 1,
        "Two": 2,
        "Three": 3,
        "Four": 4,
        "Five": 5
    }
    return ratings_dict.get(text, None)

# Scrape all 50 pages
for page in range(1, 51):  
    print(f"Scraping page {page}...")

    url = base_url.format(page)
    response = requests.get(url)

    soup = BeautifulSoup(response.text, "html.parser")
    books = soup.find_all("article", class_="product_pod")

    for book in books:
        # Title
        title = book.h3.a["title"]
        titles.append(title)

        # Price
        price = book.find("p", class_="price_color").text[1:]  
        try:
            price = price.replace("£", "").strip()
            prices.append(float(price))
        except:
            prices.append(None)


        # Availability
        availability = book.find("p", class_="instock availability").get_text(strip=True)
        availability_list.append(availability)

        # Rating
        rating_class = book.p["class"][1]  
        ratings.append(convert_rating(rating_class))

        # Book link
        link = "https://books.toscrape.com/catalogue/" + book.h3.a["href"]
        links.append(link)

print("Scraping completed successfully!")

# Create DataFrame
df = pd.DataFrame({
    "Title": titles,
    "Price (£)": prices,
    "Availability": availability_list,
    "Rating (1-5)": ratings,
    "Book Link": links
})

# Save as CSV
df.to_csv("books_dataset.csv", index=False)

print("Dataset saved as books_dataset.csv")
df.head()