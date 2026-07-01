import pandas as pd
import numpy as np
import os
import sys

# Fix Windows console emoji encoding
sys.stdout.reconfigure(encoding='utf-8')

print("🚀 Starting Bronze to Silver ETL Pipeline...")

# Create Silver directory
os.makedirs('silver', exist_ok=True)

# 1. Ingest Bronze Data
print("📥 Loading Bronze Datasets...")
caract = pd.read_csv('caract-2024.csv', sep=';', low_memory=False)
lieux = pd.read_csv('lieux-2024.csv', sep=';', low_memory=False)
usagers = pd.read_csv('usagers-2024.csv', sep=';', low_memory=False)
vehicules = pd.read_csv('vehicules-2024.csv', sep=';', low_memory=False)

datasets = {'caract': caract, 'lieux': lieux, 'usagers': usagers, 'vehicules': vehicules}

# 2. Deduplication
print("🧹 Removing duplicates...")
for name, df in datasets.items():
    initial_len = len(df)
    df.drop_duplicates(inplace=True)
    dropped = initial_len - len(df)
    if dropped > 0:
        print(f"   -> Dropped {dropped} exact duplicates from {name}")

# 3. Null Value Normalization (-1 to NaN)
print("🔍 Standardizing hidden defaults (-1 -> NaN)...")
for name, df in datasets.items():
    for col in df.columns:
        if df[col].dtype in ['int64', 'float64', 'int32', 'float32']:
            df[col] = df[col].replace(-1, np.nan)

# 4. Standardization & Enrichment (caract)
print("🌍 Standardizing Coordinates and Dates...")
# Coordinates
caract['lat'] = pd.to_numeric(caract['lat'].astype(str).str.replace(',', '.'), errors='coerce')
caract['long'] = pd.to_numeric(caract['long'].astype(str).str.replace(',', '.'), errors='coerce')

# Date parsing
caract['an'] = 2024 

def format_time(t):
    t_str = str(t).strip()
    if pd.isna(t) or t_str == 'nan' or t_str == '': return "00:00"
    if ':' in t_str: return t_str
    if len(t_str) <= 2: return f"{t_str.zfill(2)}:00"
    return f"{t_str[:-2].zfill(2)}:{t_str[-2:]}"

caract['hrmn_clean'] = caract['hrmn'].apply(format_time)

caract['accident_datetime'] = caract['an'].astype(str) + "-" + \
                              caract['mois'].astype(str).str.zfill(2) + "-" + \
                              caract['jour'].astype(str).str.zfill(2) + " " + \
                              caract['hrmn_clean'] + ":00"

caract['accident_datetime'] = pd.to_datetime(caract['accident_datetime'], errors='coerce')

# Time of Day bucketing
print("☀️ Enriching Time of Day...")
def get_time_of_day(hour):
    if pd.isna(hour): return np.nan
    if 6 <= hour < 12: return 'Morning'
    elif 12 <= hour < 17: return 'Afternoon'
    elif 17 <= hour < 22: return 'Evening'
    else: return 'Night'

caract['time_of_day'] = caract['accident_datetime'].dt.hour.apply(get_time_of_day)

# Drop redundant raw date columns to keep Silver layer clean
caract = caract.drop(columns=['jour', 'mois', 'an', 'hrmn', 'hrmn_clean'])

# 5. Enrichment: Accident Severity Index
print("🚑 Calculating Accident Severity Index...")
fatalities = usagers[usagers['grav'] == 2].groupby('Num_Acc').size().reset_index(name='total_fatalities')
hospitalized = usagers[usagers['grav'] == 3].groupby('Num_Acc').size().reset_index(name='total_hospitalized')

severity_df = pd.merge(fatalities, hospitalized, on='Num_Acc', how='outer').fillna(0)
severity_df['severity_index'] = (severity_df['total_fatalities'] * 10) + (severity_df['total_hospitalized'] * 2)

# Merge back to caract
caract = pd.merge(caract, severity_df, on='Num_Acc', how='left')
caract['total_fatalities'] = caract['total_fatalities'].fillna(0)
caract['total_hospitalized'] = caract['total_hospitalized'].fillna(0)
caract['severity_index'] = caract['severity_index'].fillna(0)

# 6. Save to Silver Layer
print("💾 Writing to Silver Layer...")
caract.to_csv('silver/caract_silver.csv', index=False)
lieux.to_csv('silver/lieux_silver.csv', index=False)
usagers.to_csv('silver/usagers_silver.csv', index=False)
vehicules.to_csv('silver/vehicules_silver.csv', index=False)

print("✅ Silver ETL Pipeline completed successfully! Clean datasets are in the '/silver' folder.")
