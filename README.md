# pdf_collector
Collecting interesting PDFs from websites using machine learning.

## Project overview

- Collect `.pdf` files from arbitrary websites.
- Index the files, allow users to vote on interesting files using a simple API.
- Feed the votes into a machine learning algorithm.
- Feed the machine learning predictions into the indexing.
- Iterate the procedure until "convergence". 

## Project TODO

- **1. Scrape websites**
- [X] Download PDFs
- [X] Store PDFs, text, ID, url
- [X] Allow efficient updating

- **2. Processing and machine learning**
- [X] Preprocess text files
- [ ] Classify some texts manually
- [ ] Create ML model

- **3. Output the results**
- [ ] Pandas -> HTML
- [X] Allow user feedback

