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
with open('website_list.txt', 'r', encoding = "utf-8") as website_file:
    websites = [tuple([k.strip() for k in line.split(', ')]) 
    for line in website_file]
    
def RGB_to_hex(RGB_tuple):
    """
    """
    red, green, blue, _ = RGB_tuple
    def clamp(x): 
        return max(0, min(x, 255))

    return "#{0:02x}{1:02x}{2:02x}".format(*[clamp(k) for k in [red, green, blue]])

def create_html_file(DATA_PDFS_DIR, DATA_TXTS_DIR, DOCS_DIR, websites):
    """
    Create a HTML file with information about every PDF file.
    """

    # Create folder for data if it does not exist
    if not os.path.exists(DOCS_DIR):
        os.makedirs(DOCS_DIR)
        
    html = ''
    counter = 1
    for name, url in websites:
        
        log_file = os.path.join(DATA_PDFS_DIR, 'log_{}.txt'.format(name))
        
        # If not log file exists, nothing is downloaded. Skip it
        if not os.path.exists(log_file):
            continue
        
    
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

                time_modified = datetime.datetime.fromtimestamp(os.path.getmtime(local))
                time_change = datetime.datetime.fromtimestamp(os.path.getctime(local))
                time_access = datetime.datetime.fromtimestamp(os.path.getatime(local))
                filesize = round(os.path.getsize(local) / 10**6, 2)
    
                # If the filename is long, shorten it
                if len(filename) > 40:
                    filename_str = filename[:40] + '...'
                else:
                    filename_str = filename
                    
                hex_color = matplotlib.colors.to_hex(matplotlib.cm.Greens(min(0.6, filesize/2)))
                html += '<tr style="background-color:{}">\n'.format(hex_color)
                html += '<td>{}</td>\n'.format(counter)
                html += '<td>{}</td>\n'.format(str(time_modified)[:10])
                html += '<td><a href="{}">{}</a></td>\n'.format(url, filename_str)
                html += '<td>{}</td>\n'.format(name)
                html += '<td>{}</td>\n'.format(filesize)
                html += '<td>Score</td>\n'
                
                base_url = 'http://tommyod.pythonanywhere.com/pdf_collector/'
                #@app.route('/pdf_collector/up/<str:website>/<int:pdf_hash>')
                upvote_url = base_url + 'up/{}/{}'.format(name, abs(hash(filename)))
                downvote_url = base_url + 'down/{}/{}'.format(name, abs(hash(filename)))
                html += '<td><a href="{}">Upvote</a></td>\n'.format(upvote_url)
                html += '<td><a href="{}">Downvote</a></td>\n'.format(downvote_url)
                html += '</tr>\n'
                counter += 1
                
                
    html_skeleton = os.path.join(DOCS_DIR, 'index_skeleton.html')
    html_index = os.path.join(DOCS_DIR, 'index.html')
    
    with open(html_skeleton, 'r') as skeleton:
        text_old = ''.join(l for l in skeleton)
        
        text_new = text_old.replace('TABLE_CONTENT', html)
        
        with open(html_index, 'w') as index:
            index.write(text_new)


if __name__ == '__main__':
    create_html_file(DATA_PDFS_DIR, DATA_TXTS_DIR, DOCS_DIR, websites)
            
