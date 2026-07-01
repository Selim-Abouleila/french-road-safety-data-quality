# French Road Safety Data Quality Analysis

This repository contains a comprehensive data quality assessment and profiling suite for the 2024 French Road Safety (BAAC) dataset.

## Project Structure
- **`data_profiling.ipynb`**: A step-by-step Jupyter Notebook detailing dataset structure, missingness calculations, consistency checks, and anomaly detection.
- **`dashboard.py`**: A premium, executive-level interactive Streamlit dashboard summarizing structural fragmentation, ETL risks, and downstream analytical impact.
- **`analyze_*.py`**: Python helper scripts used for automated data extraction and anomaly detection across tables.
- **Datasets**: The original 4 core CSV datasets (`caract-2024.csv`, `lieux-2024.csv`, `usagers-2024.csv`, `vehicules-2024.csv`).

---

## Running the Executive Dashboard

The interactive Streamlit dashboard dynamically reads the datasets, computes missingness clusters, identifies pseudo-nulls (e.g. `-1`), and presents an interactive completeness matrix visualization.

### Prerequisites
Make sure you have Python installed along with `pandas` and `streamlit`.
```bash
pip install pandas streamlit
```

### Quickstart
1. Open your terminal (Command Prompt, PowerShell, or bash).
2. Clone this repository or navigate to the project directory:
   ```bash
   cd french-road-safety-data-quality
   ```
3. Run the Streamlit application:
   ```bash
   streamlit run dashboard.py
   ```
4. A new browser tab will automatically open at `http://localhost:8501`.
