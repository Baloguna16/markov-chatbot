import os
import requests
from bs4 import BeautifulSoup

LINK = 'https://www.example.com/scrape-me'
SEARCH_TAG = 'p'

def clean_text(text):
    for spaced in ['.', ' ', ',', '!', '?', '(', '—', ')', '|']:
        text = text.replace(spaced, '-')
    return text

def get_text_from_webpage():

    main_sauce = requests.get(LINK)
    main_soup = BeautifulSoup(main_sauce.text, 'html.parser')

    tags = main_soup.find_all(SEARCH_TAG)

    for tag in tags:
        data = None

        # parse & clean data

        dir = 'data'
        filename = f'source_{i}.txt'
        filename = os.path.join(dir, filename)

        with open(filename, 'w+') as f:
            f.write(data)
