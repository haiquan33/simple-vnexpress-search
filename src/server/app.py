import string
import re
import glob
import pickle
import numpy as np
import time
from pyvi import ViTokenizer
from flask import Flask, jsonify, request
from sqlalchemy import Column, Integer, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from update_article import Article, processing_text
from sklearn.neighbors import KDTree
from sklearn.feature_extraction.text import TfidfVectorizer
from scipy.sparse import vstack


app = Flask(__name__)

@app.route("/")
def index():
    return "This is search engine API"

@app.route("/update", methods = ['GET', 'POST'])
def update():
    global indexs
    global embs
    global kdtree
    session = DBSession()
    data = request.json
    links = data['url']
    contents = []
    for link in links:
        article = session.query(Article).filter(Article.url==link).scalar()
        indexs.append(article.id)
        title = processing_text(article.title)
        desc = processing_text(article.desc)
        contents.append("{} {} {}".format(title, desc, article.content))
    session.close()
    new_embs = vectorizer.transform(contents)
    embs = vstack([embs, new_embs])
    assert embs.shape[0] == len(indexs)
    kdtree = KDTree(embs.toarray())
    pickle.dump(kdtree, open("kdtree_{}".format(time.time()), "wb"))
    print("update kdtree")
    return "Updated"


@app.route("/query", methods = ['GET', 'POST'])
def query():
    retreval_articles = []
    session = DBSession()
    data = request.json
    keyword = data['keyword']
    keyword = processing_text(keyword)
    vector = vectorizer.transform([keyword])
    result = kdtree.query(vector[0].toarray(), k=20)[1]
    for id in result[0].squeeze():
        article = session.query(Article).filter(Article.id==indexs[id]).scalar()
        print(article.url)
        desc_text = '. '.join(article.raw_content.split('.')[:3])
        retreval_articles.append((article.url, article.title, desc_text))
    session.close()
    return jsonify(articles=retreval_articles)


def build_kdtree():
    global indexs
    global embs
    contents = []
    session = DBSession()
    for article in session.query(Article).all():
        indexs.append(article.id)
        title = processing_text(article.title)
        desc = processing_text(article.desc)
        contents.append("{} {} {}".format(title, desc, article.content))
    embs = vectorizer.transform(contents)
    assert len(indexs) == embs.shape[0]
    return KDTree(embs.toarray())


if __name__ == "__main__":
    indexs = []
    embs = []
    Base = declarative_base()
    engine = create_engine('sqlite:///sqlalchemy_article.db')
    Base.metadata.bind = engine
    DBSession = sessionmaker(bind=engine)
    vectorizer = pickle.load(open('new_vectorizer', 'rb'))
    kdtree = build_kdtree()
    print("KDTree built!")
    app.run()