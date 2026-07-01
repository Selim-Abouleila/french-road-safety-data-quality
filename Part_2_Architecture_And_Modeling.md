# Part B: Modeling (Gold Layer)

To support efficient road-safety analytics and Business Intelligence (BI) tools, the cleansed Silver layer must be transformed into a **Star Schema** (Fact and Dimension tables) for the Gold layer.

### 1. Fact Table: `Fact_Accidents`
This is the central table containing the measurable, quantitative metrics of each road accident.
* **Grain:** One row per unique accident (`Num_Acc`).
* **Foreign Keys:** `Location_Key`, `Date_Key`.
* **Measures:** `total_fatalities`, `total_hospitalized`, `severity_index` (derived from the Silver layer).
* **Degenerate Dimensions:** `lat`, `long`, `time_of_day`, `lum` (lighting conditions), `agg` (location type).

### 2. Dimension Tables
These tables provide the descriptive context surrounding each accident.
* **`Dim_Location` (Sourced from `lieux_silver`):**
  * Attributes: `catr` (Road category), `circ` (Traffic regime), `vosp` (Reserved lane type), `prof` (Road profile).
* **`Dim_Vehicles` (Sourced from `vehicules_silver`):**
  * Attributes: `id_vehicule`, `catv` (Vehicle category), `obs` (Fixed obstacle hit), `choc` (Initial point of impact).
* **`Dim_Users` (Sourced from `usagers_silver`):**
  * Attributes: `id_usager`, `catu` (User category: driver/pedestrian), `sexe`, `an_nais` (Birth year), `trajet` (Reason for travel), `secu1`/`secu2` (Safety equipment).

---

# Part C: Medallion Architecture Diagram

Below is the complete Medallion Architecture flow showing the progression of data from raw ingestion to the final analytical layer.

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
```

---

# Deliverable 5: Justification of Design Choices

1. **Why Medallion Architecture?** The strict separation prevents corrupt raw data from affecting BI tools. The Silver layer acts as an idempotent, clean foundation, while the Gold layer is purely optimized for fast aggregation (read-heavy operations).
2. **Why a Star Schema in Gold?** The relational raw data (4 tables) requires complex joins. By centralizing the quantitative data into `Fact_Accidents` and pushing descriptive strings to Dimensions, we minimize query latency and avoid massive data duplication for downstream BI platforms like PowerBI or Tableau.
3. **Handling of `-1` (Null Imputation in Silver):** We chose to convert `-1` to `NULL` globally at the Silver layer rather than Gold. This ensures that any data scientist querying the Silver layer directly will not accidentally train a machine learning model where `-1` skews averages or clustering algorithms.
4. **Why a 1:N relationship between Dim_Location and Fact_Accidents?** An N:N relationship implies that a single car crash can occur in multiple completely disparate locations simultaneously, which is physically impossible. Therefore, a specific location can host *many* accidents over time (1 Location → N Accidents), but each accident record in the fact table links to exactly *one* location in the dimension table (1:N), maintaining strict physical and temporal integrity.
