import pandas as pd
import numpy as np

# Load datasets
caract = pd.read_csv('caract-2024.csv', sep=';')
lieux = pd.read_csv('lieux-2024.csv', sep=';')
usagers = pd.read_csv('usagers-2024.csv', sep=';')
vehicules = pd.read_csv('vehicules-2024.csv', sep=';')

datasets = {'caract': caract, 'lieux': lieux, 'usagers': usagers, 'vehicules': vehicules}

print("--- 1. DUPLICATES ---")
for name, df in datasets.items():
    duplicates = df.duplicated().sum()
    print(f"{name.capitalize()}: {duplicates} duplicates")

print("\n--- 2. VALUE RANGES (Anomalies) ---")
# Usagers: Age anomalies
if 'an_nais' in usagers.columns:
    # Assuming accident year is 2024
    invalid_birth_years = usagers[(usagers['an_nais'] < 1900) | (usagers['an_nais'] > 2024)]
    print(f"Usagers (an_nais): {len(invalid_birth_years)} rows with invalid birth year (e.g., <1900 or >2024)")

# Caract: Coordinates anomalies
# Lat/long are objects, need to replace ',' with '.' and convert to float
caract['lat_float'] = pd.to_numeric(caract['lat'].str.replace(',', '.'), errors='coerce')
caract['long_float'] = pd.to_numeric(caract['long'].str.replace(',', '.'), errors='coerce')

# France bounding box (approximate including over-seas territories)
# Lat: -90 to 90, Long: -180 to 180 is valid mathematically. Let's just check invalid math coords.
invalid_lat = caract[(caract['lat_float'] < -90) | (caract['lat_float'] > 90)]
invalid_long = caract[(caract['long_float'] < -180) | (caract['long_float'] > 180)]
missing_coords = caract[caract['lat_float'].isna() | caract['long_float'].isna()]

print(f"Caract (Coordinates): {len(invalid_lat)} invalid latitudes (< -90 or > 90)")
print(f"Caract (Coordinates): {len(invalid_long)} invalid longitudes (< -180 or > 180)")
print(f"Caract (Coordinates): {len(missing_coords)} unparseable/missing coordinates")


print("\n--- 3. CATEGORICAL ANOMALIES ---")
# Just sample a few known categorical columns
if 'sexe' in usagers.columns:
    invalid_sex = usagers[~usagers['sexe'].isin([1, 2, -1])]['sexe'].value_counts()
    if len(invalid_sex) > 0:
        print(f"Usagers (sexe): Invalid categories found:\n{invalid_sex}")
    else:
        print("Usagers (sexe): No invalid categories (only 1, 2, -1 found).")

if 'lum' in caract.columns:
    invalid_lum = caract[~caract['lum'].isin([1, 2, 3, 4, 5, -1])]['lum'].value_counts()
    if len(invalid_lum) > 0:
        print(f"Caract (lum): Invalid categories found:\n{invalid_lum}")
    else:
        print("Caract (lum): No invalid categories (only 1-5, -1 found).")
