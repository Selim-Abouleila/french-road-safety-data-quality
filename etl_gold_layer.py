import pandas as pd
import os
import sys

# Fix Windows console encoding
sys.stdout.reconfigure(encoding='utf-8')

print("🌟 Starting Silver to Gold ETL Pipeline (Star Schema)...")

# Create Gold directory
os.makedirs('gold', exist_ok=True)

# 1. Load Silver Datasets
print("📥 Loading Cleansed Silver Datasets...")
caract = pd.read_csv('silver/caract_silver.csv', low_memory=False)
lieux = pd.read_csv('silver/lieux_silver.csv', low_memory=False)
usagers = pd.read_csv('silver/usagers_silver.csv', low_memory=False)
vehicules = pd.read_csv('silver/vehicules_silver.csv', low_memory=False)

# 2. Build Fact Table: Fact_Accidents
print("🏗️ Building Fact_Accidents...")
# Grain: 1 row per Num_Acc
fact_cols = [
    'Num_Acc', 'accident_datetime', 'lat', 'long', 
    'time_of_day', 'lum', 'agg', 
    'total_fatalities', 'total_hospitalized', 'severity_index'
]
# Select only available columns to prevent KeyError
available_fact_cols = [col for col in fact_cols if col in caract.columns]
fact_accidents = caract[available_fact_cols].copy()

# 3. Build Dimension Tables
print("📐 Building Dimensions...")

# Dim_Location
dim_loc_cols = ['Num_Acc', 'catr', 'circ', 'vosp', 'prof']
available_loc_cols = [col for col in dim_loc_cols if col in lieux.columns]
dim_location = lieux[available_loc_cols].copy()

# Dim_Vehicles
dim_veh_cols = ['id_vehicule', 'Num_Acc', 'catv', 'obs', 'choc']
available_veh_cols = [col for col in dim_veh_cols if col in vehicules.columns]
dim_vehicles = vehicules[available_veh_cols].copy()

# Dim_Users
dim_usr_cols = ['id_usager', 'id_vehicule', 'Num_Acc', 'catu', 'sexe', 'an_nais', 'trajet', 'secu1', 'secu2']
available_usr_cols = [col for col in dim_usr_cols if col in usagers.columns]
dim_users = usagers[available_usr_cols].copy()

# 4. Save to Gold Layer
print("💾 Writing to Gold Layer (Parquet format for Analytics)...")
# Parquet is the industry standard for Gold layer analytics (highly compressed, columnar)
fact_accidents.to_parquet('gold/Fact_Accidents.parquet', index=False)
dim_location.to_parquet('gold/Dim_Location.parquet', index=False)
dim_vehicles.to_parquet('gold/Dim_Vehicles.parquet', index=False)
dim_users.to_parquet('gold/Dim_Users.parquet', index=False)

print("✅ Gold ETL Pipeline completed successfully! Star Schema is ready in the '/gold' folder.")
