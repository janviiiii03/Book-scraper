import csv
import requests
from bs4 import BeautifulSoup
 
# STEP 1: The website we're scraping.
# books.toscrape.com is a fake bookstore built purely for scraping practice.
URL = "http://books.toscrape.com/"
 
 
def get_page_html(url):
    """
    Downloads the raw HTML of a webpage.
    'requests.get()' is like your browser asking the website:
    "hey, send me your page please" — and the website replies with
    the raw HTML text.
    """
    response = requests.get(url)
    response.raise_for_status()  # stops the script if the site didn't respond properly
    return response.text
 
 
def parse_books(html):
    """
    Takes raw HTML and pulls out the book info we care about.
    BeautifulSoup turns messy HTML text into something we can
    search through, like searching a document for specific tags.
    """
    soup = BeautifulSoup(html, "html.parser")
 
    # Every book on the page is wrapped in:
    # <article class="product_pod"> ... </article>
    # We find ALL of them at once.
    book_tags = soup.find_all("article", class_="product_pod")
 
    books = []
    for book in book_tags:
        # The title is stored in the 'title' attribute of the <a> tag
        # inside the <h3> heading.
        title = book.h3.a["title"]
 
        # The price is inside a <p class="price_color">.
        price = book.find("p", class_="price_color").text
 
        # The star rating is stored as a CSS class name, like:
        # <p class="star-rating Three">
        # so we grab the second class name (e.g. "Three").
        rating_classes = book.find("p", class_="star-rating")["class"]
        rating = rating_classes[1] if len(rating_classes) > 1 else "Unknown"
 
        books.append({"title": title, "price": price, "rating": rating})
 
    return books
 
 
def save_to_csv(books, filename="books.csv"):
    """
    Writes our list of book dictionaries into a CSV file,
    which is basically a simple spreadsheet format.
    """
    with open(filename, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["title", "price", "rating"])
        writer.writeheader()
        writer.writerows(books)
 
    print(f"Saved {len(books)} books to {filename}")
 
 
def main():
    print("Fetching page...")
    html = get_page_html(URL)
 
    print("Parsing books...")
    books = parse_books(html)
 
    print("Saving to CSV...")
    save_to_csv(books)
 
    # A little preview so you see it worked
    for book in books[:3]:
        print(book)
 
 
if __name__ == "__main__":
    main()
 
 
