import pandas as pd
import string
import re
import glob
import pickle
import time
import requests
import feedparser
from bs4 import BeautifulSoup
from pyvi import ViTokenizer, ViPosTagger
from sqlalchemy import Column, Integer, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

Base = declarative_base()
engine = create_engine('sqlite:///sqlalchemy_article.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
cached_entries = []
news = "https://vnexpress.net/rss/thoi-su.rss"
thegioi = "https://vnexpress.net/rss/the-gioi.rss"
health = "https://vnexpress.net/rss/suc-khoe.rss"
law = "https://vnexpress.net/rss/phap-luat.rss"
edu = "https://vnexpress.net/rss/giao-duc.rss"


class Article(Base):
    __tablename__ = 'article'
    id = Column(Integer, primary_key=True)
    url = Column(Text)
    title = Column(Text)
    desc = Column(Text, nullable=True)
    content = Column(Text)
    raw_content = Column(Text)


def processing_text(text):
    normalized_text = '. '.join([line.strip() for line in text.split('.')])
    tokenized_text, pos_seqs = ViPosTagger.postagging(ViTokenizer.tokenize(normalized_text))
    for i, tag in enumerate(pos_seqs):
        if tag in ['Np', 'Nu', 'M']:
            tokenized_text[i] = tag
    tokens = ' '.join([token for token in tokenized_text
                      if token not in string.punctuation])
    return tokens


def crawl_link(url):
    response = requests.get(url, "html5lib")
    page = BeautifulSoup(response.text)
    try:
        title = page.find('h1').text.strip()
        desc = page.find('h2').text.strip()
        raw_content = page.find('article').text
        raw_content = ". ".join([line.strip() for line in raw_content.split('.')])
        content = processing_text(raw_content)
        article = {'url': url, 'title': title, 'desc': desc, 'content': content, 'raw_content': raw_content}
    except AttributeError:
        article = None
        print("Error")
    return article


def get_new_entry(rss):
    parsed_rss = feedparser.parse(rss)
    rss_entries = parsed_rss['entries']
    new_entry = []
    for entry in rss_entries[::-1]:
        if entry['id'] not in cached_entries:
            cached_entries.insert(0, entry['id'])
            new_entry.append(entry['id'])
            if len(cached_entries) > 500:
                cached_entries.pop()
    return new_entry
mapped = {0: "thoi su", 1: "the gioi", 2: "suc khoe", 3: "luat", 4: "giao duc"}

if __name__ == "__main__":
    while True:
        added_entry = []
        for i, rss in enumerate([news, thegioi, health, law, edu]):
            print("pull data from category {}".format(mapped[i]))
            new_entry = get_new_entry(rss)
            if len(new_entry) > 0:
                for entry in new_entry:
                    article = crawl_link(entry)
                    if article:
                        session = DBSession()
                        if len(session.query(Article).filter(Article.url==article['url']).all()) == 0:
                            print(article['url'])
                            new_article = Article(url=article['url'],
                                                  desc=article['desc'], 
                                                  content=article['content'],
                                                  title=article["title"],
                                                  raw_content=article["raw_content"])
                            added_entry.append(entry)
                            session.add(new_article)
                            session.commit()
        if len(added_entry) > 0:
            requests.post("http://127.0.0.1:5000/update", json={'url': added_entry})
        time.sleep(300)