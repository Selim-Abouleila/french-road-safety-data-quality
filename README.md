# French Road Safety Data Quality Analysis

This repository contains a comprehensive data quality assessment, ETL pipeline, and modeling suite for the 2024 French Road Safety (BAAC) dataset.

## ✅ Project Deliverables (Completed)

All required End-of-Day Deliverables for this project have been fully completed and are mapped to the files below:

1. **Data Profiling Report**
   - `data_profiling.ipynb`: Detailed Jupyter notebook with schema extraction, NaN quantification, and consistency checks.
   - `dashboard.py`: Premium Streamlit dashboard summarizing the profiling and data quality impact.
2. **Transformation Plan (Silver Layer)**
   - `Part_2_Transformation_Plan.md`: Written documentation of the standardization, cleaning, deduplication, and enrichment rules.
   - `etl_silver_layer.py`: The executable Python script that applies these transformations and outputs to the `/silver` directory.
3. **Analytical Model (Gold Layer)**
   - `Part_2_Architecture_And_Modeling.md` (Part B): Documentation of the Star Schema design (`Fact_Accidents` + Dimensions).
   - `etl_gold_layer.py`: The executable Python script that builds the Star Schema and outputs `.parquet` files to the `/gold` directory.
4. **Medallion Architecture Diagram**
   - `Part_2_Architecture_And_Modeling.md` (Part C): A complete Mermaid flowchart visually mapping the Bronze ➡️ Silver ➡️ Gold pipeline.
5. **Short Justification of Design Choices**
   - `Part_2_Architecture_And_Modeling.md` (Deliverable 5): Paragraphs explaining the choice of the Medallion architecture, Star Schema, and specific null-handling strategies.

---

## 🏛️ Medallion Architecture

Below is the complete data flow mapping the transformation of raw `.csv` files through the ETL pipeline into our final analytical Star Schema.

```mermaid
flowchart LR
    subgraph Bronze ["Bronze Layer (Raw)"]
        direction TB
        B1[(caract-2024.csv)]
        B2[(lieux-2024.csv)]
        B3[(usagers-2024.csv)]
        B4[(vehicules-2024.csv)]
    end

    subgraph ETL ["Transformations"]
        direction TB
        T1[Format Dates & Coords]
        T2[Deduplicate]
        T3[Standardize Nulls '-1']
    end

    subgraph Silver ["Silver Layer (Cleansed)"]
        direction TB
        S1[(caract_silver)]
        S2[(lieux_silver)]
        S3[(usagers_silver)]
        S4[(vehicules_silver)]
    end

    subgraph Gold ["Gold Layer (Star Schema)"]
        direction TB
        G1{{Fact_Accidents}}
        G2[(Dim_Location)]
        G3[(Dim_Vehicles)]
        G4[(Dim_Users)]
    end
    
    subgraph BI ["BI & Dashboards"]
        direction TB
        D1[Data Quality Dashboard]
        D2[Road Safety Analytics]
    end

    %% Flow logic
    B1 --> T1 --> S1
    B2 --> T2 --> S2
    B3 --> T3 --> S3
    B4 --> T3 --> S4

    S1 -->|Derive KPIs| G1
    S2 -->|Extract Dims| G2
    S3 -->|Extract Dims| G4
    S4 -->|Extract Dims| G3
    
    %% Star Schema Links
    G2 -.->|1:N| G1
    G3 -.->|N:1| G1
    G4 -.->|N:1| G1

    %% To BI
    G1 --> D2
    G2 --> D2
    B1 --> D1

    %% Styling
    classDef bronze fill:#cd7f32,stroke:#333,stroke-width:1px,color:#fff;
    classDef silver fill:#c0c0c0,stroke:#333,stroke-width:1px,color:#000;
    classDef gold fill:#ffd700,stroke:#333,stroke-width:1px,color:#000;
    
    class B1,B2,B3,B4 bronze;
    class S1,S2,S3,S4 silver;
    class G1,G2,G3,G4 gold;

    %% Subgraph Background Colors
    style Bronze fill:#fdf4e3,stroke:#cd7f32,stroke-width:2px,color:#000
    style ETL fill:#f0f9ff,stroke:#38bdf8,stroke-width:2px,color:#000
    style Silver fill:#f3f4f6,stroke:#9ca3af,stroke-width:2px,color:#000
    style Gold fill:#fef9c3,stroke:#eab308,stroke-width:2px,color:#000
    style BI fill:#f0fdf4,stroke:#4ade80,stroke-width:2px,color:#000
```

---

## Project Structure
- **`Part_2_*.md`**: Markdown documents containing the architectural models, transformation plans, and diagrams.
- **`etl_*.py`**: Python ETL scripts for building the Silver and Gold data layers.
- **`silver/` & `gold/`**: Directories containing the processed datasets.
- **`data_profiling.ipynb`**: Core Jupyter Notebook.
- **`dashboard.py`**: Streamlit executive dashboard.

---

## Running the Executive Data Quality Dashboard

The interactive Streamlit dashboard dynamically reads the datasets, computes missingness clusters, identifies pseudo-nulls (e.g., `-1`), and presents an interactive completeness matrix visualization.

### Prerequisites
Make sure you have Python installed along with `pandas` and `streamlit`.
```bash
pip install pandas streamlit
```

### Quickstart
1. Open your terminal (Command Prompt, PowerShell, or bash).
2. Navigate to this project directory:
   ```bash
   cd french-road-safety-data-quality
   ```
3. Run the Streamlit application:
   ```bash
   streamlit run dashboard.py
   ```
4. A new browser tab will automatically open at `http://localhost:8501`.
