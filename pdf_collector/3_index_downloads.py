#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Feb 24 10:48:01 2018

@author: tommy
"""

import os
import subprocess
import time
import datetime
import random
import string

DATA_PDFS_DIR = 'data_pdfs'
DATA_TXTS_DIR = 'data_txts'
DOCS_DIR = 'docs'
with open('website_list.txt', 'r', encoding = "utf-8") as website_file:
    websites = [tuple([k.strip() for k in line.split(', ')]) 
    for line in website_file]
    
    
def index_downloads(DATA_PDFS_DIR, DATA_TXTS_DIR, DOCS_DIR, websites):
    pass


if __name__ == '__main__':
    index_downloads(DATA_PDFS_DIR, DATA_TXTS_DIR, DOCS_DIR, websites)

html = ''

# Create folder for data if it does not exist
if not os.path.exists(DOCS_DIR):
    os.makedirs(DOCS_DIR)

counter = 1
for name, url in websites:
    print(name, url)
    
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

            
            info = os.stat(local)
            data_dict[local] = (date, url)
            time_modified = datetime.datetime.fromtimestamp(os.path.getmtime(local))
            time_change = datetime.datetime.fromtimestamp(os.path.getctime(local))
            time_access = datetime.datetime.fromtimestamp(os.path.getatime(local))
            filesize = round(os.path.getsize(local) / 10**6, 2)

            
            if len(filename) > 40:
                filename_str = filename[:40] + '...'
            else:
                filename_str = filename
            html += '<tr>\n'
            html += '<td>{}</td>\n'.format(counter)
            html += '<td>{}</td>\n'.format(str(time_modified)[:10])
            html += '<td><a href="{}">{}</a></td>\n'.format(url, filename_str)
            html += '<td>{}</td>\n'.format(name)
            html += '<td>{}</td>\n'.format(filesize)
            html += '</tr>\n'
            counter += 1

    

            
            
            
html_skeleton = os.path.join(DOCS_DIR, 'index_skeleton.html')
html_index = os.path.join(DOCS_DIR, 'index.html')

with open(html_skeleton, 'r') as skeleton:
    text_old = ''.join(l for l in skeleton)
    
    text_new = text_old.replace('TABLE_CONTENT', html)
    
    with open(html_index, 'w') as index:
        index.write(text_new)
        
  
            
