# Transformation Plan (Silver Layer)

This document outlines the required transformations to promote the raw BAAC 2024 datasets from the **Bronze layer** (raw ingestion) to the **Silver layer** (cleaned, standardized, and enriched). These rules are directly informed by the data profiling results (Part 1).

## 1. Standardization
Normalizing formats to ensure consistency across downstream analytical models.

* **Coordinate Standardization (`caract`):** 
  * *Issue:* `lat` and `long` use the European comma notation (`,`) for decimals.
  * *Action:* Replace commas with periods (`.`) and cast the columns from `String/Object` to `Float`.
* **Date & Time Unification (`caract`):** 
  * *Issue:* Temporal data is split across `jour`, `mois`, `an` (integers) and `hrmn` (string/time format).
  * *Action:* Concatenate these fields and cast them into a single, standardized ISO-8601 `timestamp` column named `accident_datetime`.
* **Null Value Normalization (All tables):**
  * *Issue:* The dataset utilizes `-1` as a hidden default to represent "Unknown" (e.g., present in `v1`, `vma`, `secu2`).
  * *Action:* Replace all instances of `-1` across numerical and categorical columns with native `NULL` (SQL) or `np.nan` (Pandas) to prevent statistical distortions.

## 2. Cleaning
Correcting or safely managing invalid and problematic values.

* **High-Missingness Handling:** 
  * *Issue:* Columns like `lartpc`, `occutc`, and `etatp` exceed 90% missingness. 
  * *Action:* Do not drop them entirely, as they are conditionally relevant. Instead, replace `NULL` values with explicitly typed default states (e.g., `"Not Applicable"` for strings, or `0` for specific numeric counts) *only where semantically appropriate*, otherwise leave as `NULL`.
* **String Trimming & Casting:** 
  * *Action:* Apply standard whitespace trimming (`TRIM()`) to text identifiers like `id_usager` and `id_vehicule` to prevent join failures later in the pipeline.

## 3. Enrichment
Adding derived fields to accelerate BI dashboarding and Gold-layer modeling.

* **Temporal Bucketing (`caract`):**
  * *Action:* Derive a new `time_of_day` categorical column from the timestamp:
    * `Morning` (06:00 - 11:59)
    * `Afternoon` (12:00 - 16:59)
    * `Evening` (17:00 - 21:59)
    * `Night` (22:00 - 05:59)
* **Accident Severity Index (`usagers` & `caract`):**
  * *Action:* Roll up the injury severity (`grav`) from the `usagers` table to create an aggregate `max_severity` or `total_fatalities` field at the `Num_Acc` (accident) level. This creates a quick-access KPI for the fact table without needing to join the users table every time.
* **Geospatial Enrichment (`caract`):**
  * *Action:* Extract or map the Department code (`dep`) to standard French region names to facilitate high-level geographic grouping in dashboards.

## 4. Deduplication
Removing duplicated records to maintain referential integrity.

* **Locations Table (`lieux`):**
  * *Issue:* Data profiling identified exactly 2 duplicate records in the `lieux-2024.csv` table.
  * *Action:* Apply a strict `DROP DUPLICATES` (or `SELECT DISTINCT`) operation on the primary key (`Num_Acc`) during the Bronze-to-Silver transition.
* **Global Safety Net:**
  * *Action:* Apply a general deduplication rule across all incoming Bronze tables to ensure idempotency in the ETL pipeline.

## 5. Documentation of Flow
The pipeline will execute in the following sequence for each batch:
1. **Ingest** Bronze CSVs.
2. **Apply Deduplication** to remove any exact row copies.
3. **Standardize** strings, coordinates, and convert `-1` to `NULL`.
4. **Enrich** dates into timestamps and calculate derived severity metrics.
5. **Write** to the Silver Layer (e.g., as Parquet or Delta tables) enforcing strict schema validation.
