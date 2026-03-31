import pprint
import requests
from bs4 import BeautifulSoup


BASE_URL = "https://quotes.toscrape.com"
SEARCH_URL = f"{BASE_URL}/search.aspx"
FILTER_URL = f"{BASE_URL}/filter.aspx"

HEADERS = {
    "User-Agent": "Mozilla/5.0"
}

def _get_soup(response):
    return BeautifulSoup(response.text, "html.parser")

def _extract_hidden_inputs(soup):
    return {
        el["name"]: el.get("value", "")
        for el in soup.find_all("input", {"type": "hidden"})
        if el.get("name")
    }

def _extract_select_values(soup, select_id):
    select = soup.find("select", {"id": select_id})
    if not select:
        return []
    
    return [
        option.get("value")
        for option in select.find_all("option")
        if option.get("value")
    ]

def get_quotes():
    print("Scraping quotes started...")

    quotes = {}

    # Initial request (authors + payload)
    response = requests.get(SEARCH_URL, headers=HEADERS)
    response.raise_for_status()

    soup = _get_soup(response)
    base_payload = _extract_hidden_inputs(soup)
    authors = _extract_select_values(soup, "author")

    total_authors = len(authors)

    for index, author in enumerate(authors, start=1):
        print(f"[{index}/{total_authors}] Processing author: {author}")

        # Get tags per author
        author_response = requests.post(
            FILTER_URL,
            headers=HEADERS,
            data={**base_payload, "author": author}
        )
        author_response.raise_for_status()

        soup = _get_soup(author_response)
        tag_payload = _extract_hidden_inputs(soup)
        tags = _extract_select_values(soup, "tag")

        for tag in tags:
            # Fetch quote
            tag_response = requests.post(
                FILTER_URL,
                headers=HEADERS,
                data={**tag_payload, "author": author, "tag": tag}
            )
            tag_response.raise_for_status()

            soup = _get_soup(tag_response)
            quote_el = soup.select_one(".quote .content")

            if not quote_el:
                continue

            quote_text = quote_el.get_text(strip=True)[1:-1]

            quote = quotes.setdefault(
                quote_text, 
                {
                    "author": author,
                    "tags": [],
                }
            )
            quote["tags"].append(tag)

    print("Quotes extracted and returned...")

    result = [
        {
            "quote": k,
            **v,
        }
        for k, v in quotes.items()
    ]
    return result

if __name__ == "__main__":
    quotes = get_quotes()
    pprint.pprint(quotes)