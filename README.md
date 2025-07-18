# 🏠 Rental Fraud Detection (Work in Progress)

This project aims to detect potentially fraudulent rental listings in Spain, starting with data extracted from Rentalia.com.

The long-term goal is to create a tool that allows users to select a location, date range, number of guests, and rental platform (e.g., Rentalia, Idealista), and detect listings that present anomalous or suspicious patterns.

---

## 🔄 Project Phases

1. **Data Collection (Done ✅)**  
   A Selenium-based scraper for [Rentalia.com](https://www.rentalia.com/) that extracts listings for a specific region, date, and number of guests. Currently hardcoded (e.g., Cádiz, 1 guest), but will support user input via interface in the future.

2. **Data Analysis (In Progress 🔧)**  
   Using both supervised and unsupervised machine learning models to analyze rental listings and detect fraud-like behavior.

   - Supervised models trained on labeled datasets (fraud/not fraud) show high accuracy (~90%).
   - Unsupervised models (e.g., Isolation Forest) currently perform worse (~35–40%), but useful for unknown cases.

3. **Visualization (To Do 📊)**  
   The goal is to present results through dashboards or interactive visuals (Plotly / Streamlit) to easily identify anomalies and patterns.

---

## ⚙️ Requirements

To run the scraper:

- Python 3.8+
- Google Chrome browser
- ChromeDriver installed (must match your Chrome version)
      - You can download ChromeDriver here: https://chromedriver.chromium.org/downloads
- Selenium
- pandas

Install dependencies:

```bash
pip install -r requirements.txt
```

Make sure to update the script (scraper.py) with the correct path to your ChromeDriver. Example:
PATH = "C:\\Tools\\chromedriver\\chromedriver.exe"


