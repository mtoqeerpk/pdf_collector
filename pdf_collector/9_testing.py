#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Feb 24 13:57:57 2018

@author: tommy
"""
import os
import collections
import random
import numpy as np
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.feature_extraction.text import CountVectorizer

def yield_stopwords():
    """
    Yield every stopword from the stopwords-directory.
    """
    for directory, _, filenames in os.walk('stopwords'):
        for filename in filenames:
            with open(os.path.join(directory, filename), 'r') as file:
                for line in file:
                    yield line.strip()

def get_text():

    DATA_PDFS_DIR = 'data_pdfs'
    DATA_TXTS_DIR = 'data_txts'
    with open('website_list.txt', 'r', encoding = "utf-8") as website_file:
        websites = [tuple([k.strip() for k in line.split(', ')]) 
        for line in website_file]
        
    
    for name, url in websites:
        
        log_file = os.path.join(DATA_PDFS_DIR, 'log_{}.txt'.format(name))
    
        data_dict = dict()
        with open(log_file, 'r', encoding = "ISO-8859-1") as log_file:
            for line in log_file:
                if not '.pdf' in line:
                    continue
                try:
                    date = line[:19]
                    url = line[line.index('URL:')+4:line.index('.pdf')+4]
                    local = line[line.index('-> "')+4:line.index('.pdf"')+4]
                except:
                    pass
                _, filename = os.path.split(local)
    
                data_dict[local] = (date, url)
                
                text_file = (local
                             .replace(DATA_PDFS_DIR, DATA_TXTS_DIR)
                             .replace('.pdf', '.txt'))
                
                #print(local, data_dict[local])
                
                with open(text_file, 'r') as text_file:
                    text = ''.join(line for line in text_file)
                
                data_dict[local] = {'date':date, 'url':url, 'text':text}
                
                
        return data_dict
    
    



data = ['bob i am a cat. bob is a cat', 
        'dogs are dogs', 
        'cats and bob']


data = sorted(get_text().items())
random.shuffle(data)
data_text = [v[1]['text'] for v in data][:15]
data_files = [v[0] for v in data][:15]

stop_words = list(yield_stopwords())
count_vect = CountVectorizer(stop_words = stop_words)
stop_words = []
X_train_counts = count_vect.fit_transform(data_text)

for k in collections.Counter(count_vect.vocabulary_).most_common(5):
    print(k)

tf_transformer = TfidfTransformer(use_idf=True).fit(X_train_counts)

num_texts, num_words = X_train_counts.shape

print('Texts: {:,}\t Words: {:,}'.format(num_texts, num_words))

#print(count_vect.vocabulary_)

reverse_vocab = {v:k for (k, v) in count_vect.vocabulary_.items()}



scaled_counts = tf_transformer.transform(X_train_counts)

# Loop gjennom hver tekst
for text in range(num_texts):
    filename = data_files[text]
    print(filename)
        
    # Hent ut topp n ord
    n = 10
    dense = scaled_counts[text, :].todense()
    sorted_arr = dense.argsort()[:, -n:][::-1]
    for k in np.nditer(sorted_arr):
        print(' ',int(k), reverse_vocab[int(k)])











