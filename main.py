import string
import os
import requests
from bs4 import BeautifulSoup


def get_article(url):

    for i in range(1, user_page_count + 1):
        link_page = url + f'&page={i}'
        os.mkdir(f'Page_{i}')

        request = requests.get(link_page)
        if request.status_code > 299:
            return f'The URL returned error code {request.status_code}.'
        soup = BeautifulSoup(request.content, 'html.parser')
        article_links = soup.find_all('a', {'data-track-action': 'view article'})
        article_types = soup.find_all('span', {'class': 'c-meta__type'})
        links_types = [*zip(article_links, article_types)]
        news_articles = [links for links, types in links_types if types.text == user_title]
        articles = [('https://www.nature.com' + link['href']) for link in news_articles]
        titles = []
        for article in articles:
            r = requests.get(article)
            s = BeautifulSoup(r.content, 'html.parser')
            title_soup = s.find('title').text
            for c in string.punctuation:
                title_soup = title_soup.replace(c, '')

            title_soup = title_soup.replace(' ', '_')

            titles.append(title_soup)
            body = s.find('div', {'class': 'c-article-body u-clearfix'})
            file = open(f'Page_{i}/{title_soup}.txt', 'wb')
            file.write(body.text.encode())
            file.close()


user_page_count = int(input())
user_title = input()
get_article('https://www.nature.com/nature/articles?sort=PubDate&year=2020')
