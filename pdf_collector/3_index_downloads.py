#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Feb 24 10:48:01 2018

@author: tommy
"""

import os
import datetime
import matplotlib


DATA_PDFS_DIR = 'data_pdfs'
DATA_TXTS_DIR = 'data_txts'
DOCS_DIR = '../docs'
with open('website_list.txt', 'r', encoding="utf-8") as website_file:
    websites = [tuple([k.strip() for k in line.split(', ')]) 
                for line in website_file]
    
    
def join_up_to(iterable, len_limit, sep=', '):
    """
    Join an iterable of string, but keep the result to a sensible
    length. Used for joining top keywords in a table.
    """
    result = ''
    i = 0
    while len(result) < len_limit:
        try:
            result += sep + iterable[i]
        except IndexError:
            break
        i += 1
        
    return result.strip(sep)
    
    
def read_top_terms():
    """
    Read top terms for each document from a file.
    """
    DATA_TXTS_DIR = 'data_txts'
    TOP_TERMS_FILENAME = 'top_terms.txt'
    filename = os.path.join(DATA_TXTS_DIR, TOP_TERMS_FILENAME)
    top_terms = dict()
    with open(filename, 'r') as terms_file:
        for line in terms_file:
            url, *terms = line.split(', ')
            
            top_terms[url] = [t.strip() for t in terms]
            
    return top_terms
    

def create_html_file(DATA_PDFS_DIR, DATA_TXTS_DIR, DOCS_DIR, websites):
    """
    Create a HTML file with information about every PDF file.
    """

    # Create folder for data if it does not exist
    if not os.path.exists(DOCS_DIR):
        os.makedirs(DOCS_DIR)
        
    top_terms = read_top_terms()
        
    html = ''
    for name, url in websites:
        
        log_file = os.path.join(DATA_PDFS_DIR, 'log_{}.txt'.format(name))
        
        # If not log file exists, nothing is downloaded. Skip it
        if not os.path.exists(log_file):
            continue
        
        with open(log_file, 'r', encoding="ISO-8859-1") as log_file:
            for line in log_file:
                if '.pdf' not in line:
                    continue
                try:
                    url = line[(line.index('URL:') + 4):
                               (line.index('.pdf') + 4)]
                    local = line[(line.index('-> "') + 4):
                                 (line.index('.pdf"') + 4)]
                except:
                    pass
                _, filename = os.path.split(local)

                from_ts = datetime.datetime.fromtimestamp
                time_modified = from_ts(os.path.getmtime(local))
                #time_change = from_ts(os.path.getctime(local))
                #time_access = from_ts(os.path.getatime(local))
                filesize = round(os.path.getsize(local) / 10**6, 2)
    
                # If the filename is long, shorten it
                if len(filename) > 40:
                    filename_str = filename[:40] + '...'
                else:
                    filename_str = filename
                    
                # Create a row in the table        
                color_rgb = matplotlib.cm.Greens(min(0.6, filesize / 2))
                hex_color = matplotlib.colors.to_hex(color_rgb)
                html += '<tr style="background-color:{}">\n'.format(hex_color)
                html += '<td>{}</td>\n'.format(str(time_modified)[:10])
                html += '<td><a href="{}">{}</a></td>\n'.format(url, filename_str)
                html += '<td>{}</td>\n'.format(name)
                html += '<td>{}</td>\n'.format(filesize)
                html += '<td>Score</td>\n'
                terms = top_terms[url]
                html += '<td>{}</td>\n'.format(join_up_to(terms, 200))
                
                # The voting logic
                u = 'http://tommyod.pythonanywhere.com/pdf_collector/'
                hashed = abs(hash(filename))
                upvote_url = u + 'up/{}/{}'.format(name, hashed)
                downvote_url = u + 'down/{}/{}'.format(name, hashed)
                html += '<td><a href="{}">Up</a> / <a href="{}">Down</a></td>\n'.format(upvote_url, downvote_url)
                html += '</tr>\n'
                
    html_skeleton = os.path.join(DOCS_DIR, 'index_skeleton.html')
    html_index = os.path.join(DOCS_DIR, 'index.html')
    
    with open(html_skeleton, 'r') as skeleton:
        text_old = ''.join(l for l in skeleton)
        
        text_new = text_old.replace('TABLE_CONTENT', html)
        
        with open(html_index, 'w') as index:
            index.write(text_new)


if __name__ == '__main__':
    create_html_file(DATA_PDFS_DIR, DATA_TXTS_DIR, DOCS_DIR, websites)
    