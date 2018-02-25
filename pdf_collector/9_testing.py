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
import string
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
    """
    Iterate through every stored file, return data for machine learning.
    """

    # --------------------------
    # ---------- SETUP ---------
    # --------------------------
    DATA_PDFS_DIR = 'data_pdfs'
    DATA_TXTS_DIR = 'data_txts'
    with open('website_list.txt', 'r', encoding = "utf-8") as website_file:
        websites = [tuple([k.strip() for k in line.split(', ')]) 
        for line in website_file]
        
    ALLOWED_CHARS = set(string.ascii_letters + 'øæåØÆÅ' + ' .,-%&@£+-\\' + r"\\")
    data_dict = dict()
    # --------------------------
    # ---------- MAIN LOOP ---------
    # --------------------------
    for name, url in websites:
        
        log_file = os.path.join(DATA_PDFS_DIR, 'log_{}.txt'.format(name))
        
        try:
            log_file = open(log_file, 'r', encoding = "ISO-8859-1")
        except:
            continue

        for line in log_file:
            if not '.pdf' in line:
                continue
            try:
                date = line[:19]
                url = line[line.index('URL:')+4:line.index('.pdf')+4]
                local = line[line.index('-> "')+4:line.index('.pdf"')+4]
            except:
                continue
            _, filename = os.path.split(local)

            #data_dict[local] = (date, url)
            
            text_file = (local
                         .replace(DATA_PDFS_DIR, DATA_TXTS_DIR)
                         .replace('.pdf', '.txt'))
            
            #print(local, data_dict[local])
            try:
                with open(text_file, 'r') as text_file:
                    text = ''.join(line.replace('\n', ' ') for line in text_file)
                    print('---------------\n', repr(text[:200]))
                    text = ''.join([c for c in text if c in ALLOWED_CHARS])
                    print('---------------\n', repr(text[:200]))
            except:
                continue
                    
            
            data_dict[local] = {'date':date, 'url':url, 'text':text}
        log_file.close()
                
                
    return data_dict

data = sorted(get_text().items())



#%% ----------------

# Prepare the data
data_text = [v[1]['text'] for v in data]
data_files = [v[0] for v in data]

# Retrieve a set of stopwords, count occurences and save as sparse matrix
stop_words = list(yield_stopwords())
count_vect = CountVectorizer(stop_words = stop_words)
X_train_counts = count_vect.fit_transform(data_text)
reverse_vocab = {v:k for (k, v) in count_vect.vocabulary_.items()}

# Transform using term frequency and term frequency inverse document frequen.
# See wikipedia for more information:
# https://en.wikipedia.org/wiki/Tf%E2%80%93idf
tf_transformer = TfidfTransformer(use_idf=True).fit(X_train_counts)
num_texts, num_words = X_train_counts.shape
scaled_counts = tf_transformer.transform(X_train_counts)

print('Texts: {:,}\t Words: {:,}'.format(num_texts, num_words))




#%% ----------------

top_terms = dict()

DATA_TXTS_DIR = 'data_txts'
TOP_TERMS_FILENAME = 'top_terms.txt'
terms_file = open(os.path.join(DATA_TXTS_DIR, TOP_TERMS_FILENAME), 'w')

# Iterate through every single text
for text in range(num_texts):
    print(data[text][0])
    filename = data_files[text]
    #print(filename)
        
    # Hent ut topp n ord
    n = 50
    dense = scaled_counts[text, :].todense()
    sorted_arr = dense.argsort()[:, -n:][::-1]
    for k in np.nditer(sorted_arr):
        break
        #print(' ',int(k), reverse_vocab[int(k)])
        
        
    top_terms[data[text][1]['url']] = [reverse_vocab[int(k)] for 
             k in np.nditer(sorted_arr) if 3 < len(reverse_vocab[int(k)]) < 25]
    
    #print(top_terms)
    
    terms_file.write(', '.join([data[text][1]['url']] +
                               top_terms[data[text][1]['url']]) + '\n')
    
    
terms_file.close()











