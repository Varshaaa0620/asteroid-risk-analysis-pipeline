# Asteroid Risk Analysis & Automated Executive Reporting Pipeline

## Executive Overview
This project processes NASA CNEOS fireball and close-approach dataset records to compute impact risk indicators, generate high-resolution risk visualizations, and populate an automated executive Excel dashboard with dynamic metrics.

## Key Features & Pipeline Architecture
1. **Data Extraction & Storage:** Ingests raw near-Earth object telemetry directly from a local SQLite database (`nasa_cneos.db`).
2. **Automated Excel Dashboard Automation:** Programmatically injects processed data into `Asteroid_Executive_Risk_Report.xlsx` using Python's `openpyxl` library without overwriting existing formulas.
3. **Dynamic Formula Analytics:** Drives an executive dashboard using formulas including `INDEX/MATCH`, `LARGE`, `COUNTIF`, and `COUNTA`.
4. **Data Visualization:** Produces publication-ready visual charts using Seaborn and Matplotlib (`chart1_risk_distribution.png`, `chart2_miss_distance_by_size.png`, `chart3_velocity_vs_risk.png`).

## Repository Structure
* `etl_pipeline.py` – Reads SQLite data, performs feature engineering (risk scores), and exports clean outputs.
* `generate_excel_report.py` – Automates Excel spreadsheet formatting, layout styling, and dataset sheet refreshes.
* `generate_visualizations.py` – Script for statistical plots and exporting visual charts.
* `Asteroid_Executive_Risk_Report.xlsx` – Executive report workbook with dynamic KPI cards and top-risk threat tables.
* `nasa_cneos.db` / `nasa_cneos_cleaned.csv` – Raw and processed dataset files.

## Tech Stack
* **Language:** Python 3.x
* **Data Processing & Storage:** Pandas, SQLite (`sqlite3`)
* **Visualization:** Matplotlib, Seaborn
* **Reporting:** OpenPyXL, Microsoft Excel (Advanced Formulas)