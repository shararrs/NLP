from bs4 import BeautifulSoup
import requests
import re
import urllib.request
import os



STARTER_URL = "https://en.wikipedia.org/wiki/Vince_Gilligan"
REDDIT_URL = "https://teddit.net/r/Newmaxx/"


def url_filter(urls) -> list[str]:
    return list(set((
        url
        for url in urls
        if not url.startswith('/')
        and not any((
            substr in url
            for substr in ('.png', '.pdf', '.jpg', 'youtube.com', 'teddit', 'twitter.com', 'reddit.com', 'google.com', 'patreon.com')
        ))
    )))


def get_urls(url):
    r = requests.get(url)

    data = r.text
    soup = BeautifulSoup(data, features="html.parser")

    urls = url_filter((
        link.get('href')
        for link in soup.find_all('a')
    ))

    return urls

def scrape(url):
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

# Press the green button in the gutter to run the script.
if __name__ == '__main__':

    if not os.path.exists('websites'):
        os.makedirs('websites')

    #requester(STARTER_URL)
    urls = get_urls(REDDIT_URL)
    counter = 1
    for url in urls:
        if counter == 21:
            break
        with open(f'websites/{counter}.txt', 'w', encoding='utf8') as file:
            scrape_result = scrape(url)
            if scrape_result:
                file.write(scrape_result)
                counter += 1

