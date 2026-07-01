import pandas as pd
import os

caract = pd.read_csv('caract-2024.csv', sep=';')
lieux = pd.read_csv('lieux-2024.csv', sep=';')
usagers = pd.read_csv('usagers-2024.csv', sep=';')
vehicules = pd.read_csv('vehicules-2024.csv', sep=';')

datasets = {'caract': caract, 'lieux': lieux, 'usagers': usagers, 'vehicules': vehicules}

for name, df in datasets.items():
    print(f"\n--- {name.upper()} ---")
    # Some missing values might be encoded as -1 (which is common in this dataset) or pd.NA
    # We will just look at standard NaNs first, but we can also check for -1.
    
    # Standard missing
    missing = df.isnull().sum()
    missing_pct = (missing / len(df)) * 100
    missing_df = pd.DataFrame({'Missing_Count': missing, 'Missing_Pct': missing_pct})
    missing_df = missing_df[missing_df['Missing_Pct'] > 0].sort_values(by='Missing_Pct', ascending=False)
    
    print(missing_df)
    
    # Also check if there are many -1 values which often denote "not filled" or "unknown"
    print("\n-1 (Unknown) Values Count:")
    for col in df.columns:
        if df[col].dtype in ['int64', 'float64']:
            count_minus_one = (df[col] == -1).sum()
            if count_minus_one > 0:
                print(f"{col}: {count_minus_one} ({(count_minus_one/len(df))*100:.2f}%)")
