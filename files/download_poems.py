import requests
from bs4 import BeautifulSoup
import os
import os.path
import logging
import random


base_url = 'http://az.lib.ru'
url_pattern = 'http://az.lib.ru/janr/index_janr_2-%d.shtml'
pages = 19

def process_page(s):
    for link in s.select('dl a'):
        href = link['href']
        if href.count('/') == 3:
            logging.info('Downloading %s' % href)
            r = requests.get(base_url + href)
            filename = href[href.rindex('/') + 1:]
            logging.info('Saving to %s' % filename)
            filename = os.path.join('poems', str(random.randint(1, 10000)) + '-' + filename)

            with open(filename, 'w', encoding='utf-8') as f:
                f.write(r.text)


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)

    if not os.path.exists('poems'):
        os.makedirs('poems')

    for page in range(1, pages + 1):
        url = url_pattern % page
        logging.info('Downloading %s' % url)
        r = requests.get(url)
        s = BeautifulSoup(r.text, 'html.parser')
        process_page(s)
