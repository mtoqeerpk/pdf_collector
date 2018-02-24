#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Download PDF files and save them.

@author: tommy
"""

# Imports
import subprocess
import os
import time

# Constants
DATA_PDFS_DIR = 'data_pdfs'
with open('website_list.txt', 'r', encoding = "utf-8") as website_file:
    websites = [tuple([k.strip() for k in line.split(', ')]) 
    for line in website_file]


def download_from_website(DATA_PDFS_DIR, name, url):
    """
    Download from a single pdf.
    """
    
    # Create a folder for the PDFs if it does not exist
    if not os.path.exists(os.path.join(DATA_PDFS_DIR, name)):
        os.makedirs(os.path.join(DATA_PDFS_DIR, name))
            
    # Setup the download parameters
    start_time = time.perf_counter()
    print('Downloading from "{}"'.format(url))
    log_name = os.path.join(DATA_PDFS_DIR, 'log_{}.txt'.format(name))
    
    # Download using the wget command (UNIX only)
    subprocess.run(["wget", 
                    url, 
                    "--directory-prefix={}".format(os.path.join(DATA_PDFS_DIR, name)),
                    "-nd", 
                    "--accept=pdf", 
                    "-r", 
                    "-t 3", 
                    "-e robots=off", 
                    "-nc",
                    "-nv",
                    "--append-output={}".format(log_name)])
    
    # Print information about download times
    print('Downloading from "{}" DONE'.format(url))
    dl_time = round(time.perf_counter() - start_time, 1)
    print(' -> Downloading took {} seconds'.format(dl_time))


def download_pdfs(DATA_PDFS_DIR, websites):
    """
    Download PDFs from websites.
    """
    # Create folder for data if it does not exist
    if not os.path.exists(DATA_PDFS_DIR):
        os.makedirs(DATA_PDFS_DIR)
    
    # For every website, download all PDFs
    for name, url in websites:
        download_from_website(DATA_PDFS_DIR, name, url)

    
if __name__ == '__main__':
    download_pdfs(DATA_PDFS_DIR, websites)