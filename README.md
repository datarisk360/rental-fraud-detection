# Rental Fraud Detection (WIP)

This project aims to identify potentially fraudulent rental listings in Spain, based on pricing patterns, location, and other listing metadata.

## Project Phases

1. **Data Collection**
   - A custom scraper for Rentalia.com to extract listing data by date, location, and number of guests.
   - Currently hardcoded to a region in Spain (e.g., Cádiz) and date window.
   - In future iterations, the idea is to develop a user-friendly interface to select platform, region, dates, and guest count.

2. **Data Analysis**
   - Experimentation with supervised models (trained on a labeled dataset of rental listings as fraudulent or not) with promising results (>90% accuracy).
   - Also exploring unsupervised anomaly detection (Isolation Forest, LOF), although current performance is lower (~35–40%).

3. **Visualization (WIP)**
   - Planned dashboard or interactive report to help visualize potential outliers and suspicious listings.
   - Current placeholder includes test plots of pricing distributions and anomaly scores.

## Tech Stack

- Python, pandas, scikit-learn, BeautifulSoup
- Jupyter Notebooks
- Future: Streamlit / Plotly for visualization

## Structure

- `scraper/`: web scraping logic (Rentalia for now)
- `models/`: supervised and unsupervised models, results
- `data/`: small sample of extracted listings
- `notebooks/`: model training and testing
- `visuals/`: graphs and screenshots

## Work in Progress

This is a learning and experimentation project. Future steps:
- Add scraping from other platforms (e.g., Idealista)
- Improve anomaly detection
- Build user-facing interface

---
