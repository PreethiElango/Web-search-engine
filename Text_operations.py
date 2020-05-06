import json
import pickle
from collections import defaultdict 
import operator
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
import json
from sklearn.feature_extraction.text import TfidfVectorizer
import pandas as pd
import pickle
import re
import string
from numpy import argmax

def get_input():
    print("type \"quit\" to close the translation")
    while(True):
        input_sentence = input('English: ')
        if(input_sentence=='quit'):
            break
        k=tfidf_topelements(query_processing("Preethi uic"))
        return k


def stopwords_stemming(tokens):
    ps = PorterStemmer()
    stop_words = set(stopwords.words('english'))
    tokens = [ps.stem(token) for token in tokens if token not in stop_words] 
#     print(tokens) 
    return ' '.join([token for token in tokens if len(token)>1 and token not in stop_words])

def Tokenisation(lines):
    pattern = re.compile('[0-9].*')
    lines = re.sub(pattern,' ',lines)
    translator = str.maketrans(string.punctuation,' '*len(string.punctuation))
    lines = lines.translate(translator)
    tokens = lines.split()
    return tokens
def content_processing():
    f = open('content_new_final (1).json','r') 
    df = json.load(f)
    df = pd.DataFrame(df.items())
    tfidf_vectorizer=TfidfVectorizer(use_idf=True)
    tfidf_documents=tfidf_vectorizer.fit_transform(df[1].apply(stopwords_stemming).values.astype('U'))
    pickle.dump(tfidf_vectorizer, open('tfidf_vectorizer'+'.pk', 'wb'),protocol=pickle.HIGHEST_PROTOCOL)
    pickle.dump(tfidf_documents, open('tfidf_documents'+'.pk', 'wb'),protocol=pickle.HIGHEST_PROTOCOL)
    
def query_processing(query):
    processed_query = stopwords_stemming(Tokenisation(query))
    with open('tfidf_vectorizer'+'.pk', 'rb') as fp:
            tfidf_vectorizer= pickle.load(fp)
    q_tfidf=tfidf_vectorizer.transform([query])
    with open('tfidf_documents'+'.pk', 'rb') as fp:
            doc_tfidf= pickle.load(fp)
    similarity = cosine_similarity(doc_tfidf,q_tfidf)
    return similarity

def tfidf_topelements(similarity):
    f = open('content_new_final (1).json','r') 
    df = json.load(f)
    with open('PageRank.json', 'r') as fp:
         rank= json.load(fp)
    df = pd.DataFrame(df.items())
    flat = similarity.flatten()
    reference=flat
    reference.sort()
    s=[]
    for i in range(1,200):
        s.append(reference[-i])
    index=[]
    for i in s:
        if len(index)<=200:
            k=np.where(similarity==i)
            index.append(df.iloc[k[0][0],0])
            index=set(index)
            index=list(index)
    order=[]
    for i in index:
        k=(i,rank[i])
        order.append(k)
    order = sorted(order, key=operator.itemgetter(1),reverse=True)
    return order