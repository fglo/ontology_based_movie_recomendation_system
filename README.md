# Ontology Based Movie Recommendation System

Simple Web App serving as a movie recommendation system based on a ontology built in the Protege app:
https://protege.stanford.edu/

## SETUP:
pip install -r backend/requirements.txt

After that you need to fill out needed information in backend/config.py

## RUN:
uvicorn backend.main:app --reload
