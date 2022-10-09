from bs4 import BeautifulSoup
import requests
import re
import urllib.request
import os

REDDIT_DOMAIN = "https://teddit.net"
REDDIT_URL = "https://teddit.net/r/Newmaxx/"
# REDDIT_URL = "https://news.ycombinator.com/"
# REDDIT_URL = "https://www.teddit.net/r/finance/"



# Blacklist URLs that do not link to good websites
BLACKLIST = ('',)
with open('blacklist.txt', 'r') as blacklist_file:
    BLACKLIST = tuple((x.strip() for x in blacklist_file.readlines()))


def url_filter(urls) -> list[str]:
    """Filter only the urls that may link to an informative website"""
    return list(set((
        url
        for url in urls
        if url
        if not url.startswith('/')
        and not any((
            substr in url
            for substr in BLACKLIST
        ))
    )))


def get_urls(url) -> (list[str], str):
    """Given a URL (to a reddit page), return all external links, and the next page link"""

    # make the request
    r = requests.get(url)
    data = r.text
    soup = BeautifulSoup(data, features="html.parser")

    # get all the urls on the page, then filter them
    urls = url_filter((
        link.get('href')
        for link in soup.find_all('a')
    ))

    # get the url of the next page link (used by the crawler)
    next_page = next(iter((
        link_addr
        for link in soup.find_all('a')
        for link_addr in [link.get('href')]
        if '/hot?t=&after=' in link_addr
    )))

    return urls, REDDIT_DOMAIN+next_page


def scrape(url):
    """Visit a url and return all the text"""
    """This is taken from https://github.com/kjmazidi/NLP"""

   # function to determine if an element is visible
    def visible(element):
        if element.parent.name in ['style', 'script', '[document]', 'head', 'title']:
            return False
        elif re.match('<!--.*-->', str(element.encode('utf-8'))):
            return False
        return True

    try:
        html = urllib.request.urlopen(url)
    except:
        return ''

    soup = BeautifulSoup(html,features="html.parser")
    data = soup.findAll(text=True)
    result = filter(visible, data)
    temp_list = list(result)  # list from filter
    temp_str = ' '.join(temp_list)
    return temp_str


def crawl(starter_url):
    """Generator function that takes a subreddit url and yields text from each linked website
    (including next pages)"""
    url = starter_url
    while True:
        print(f"Taking urls from {url}")
        external_urls, next_page_url = get_urls(url)
        for external_url in external_urls:
            print(f"Scraping from {external_url}")
            scraped_result = scrape(external_url)
            yield external_url, scraped_result
        url = next_page_url


if __name__ == '__main__':

    # create a folder to store the website text
    if not os.path.exists('websites'):
        os.makedirs('websites')

    # create the crawler
    site_generator = crawl(starter_url=REDDIT_URL)

    # crawl to 20 websites
    counter = 1
    while counter < 21:
        url, scraped_result = next(site_generator)

        # write the website text to a file
        if scraped_result:
            with open(f'websites/{counter}.txt', 'w', encoding='utf8') as file:
                file.writelines([url])
                file.write(scraped_result)
                counter += 1

