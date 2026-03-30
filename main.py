import requests
from bs4 import BeautifulSoup

def get_quotes():
    ### FINAL OUTPUT
    quotes = []

    headers = {'User-Agent': 'Mozilla/5.0'}
    url = 'https://quotes.toscrape.com/search.aspx'

    extracted_keys = []

    # Authors Level
    authors = []
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')
    hidden_inputs = soup.find_all("input", {'type':'hidden'})
    payload = {x["name"]: x["value"] for x in hidden_inputs}
    select_element = soup.find('select', {'id': 'author'})
    if select_element:
        options = select_element.find_all('option')
        for option in options:
            if 'value' not in option.attrs:
                continue

            value =  option.attrs['value']
            authors.append(value)

    for author in authors:
        ### Tag Level
        tags = []

        author_response = requests.post(
            'https://quotes.toscrape.com/filter.aspx',
            headers=headers,
            data={
                **payload,
                'author': author
            }
        )
        soup = BeautifulSoup(author_response.text, 'html.parser')
        tag_hidden_inputs = soup.find_all("input", {'type':'hidden'})
        tag_payload = {x["name"]: x["value"] for x in tag_hidden_inputs}
        select_element = soup.find('select', {'id': 'tag'})
        if select_element:
            options = select_element.find_all('option')
            for option in options:
                if 'value' not in option.attrs:
                    continue

                value =  option.attrs['value']
                tags.append(value)

        for tag in tags:
            combined_key = f'{author}:{tag}'
            if combined_key in extracted_keys:
                continue

            extracted_keys.append(combined_key)

            tag_response = requests.post(
                'https://quotes.toscrape.com/filter.aspx',
                headers=headers,
                data={
                    **tag_payload,
                    'author': author,
                    'tag': tag
                }
            )

            soup = BeautifulSoup(tag_response.text, 'html.parser')
            select_element = soup.select_one('.quote .content')
            quote = select_element.text

            print(author, tag, quote)
            quotes.append({
                'author': author,
                'tag':tag,
                'quote': quote,
            })

    return quotes

if __name__ == '__main__':
    quotes = get_quotes()
    pass