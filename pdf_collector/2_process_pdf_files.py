#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Feb 24 10:23:53 2018

@author: tommy
"""

import os
import subprocess

DATA_PDFS_DIR = 'data_pdfs'
DATA_TXTS_DIR = 'data_txts'
with open('website_list.txt', 'r', encoding = "utf-8") as website_file:
    websites = [tuple([k.strip() for k in line.split(', ')]) 
    for line in website_file]

def yield_pdfs(DATA_PDFS_DIR, websites):

    for name, url in websites:
        path_to_pdfs = os.path.join(DATA_PDFS_DIR, name)
        for dirpath, dirnames, filenames in os.walk(path_to_pdfs):
            for filename in filenames:
                # If it's not a PDF, continue
                if not filename[-4:] == '.pdf':
                    continue
                try:
                    print(filename)
                    yield name, filename    
                except:
                    pass
               
def convert_to_txt(DATA_PDFS_DIR, websites):
    # Create folder for data if it does not exist
    if not os.path.exists(DATA_TXTS_DIR):
        os.makedirs(DATA_TXTS_DIR)
        
    for name, url in websites:
        folder_name = os.path.join(DATA_TXTS_DIR, name)
        # Create folder for data if it does not exist
        if not os.path.exists(folder_name):
            os.makedirs(folder_name)
        
    # Convert to text files
    for name, filename in yield_pdfs(DATA_PDFS_DIR, websites):
        filename_pdf = os.path.join(DATA_PDFS_DIR, name, filename)
        filename_txt = os.path.join(DATA_TXTS_DIR, name, filename.replace('.pdf', '.txt'))
        
        subprocess.run(["pdftotext",
                        filename_pdf,
                        filename_txt])
    
if __name__ == '__main__':
    convert_to_txt(DATA_PDFS_DIR, websites)