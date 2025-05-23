CIS6930SP25 -- PROJECT 2
Name: Anshita Rayalla

Assignment Description
This project implements a redaction system that censors sensitive named entities, coreferences, and specified names from PDF documents using Python, spaCy, and PyMuPDF. It supports multiple input files and logs all redacted tokens.

Installing models
bash: 
uv add pip
uv run -m spacy download en_core_web_sm
uv run -m spacy download en_core_web_trf

How to run
bashuv run python:
 ''' main.py --input "resources/*.pdf" --output redacted/ --names Bill --names Carter --entities --coref --stats redacted/stats.tsv '''

Features and functions
main.py

Video link:
https://www.youtube.com/watch?v=T352t90wg1I

Redacts manually specified names (--names)
Redacts named entities using spaCy (--entities)
Attempts coreference resolution via API (--coref)
Outputs redacted PDF documents to the output folder
Logs redacted tokens in stats.tsv

Bugs and Assumptions

The --coref feature uses a REST API hosted on UF internal clusters. It will fail when run outside the UF network.
spaCy model must be installed before using --entities
Only works on PDFs with selectable (non-image) text