# Final Capstone Project

This repository contains the implementation of the final capstone
project.

## Modules

### Module 1 - Data Pipeline

The data pipeline:

1. Scrapes Books to Scrape.
2. Cleans and transforms the data.
3. Converts GBP prices to INR using the fixed project rate.
4. Stores the data in a normalized SQLite database.
5. Executes SQL queries.
6. Validates SQL results using pandas.

### Module 2 - Analytics

Titanic dataset analysis and machine learning.

### Module 3 - Support Assistant

An offline-capable policy support assistant using retrieval,
embeddings, ChromaDB, LangGraph, FastAPI and deterministic mock mode.

## Repository Structure

```text
final-capstone-project/
│
├── data_pipeline/
│
├── analytics/
│
├── support_assistant/
│
├── README.md
└── .gitignore