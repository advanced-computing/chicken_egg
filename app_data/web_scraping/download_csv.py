# download_csv_module.py
import requests
from io import StringIO
import pandas as pd
from bs4 import BeautifulSoup
from urllib.parse import urljoin

def download_csv(website: str, keyword: str) -> pd.DataFrame:
    """
    Downloads CSV data from a website by finding the first link that contains the specified keyword.
    
    Args:
        website (str): URL of the website to scrape.
        keyword (str): Word to search for in the link text or URL.
    
    Returns:
        pd.DataFrame: DataFrame read from the CSV file.
    
    Raises:
        ValueError: If no link containing the keyword is found.
    """
    # Fetch the webpage content
    response = requests.get(website)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, 'html.parser')
    
    csv_link = None
    # Search for the first anchor tag where the text or href contains the keyword.
    for a in soup.find_all('a', href=True):
        if keyword.lower() in a.text.lower() or keyword.lower() in a['href'].lower():
            csv_link = a['href']
            break
    if not csv_link:
        raise ValueError(f"No link found containing keyword '{keyword}'")
    
    # Convert relative URLs to absolute URLs
    if not csv_link.startswith("http"):
        csv_link = urljoin(website, csv_link)
    
    # Download the CSV file
    csv_response = requests.get(csv_link)
    csv_response.raise_for_status()
    csv_data = StringIO(csv_response.text)
    df = pd.read_csv(csv_data)
    return df

# Testing with bird flu data
website = "https://www.cdc.gov/bird-flu/situation-summary/data-map-commercial.html"
keyword = "csv"  # or another keyword that appears in the CSV link

df = download_csv(website, keyword)
print(df.tail())



